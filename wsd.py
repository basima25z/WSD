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
import math
import random


def main(argv):
    trainFile = os.path.basename(sys.argv[1])
    testingFile = os.path.basename(sys.argv[2])
    model = os.path.basename(sys.argv[3])

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




    contentsTrainSplit=contentsTrain.splitlines() #whole file is split by \n, each \n is put in its own index
    contentsTestSplit = contentsTest.splitlines()


    listInstance=[]
    for x in contentsTestSplit:
        instanceId = re.findall('<instance id="([^"]*)"', x)
        listInstance.append(instanceId)
    
    

    listInstanceFil = [x for x in listInstance if x != []]


    instanceList =[]
    instanceMatch = '<instance id="([^"]*)"'
    for i in contentsTestSplit:
        matchy = re.match(instanceMatch,i)
        if matchy:
            instanceMatchy = matchy.group(0)
            instanceList.append(instanceMatchy)

   
    for i,line in enumerate(contentsTestSplit):
        if line.startswith("<instance id="):
            contentsTestSplit[i]=""

    while("" in contentsTestSplit):
        contentsTestSplit.remove("")
            


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
    


    trainWordsList = split_list(finTrain)
    
    testWordsList = split_list(contentsTestSplit)



    d={}

    for index in range(0,len(trainWordsList)):
        contents=trainWordsList[index] #pargraph

        currentSense = senses[index]


        matchLine = "<head>line</head>"
        for j in range(0,len(contents)):
            matchF=re.search(matchLine,contents[j])
            if matchF:
                locate = j


        #Yarowsky's Rule: Word immediately to the left
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
        #Yarowsky's Rule: Word found in -/+2 word window
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
        


        #RULE OF YOUR OWN

        if(locate-4)>=0:
            left_word_4 = "R-4: " + contents[locate-4]

            if left_word_4 not in d:
                d[left_word_4]={}
                d[left_word_4]["product"]=0
                d[left_word_4]["phone"]=0

            if left_word_4 in d:
                if currentSense=="phone":
                    d[left_word_4]["phone"]+=1
                else:
                    d[left_word_4]["product"]+=1



    

    result_dict_phone = {word:d[word]['phone']/phone_freq_count for word in d.keys()}
    result_dict_product = {word:d[word]['product']/prod_freq_count for word in d.keys()}


    for key,value in result_dict_product.items():
        if (value==0.0):
            result_dict_product[key]=0.1


    for key,value in result_dict_phone.items():
        if (value==0.0):
            result_dict_phone[key]=0.1

    division_dict ={}
    for i,v in result_dict_phone.items():
        for j,k in result_dict_product.items():
            division_dict[i]={}
            division_dict[i]=(v/k)
    


    log_dict ={}
    for key,value in division_dict.items():
        temp = math.log10(value)
        log_dict[key]=abs(temp)

    

###############TESTING##############################
    miniLogDict ={}

    count=0
    for index in range(0,len(testWordsList)): #testWordsList
        contentsTest=testWordsList[index] #pargraph


        matchLine = "<head>line</head>"
        for p in range(0,len(contentsTest)):
            matchF=re.search(matchLine,contentsTest[p])
            if matchF:
                locateTest = p
        

        if (locateTest-1) >= 0:
            left_word_test = "L-1: " + contentsTest[locateTest-1] 
            

            for keyL, valL in log_dict.items():
                if keyL ==left_word_test:
                    miniLogDict[keyL] = valL
        
                    
        if (locateTest-2) >= 0:
            left_word_test_2 = "L-2: " + contentsTest[locateTest-2] 
           


            for keyL, valL in log_dict.items():
                if keyL ==left_word_test_2:
                    miniLogDict[keyL] = valL

        if(locateTest+1) <len(contentsTest):
            right_word_test = "R+1: " + contentsTest[locateTest+1] 

            for keyL, valL in log_dict.items():
                if keyL ==right_word_test:
                    miniLogDict[keyL] = valL


            
        #Yarowsky's Rule: Word found in -/+2 word window
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

        if(locateTest-4)>=0:
            left_word_test_4 = "R-4: " + contentsTest[locateTest-4]

            for keyL, valL in log_dict.items():
                if keyL ==left_word_test_4:
                    miniLogDict[keyL] = valL


        max_value = max(miniLogDict.values())
        max_keys =[k for k, v in miniLogDict.items() if v == max_value]

        

        #max_key returns the highest value and puts it in a list
        #if there are multiple max keys (because there may be the same log)
        #chooses a max_key at random and then evalutes if it had the highest phone or productx 
        if len(max_keys)>1:
            max_keys =random.sample(max_keys,1)


        for keyMax, valMax in d.items():
            for i in max_keys:
                if keyMax == i:
                    max_val =0

                    for k2,v2 in valMax.items():
                        if v2>max_val: #what do u do if product =1 and phone =1 
                            max_val =v2
                            finalSense = k2
                            #print("senseid=", finalSense)
                            #print(listInstanceFil[count])
                            #ans = listInstance[count]
                            finAns = str(listInstanceFil[count])[2:-2]

                            print('<answer instance="'+finAns+'" senseid="'+finalSense+'"/>')
                            count = count+1


def split_list(finTrain):
    return[item.split() for item in finTrain]


if __name__ == "__main__":
    #print('---------------------------------------------------------------------------------------------')
    #print('Basima Zafar')
    main(sys.argv)