'''
#Basima Zafar
#CMSC 416: Natural Language Processing
#Progamming Assignment 4: Word Sense Disambiguation
#The purpose of this program is to catagorize <head>line</head> in each paragraph as either a product or phone
#In order to do this, you have to train your word sense disambiguation on your training data and utilize what it has learned on the testing data
#The training file has a small paragraph as well as the sense that it is
#The testing file has a small paragraph and when we run it through the word sense dismabiguation, our goal to accurately catagorize it as either
# a product or phone based off the log likely hood 
#The output utilies STDOUT, so in the command line, following the two files, use '>' along with the filename.txt that you would like to output to
#To run this program in the terminal the commands are: python3 wsd.py line-train.txt line-test.txt my-model.txt > my-line-answers.txt
#It is not necceasry to add the 3.8 after python unless you're IDE defaults to the python 2.7 interpretor 
'''

import os
import sys
import re
import csv
import itertools
from collections import Counter
import string
import math
import random

'''
################################################################
# Fucntion: Main
# Parameter: command line arguments
# The purpose of the main method is to read three files from the command line
# The program outputs to STDOUT, hence when the '>' is typed in following a filename.txt anything that 
# prints in the program will output directy to that file (within the same directory)
# After the files are read, the words unnecessary in the file are removed with a series of regex statements (words like corupus, lexlt, etc.)
# There is also a regex statement to remove unncessary punctuation, such as an exclamation point, we have to remove so that it is not included as word (this happens if there is a space between the word and punctuation)
# There is also a regex statement to replaces any occurence of <head>lines</head> with <head>line</head>, we have to do this so that we can recognize the surronding words around the word line 
# and replacing lines with line makes each occurance easier to locate
###############################################################
'''

