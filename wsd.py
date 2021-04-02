#Basima Zafar
#PA4
#NLP: WSD

import os
import sys
import re
import csv
import itertools
from collections import Counter
import string


def main(argv):
    trainFile = os.path.basename(sys.argv[1])
    testingFile = os.path.basename(sys.argv[2])
    model = os.path.basename(sys.argv[3])

    openTrainFile = open(trainFile, "r")
    contentsTrain = openTrainFile.read().lower()
    #contentsTrain=contentsTrain.replace(string.punctuation,"")

    openTestFile = open(testingFile, "r")
    contentsTest = openTestFile.read().lower()


    #contentsTrain=removeBrackets(contentsTrain)

    #remove words:corpus, lexlt,context and instance from file and replace with a white space
    contentsTrain=re.sub(r'<[/]?corpus(.*)>\s|<[/]?lexelt(.*)>\s|<[/]?context>\s|</instance>\s',"",contentsTrain)
    #print(contentsTrain)

    contentsTrain=re.sub(r'<s>|</s>|<@>|</@>|<p>|</p>',"",contentsTrain)

    contentsTrain=re.sub(r'[!#?,:;]',"",contentsTrain)

    #print(contentsTrain)


    contentsTrain = re.sub( r"\<head\>lines\<\/head\>", "<head>line</head>",contentsTrain)

    #print(contentsTrain)

    #need to make a list of sense with freq to help with log 


    contentsTrainSplit=contentsTrain.splitlines() #whole file is split by \n, each \n is put in its own index
    #print(contentsTrainSplit)


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

    #print(senses)
    #print(phone_freq_count)
    #print(prod_freq_count)

    #print(contentsTrainSplit)

    finTrain =[]

    for i in contentsTrainSplit[2::3]: #list slicing gets rid of the instance id and sense id, now we just have the text we need
        finTrain.append(i)

    #print(finTrain) #this is accurate

    #First rule is k-1
    #the dict should look like: {word_k-1:{sense1,freq}{sense2,freq}, word_k-1:{sense1,freq} {sense_2,freq}}

    ################################################
    #how to create dictionaries
    # d={}
    # d['telephone']={}
    # d['telephone']['phone']='3'
    # d['telephone']['product'] = '5'

    # #d['call']={}
    # d['call']={}
    # d['call']['phone']='3'
    # d['call']['product'] = '5'

    #print(d)
    ##################################################
    #loop thru finTrain
    #if within a sentance --> split into just words, the <line> occurs
    #locate index
    #use index to retieve word left to 

    trainWordsList = split_list(finTrain)
    #print(trainWordsList)



    

    # wordList =[]
    # for pargarph in trainWordsList:
    #     print(pargarph) #same as split

    # count =0
    # matchesIndicies =[]
    # for index in range(0,len(trainWordsList)):

    #     for paragraph in trainWordsList:
    #         for word in paragraph:
    #             #count+=1
    #             if word =="<head>line</head>":
    #                 index=count
    #                 matchesIndicies.append(count)
    #                 #print(word,index)
    #                 #print(matchesIndicies)
    #             count+=1

    matchesIndicies=[]
    for index in range(0,len(trainWordsList)):
        for paragraph in trainWordsList:
            for i,v in enumerate(paragraph):
                if v=="<head>line</head>":
                    matchesIndicies.append(i)
    # print(matchesIndicies)
    # prin
    

            
    #print("Match: ", matchesIndicies) 

    #now we know where all of it occurs



    d={}


    #list is a list of words so it looks like 
    #[[wordp1,wordp1,wordp1],[wordp2,wordp2,wordp2]]
    for index in range(0,len(trainWordsList)):
        #print("index: ",index)
        contents=trainWordsList[index] #pargraph

        #print(len(contents))
        

        currentSense = senses[index]
        #print(currentSense)

        matchLine = "<head>line</head>"
        for j in range(0,len(contents)):
            matchF=re.search(matchLine,contents[j])
            if matchF:
                locate = j


        #Yarowsky's Rule: Word immediately to the left
        if (locate-1) >= 0:
            left_word = "L-1: " + contents[locate-1] 
            print(left_word)

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
            print(left_word_2)

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
            print(right_word)

            if right_word not in d:
                d[right_word]={}
                d[right_word]["product"]=0
                d[right_word]["phone"]=0
 
            if right_word in d:
                if currentSense=="phone":
                    d[right_word]["phone"]+=1
                else:
                    d[right_word]["product"]+=1
        #Yarowsky's Rule: Word found in -/+2 word window
        if(locate-2) and (locate+2) <len(contents): #and (locate-2) 
            right_word_wind_1 = "R_wind_+1: " + contents[locate+1]
            right_word_wind_2="R_wind_+2: " +contents[locate+2]

            left_word_wind_1= "L_wind_-1: " + contents[locate-1]
            left_word_wind_2= "L_wind_-2: " + contents[locate-2]

            print(right_word_wind_1)
            print(right_word_wind_2)
            print(left_word_wind_1)
            print(left_word_wind_2)


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
            print(pair_left)

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
            print(pair_mid)

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
            print(pair_right)

            if pair_right not in d:
                d[pair_right]={}
                d[pair_right]["product"]=0
                d[pair_right]["phone"]=0

            if pair_right in d:
                if currentSense=="phone":
                    d[pair_right]["phone"]+=1
                else:
                    d[pair_right]["product"]+=1
        


        #RULE OF YOUR OWN

        if(locate-4)>=0:
            left_word_4 = "R-4: " + contents[locate-4]
            print(left_word_4)

            if left_word_4 not in d:
                d[left_word_4]={}
                d[left_word_4]["product"]=0
                d[left_word_4]["phone"]=0

            if left_word_4 in d:
                if currentSense=="phone":
                    d[left_word_4]["phone"]+=1
                else:
                    d[left_word_4]["product"]+=1

    print(d) # 8 product, 52 phone - the, new - 9 prod , 1 phone
    # #his prod 3, phone 1 in file, should be, 1 phone, 2 prod


    # Take in testing file, 
    # clean it,
    # take it words left, right etc, 
    # search to see if theres a match in trainingDict 
    # if there is a match....?


    #make log dict and calculate log of each word
    #once created split testing data like we did before and then search for the word i
    #in the training data, if word is found --> any occurance, calcilate the log and return the highest

    #Things to consider when refractoring: there may be no words if the line ends with the word line, so may have to change rule from +4 to -4?
    


                

  



def split_list(finTrain):
    return[item.split() for item in finTrain]

    



if __name__ == "__main__":
    #print('---------------------------------------------------------------------------------------------')
    #print('Basima Zafar')
    main(sys.argv)