def main(argv):
    trainFile = str(sys.argv[1])
    testingFile = str(sys.argv[2])
    model = str(sys.argv[3])

    openTrainFile = open(trainFile, "r")
    contentsTrain = openTrainFile.read().lower()


    openTestFile = open(testingFile, "r")
    contentsTest = openTestFile.read().lower()



    #remove words:corpus, lexlt,context and instance from file and replace with a white space
    contentsTrain=re.sub(r'<[/]?corpus(.*)>\s|<[/]?lexelt(.*)>\s|<[/]?context>\s|</instance>\s',"",contentsTrain)
    
    contentsTest=re.sub(r'<[/]?corpus(.*)>\s|<[/]?lexelt(.*)>\s|<[/]?context>\s|</instance>\s',"",contentsTest)

    contentsTrain=re.sub(r'<s>|</s>|<@>|</@>|<p>|</p>',"",contentsTrain)
    contentsTest=re.sub(r'<s>|</s>|<@>|</@>|<p>|</p>',"",contentsTest)

    contentsTrain=re.sub(r'[!#?,.;-]',"",contentsTrain) #did remove periods before but added space in 4.5 so it was 4 5
    contentsTest=re.sub(r'[!#?,.;-]',"",contentsTest) #got rid of period, may affect decimals somwhats like the 4.5

    

    contentsTrain = re.sub( r"\<head\>lines\<\/head\>", "<head>line</head>",contentsTrain)
    contentsTest = re.sub( r"\<head\>lines\<\/head\>", "<head>line</head>",contentsTest)



    #Splits the training and testing file to return a list of lines in a string 
    contentsTrainSplit=contentsTrain.splitlines() #whole file is split by \n, each \n is put in its own index
    contentsTestSplit = contentsTest.splitlines()


    #For our output, we have to print out the instance number, so in order to do that you have to capture each instance number
    #This is done through regex, the pattern finds all the instance line numbers and then appends it to listInstance
    #This will come in handy when printing out results 

    listInstance=[]
    for x in contentsTestSplit:
        instanceId = re.findall('<instance id="([^"]*)"', x)
        listInstance.append(instanceId)
    
    
    #The above for loop creates a list of line numbers, but every other one is empty, in order to do have a proper list of instance numbers, we have to remove them
    #Prior: [lineNum],[],[lineNum],[]
    #A for loop that traverses through listInstance and appends each number to listInstanceFil if it is not empty
    listInstanceFil = [x for x in listInstance if x != []]


   #This for loop removes any line in the testing file list that starts with <instance id=" and replaces it with a white space
    for i,line in enumerate(contentsTestSplit):
        if line.startswith("<instance id="):
            contentsTestSplit[i]=""

    #While loop that traverses through the testing file list and removes any occurance of a whitespace
    #This has to be done in order to remove any indicies in the list that are empty
    while("" in contentsTestSplit):
        contentsTestSplit.remove("")
            

    #In order to train our word sense disambiguation program, we have to capture all the correct senses in our training data
    #To do this, I utilized regex to search for the pattern in each index of the list, if a match was found, it would append it to the list of senses
    # along with incrementing the count of either phone or product
    #We have to keep count of both phone or product to use later when calculating log likelyhood

    pattern='senseid="([^"]*)"'
    senses=[]
    phone_freq_count=0
    prod_freq_count=0

    for i in contentsTrainSplit:
        match = re.search(pattern, i)
        if match:
            sense=match.group(1)
            senses.append(sense)

            if sense=='phone':
                phone_freq_count+=1
            else:
                prod_freq_count+=1

    

    finTrain =[]

    for i in contentsTrainSplit[2::3]: #list slicing gets rid of the instance id and sense id, now we just have the text we need
        finTrain.append(i)
    
    #calls the split_list method that seperates each paragraph that contains <head>line</head> into an list of arrays
    #So it would look like this: [[the,new,york],[according, to]]
    trainWordsList = split_list(finTrain)
    testWordsList = split_list(contentsTestSplit)


    #creation of dictionary d --> this will be utilized to create a nested dictionary in the if statements below
    d={}

    for index in range(0,len(trainWordsList)):
        contents=trainWordsList[index] #On each iteration, this gets the list of words of a single paragraph

        currentSense = senses[index] #on each iteration, this gets the sense that correlates to pargraph (list of words) above

        #A for loop that traverses through the list of words(that make up a paragraph) to locate where <head>line</head> is
        #Once the word matches <head>line</head> it sets locate to that index, this is neccessary in order to grab the surronding words

        matchLine = "<head>line</head>"
        for j in range(0,len(contents)):
            matchF=re.search(matchLine,contents[j])
            if matchF:
                locate = j


        #Yarowsky's Rule: Word immediately to the left
        #If the locate variable set above minus 1 is greater than 0 (this shows that the location is reachable), then capture the word to the left of <head>line </head>
        #It added the tag "L-1" to the word captured (this is so that we can recognize where the word captured in refence to <head>line</head>)
        #Once the word has added the tag, if the left_word is not in dictonary (which it won't be on the first occurance), it adds it as the key to the d dictionary
        # it then creates a nested dictionary inside of the d dictionary which had product and phone as the key (in the nested dict)
        # If the leftword is already in the dictionary, which it will be after the first occurrance/if statement, it increments the value in the nested dictionary depending on if the current sense
        # is phone or product
        # The following if statements follow the exact same structure, but instead captures the other surronding words (right,right window,etc)
        if (locate-1) >= 0:
            left_word = "L-1: " + contents[locate-1] 

            if left_word not in d:
                d[left_word]={}
                d[left_word]["product"]=0
                d[left_word]["phone"]=0

            if left_word in d:
                if currentSense=="phone":
                    d[left_word]["phone"]+=1
                else:
                    d[left_word]["product"]+=1
        #Yarowsky's Rule: Word found in -2 word window
        if(locate-2) >=0:
            left_word_2 = "L-2: " + contents[locate-2]

            if left_word_2 not in d:
                d[left_word_2]={}
                d[left_word_2]["product"]=0
                d[left_word_2]["phone"]=0

            if left_word_2 in d:
                if currentSense=="phone":
                    d[left_word_2]["phone"]+=1
                else:
                    d[left_word_2]["product"]+=1
        #Yarowsky's Rule: Word immediately to the right
        if(locate+1) <len(contents):
            right_word = "R+1: " + contents[locate+1] 

            if right_word not in d:
                d[right_word]={}
                d[right_word]["product"]=0
                d[right_word]["phone"]=0
 
            if right_word in d:
                if currentSense=="phone":
                    d[right_word]["phone"]+=1
                else:
                    d[right_word]["product"]+=1
        #Yarowsky's Rule: Word found in -2/+2 word window
        if(locate-2) and (locate+2) <len(contents): 
            right_word_wind_1 = "R_wind_+1: " + contents[locate+1]
            right_word_wind_2="R_wind_+2: " +contents[locate+2]

            left_word_wind_1= "L_wind_-1: " + contents[locate-1]
            left_word_wind_2= "L_wind_-2: " + contents[locate-2]


            if right_word_wind_1 not in d:
                d[right_word_wind_1]={}
                d[right_word_wind_1]["product"]=0
                d[right_word_wind_1]["phone"]=0

            if right_word_wind_1 in d:
                if currentSense=="phone":
                    d[right_word_wind_1]["phone"]+=1
                else:
                    d[right_word_wind_1]["product"]+=1


            if right_word_wind_2 not in d:
                d[right_word_wind_2]={}
                d[right_word_wind_2]["product"]=0
                d[right_word_wind_2]["phone"]=0

            if right_word_wind_2 in d:
                if currentSense=="phone":
                    d[right_word_wind_2]["phone"]+=1
                else:
                    d[right_word_wind_2]["product"]+=1
        
            
            if left_word_wind_1 not in d:
                d[left_word_wind_1]={}
                d[left_word_wind_1]["product"]=0
                d[left_word_wind_1]["phone"]=0

            if left_word_wind_1 in d:
                if currentSense=="phone":
                    d[left_word_wind_1]["phone"]+=1
                else:
                    d[left_word_wind_1]["product"]+=1
            
            if left_word_wind_2 not in d:
                d[left_word_wind_2]={}
                d[left_word_wind_2]["product"]=0
                d[left_word_wind_2]["phone"]=0

            if left_word_wind_2 in d:
                if currentSense=="phone":
                    d[left_word_wind_2]["phone"]+=1
                else:
                    d[left_word_wind_2]["product"]+=1




        #Yarowsky's Rule: Pair of words at offsets -2 and -1
        if(locate-2) and (locate-1) <len(contents):
            pair_left = "L-2-1: " + contents[locate-2] + " " + contents[locate-1]

            if pair_left not in d:
                d[pair_left]={}
                d[pair_left]["product"]=0
                d[pair_left]["phone"]=0

            if pair_left in d:
                if currentSense=="phone":
                    d[pair_left]["phone"]+=1
                else:
                    d[pair_left]["product"]+=1
        #Yarowsky's Rule: Pair of words at offset -1 and +1
        if(locate-1) and (locate+1) <len(contents):
            pair_mid = "M-1+1: " + contents[locate-1] + " " + contents[locate+1]


            if pair_mid not in d:
                d[pair_mid]={}
                d[pair_mid]["product"]=0
                d[pair_mid]["phone"]=0

            if pair_mid in d:
                if currentSense=="phone":
                    d[pair_mid]["phone"]+=1
                else:
                    d[pair_mid]["product"]+=1
        #Yarowsky's Rule: Pair of words at offset +1 and +2
        if(locate+1) and (locate+2) <len(contents):
            pair_right = "R+1+2: " + contents[locate+1] + " " + contents[locate+2]

            if pair_right not in d:
                d[pair_right]={}
                d[pair_right]["product"]=0
                d[pair_right]["phone"]=0

            if pair_right in d:
                if currentSense=="phone":
                    d[pair_right]["phone"]+=1
                else:
                    d[pair_right]["product"]+=1
        


        #This is the rule I created on my own, at first I was strictly capturing words to the right of <head>line</head> due to 
        # the fact that sometimes the words that occur after define the previous words, but then I noticed that <head>line</head>
        # could be the last word and then this feature wouldn't aid in helping classifying the sense, so it was changed to gather the fourth word to the left of <head>line</head>

        if(locate-4)>=0:
            left_word_4 = "L-4: " + contents[locate-4]

            if left_word_4 not in d:
                d[left_word_4]={}
                d[left_word_4]["product"]=0
                d[left_word_4]["phone"]=0

            if left_word_4 in d:
                if currentSense=="phone":
                    d[left_word_4]["phone"]+=1
                else:
                    d[left_word_4]["product"]+=1


    #Printing sense dict to my-model.txt for debugging
    with open(argv[3], "w") as f:
        f.write("Sense Dict")
        print(d,file=f)

    
    #The two dictionaries below are used to classify the numerator and denominator for the log likelyhood (prior to dividing them and applying log)
    #for each word with the sense "phone", it finds the number of times the word occured with phone and then divides by the total phone count
    #number of time phone occurred with word divided by the total phone count 
    result_dict_phone = {word:d[word]['phone']/phone_freq_count for word in d.keys()}

    #for each word with the sense "product", it finds the number of times the word occured with product and then divides by the total product count
    #number of time product occurred with word divided by the total product count 
    result_dict_product = {word:d[word]['product']/prod_freq_count for word in d.keys()}

    #When you calculate log, you can get a negative infinity if your numerator is a 0 and a positive infinity if youur denominator is 0
    #The below for loops traverse through the phone dict and the product dict and checks to see if the value is 0.0 if it is, replaces it with a 0.1
    for key,value in result_dict_product.items():
        if (value==0.0):
            result_dict_product[key]=0.1

    for key,value in result_dict_phone.items():
        if (value==0.0):
            result_dict_phone[key]=0.1

    #For loop that traverses through the phone dict (which contains the number of times phone occurred with word divided by the total product count, for each word)
    # and product dict(which contains the number of time product occurred with word divided by the total product count, for each word)
    # and divides each value of each list by each other and adds it to the division_dict

    division_dict ={}
    for i,v in result_dict_phone.items():
        for j,k in result_dict_product.items():
            division_dict[i]={}
            division_dict[i]=(v/k)
    
    #Creation of log_dict
    #for each value in the division dict, it finds the log value and then the absolute value of it --> then adds log_dict
    log_dict ={}
    for key,value in division_dict.items():
        temp = math.log10(value)
        log_dict[key]=abs(temp)

    #Printing log dict to my-model.txt for debugging
    with open(model, "a") as f:
        f.write("Log Dict")
        print(log_dict,file=f)


###############TESTING##############################
    #creation of mini dict, this will be used to add any matches between a word in the testing and in log dict
    miniLogDict ={}

    count=0
    for index in range(0,len(testWordsList)): 
        contentsTest=testWordsList[index] #On each iteration, this gets the list of words of a single paragraph


        #A for loop that traverses through the list of words(that make up a paragraph) to locate where <head>line</head> is
        #Once the word matches <head>line</head> it sets locate to that index, this is neccessary in order to grab the surronding words
        matchLine = "<head>line</head>"
        for p in range(0,len(contentsTest)):
            matchF=re.search(matchLine,contentsTest[p])
            if matchF:
                locateTest = p


        
        #Yarowsky's Rule: Word immediately to the left
        if (locateTest-1) >= 0:
            left_word_test = "L-1: " + contentsTest[locateTest-1] 
            #If key in log_dict (key = word (ex: telephonek_1)) matches the left_word that was captured
            #It adds the word and log value as the key and value into the miniLogDict
            #The purpose of the miniLogDict is to hold the word and the log if a match if found between the log_dict and the word captured from the testing file
            #The same process goes on for each rule in the next few if statements

            for keyL, valL in log_dict.items():
                if keyL ==left_word_test: 
                    miniLogDict[keyL] = valL
        
        #Yarowsky's Rule: Word found in -2 word window        
        if (locateTest-2) >= 0:
            left_word_test_2 = "L-2: " + contentsTest[locateTest-2] 
           
            for keyL, valL in log_dict.items():
                if keyL ==left_word_test_2:
                    miniLogDict[keyL] = valL

        #Yarowsky's Rule: Word immediately to the right
        if(locateTest+1) <len(contentsTest):
            right_word_test = "R+1: " + contentsTest[locateTest+1] 

            for keyL, valL in log_dict.items():
                if keyL ==right_word_test:
                    miniLogDict[keyL] = valL


            
        #Yarowsky's Rule: Word found in -2/+2 word window
        if(locateTest-2) and (locateTest+2) <len(contentsTest):  
            right_word_wind_test_1 = "R_wind_+1: " + contentsTest[locateTest+1]
            right_word_wind_test_2="R_wind_+2: " +contentsTest[locateTest+2]

            left_word_wind_test_1= "L_wind_-1: " + contentsTest[locateTest-1]
            left_word_wind_test_2= "L_wind_-2: " + contentsTest[locateTest-2]


            for keyL, valL in log_dict.items():
                if keyL ==right_word_wind_test_1:

                    miniLogDict[keyL] = valL


            for keyL, valL in log_dict.items():
                if keyL ==right_word_wind_test_2:
                    miniLogDict[keyL] = valL


            for keyL, valL in log_dict.items():
                if keyL ==left_word_wind_test_1:
                    miniLogDict[keyL] = valL


            for keyL, valL in log_dict.items():
                if keyL ==left_word_wind_test_2:
                    miniLogDict[keyL] = valL

        #Yarowsky's Rule: Pair of words at offset -2 and -1
        if(locateTest-2) and (locateTest-1) <len(contentsTest):
            pair_left_test = "L-2-1: " + contentsTest[locateTest-2] + " " + contentsTest[locateTest-1]

            for keyL, valL in log_dict.items():
                if keyL ==pair_left_test:
                    miniLogDict[keyL] = valL
            

            
        #Yarowsky's Rule: Pair of words at offset -1 and +1
        if(locateTest-1) and (locateTest+1) <len(contentsTest):
            pair_mid_test = "M-1+1: " + contentsTest[locateTest-1] + " " + contentsTest[locateTest+1]

            for keyL, valL in log_dict.items():
                if keyL ==pair_mid_test:
                    miniLogDict[keyL] = valL
            

        
        #Yarowsky's Rule: Pair of words at offset +1 and +2
        if(locateTest+1) and (locateTest+2) <len(contentsTest):
            pair_right_test = "R+1+2: " + contentsTest[locateTest+1] + " " + contentsTest[locateTest+2]

            for keyL, valL in log_dict.items():
                if keyL ==pair_right_test:
                    miniLogDict[keyL] = valL


        #RULE OF YOUR OWN
        #Word captured four words to the left of <head>line</head>
        if(locateTest-4)>=0:
            left_word_test_4 = "L-4: " + contentsTest[locateTest-4]

            for keyL, valL in log_dict.items():
                if keyL ==left_word_test_4:
                    miniLogDict[keyL] = valL


        #We have to find the max log likelyhood value and word to know what to search for in the sense dict (called d)
        #max_value gets the max log likelyhood value of the words that matched in the testing file to the log dict
        #max_key gets the key (word captured that matched) that correlated with the max_value

        max_value = max(miniLogDict.values())
        max_keys =[k for k, v in miniLogDict.items() if v == max_value]

    

        

        #max_key returns the highest value and puts it in a list
        #if there are multiple max keys (because there may be the same log)
        #chooses a max_key at random and then evalutes if it had the highest phone or product
        if len(max_keys)>1:
            max_keys =random.sample(max_keys,1)
        

        #Traverse through the sense dict d, if the max_key matches a key in the sense dict, traverse through
        # the nested dictionary values: {telephonek_1{product:5,phone:2}}
        #It finds the highest value inside the inner dict and sets it to max_val

        for keyMax, valMax in d.items(): #
            for i in max_keys:
                if keyMax == i:
                    max_val =0

                    for k2,v2 in valMax.items():
                        if v2>max_val: #if the value in nested dicts is greater than max_val 
                            max_val =v2 #assigns the highest value in the nested dict to max_val
                            finalSense = k2 #assigns the sense (product or phone) that correlates to the highest value to finalSense variable 
                            finAns = str(listInstanceFil[count])[2:-2] #uses list slicing get rid of [''] and str(list) to capture the line number in the dict
                            #Print to STDOUT
                            print('<answer instance="'+finAns+'" senseid="'+finalSense+'"/>')
                            count = count+1 #uses as an iterator to iterate through listInstanceFil


def split_list(finTrain):
    return[item.split() for item in finTrain] #splits item sent in


if __name__ == "__main__":
    #print('---------------------------------------------------------------------------------------------')
    #print('Basima Zafar')
    main(sys.argv)