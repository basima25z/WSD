#Basima Zafar
#PA4
#NLP: WSD

import os
import sys
import re
import csv
import itertools
from collections import Counter


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
    #print(contentsTrain)

    contentsTrain=re.sub(r'<s>|</s>|<@>|</@>|<p>|</p>'," ",contentsTrain)

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



    #count=0
    #index=0
    #####################################################
    #PRETENSE:split before
    # matchIndex=0
    # for paragraph in trainWordsList:
    #     for index,word in enumerate(paragraph):
    #     #for word in paragraph:
    #         #print(index,word)
    #         #count+=1
    #         if word =="<head>line</head>":
    #             matchIndex=index
    #             print(matchIndex,word)

    #             left = matchIndex-1
    #             if(matchIndex-1)>0:
    #                 print(word[index-1])
    #             #count+=1

    #             # if(matchIndex-1)>=0:
    #             #     print(word[matchIndex-1])

    #     # if (index-1)>=0:
    #     #     left = "L:" + word[index]
    #     #     print(left)

        #####################################################

    # wordList =[]
    # for pargarph in trainWordsList:
    #     print(pargarph) #same as split

    count =0
    matchesIndicies =[]
    for index in range(0,len(trainWordsList)):

        for paragraph in trainWordsList:
            for word in paragraph:
                #count+=1
                if word =="<head>line</head>":
                    index=count
                    matchesIndicies.append(count)
                    #print(word,index)
                    #print(matchesIndicies)
                count+=1
            
    #print("Match: ", matchesIndicies) 

    #now we know where all of it occurs


    # for index in range(0,len(trainWordsList)):
    #     contents = trainWordsList[index]
    #     print(contents)

    #     for i,val in enumerate(trainWordsList[index]):
    #         #print(val)
    #         if val =="<head>line</head>":
    #             pos=i
    #             #left_word = "L: " + val
    #             #print(left_word)




    d={}
        
    
    
    for index in range(0,len(trainWordsList)):
        contents=trainWordsList[index]
        

        currentSense = senses[index]
        print(currentSense)

        for j in range(0,len(contents)):
            
            if(contents[j])=="<head>line</head>":
                locate = j
                #print(j)
            
        if (locate-1) >= 0:
            left_word = "L: " + contents[locate-1] #+" "+ contents[locate-1]
            print(left_word,currentSense)

            if left_word not in d:
                d[left_word]={}
                d[left_word]["product"]=0
                d[left_word]["phone"]=0
                # if currentSense=="phone":
                #     d[left_word]["phone"]=1
                # else:
                #     d[left_word]["product"]=1
            if left_word in d:
                if currentSense=="phone":
                    d[left_word]["phone"]+=1
                else:
                    d[left_word]["product"]+=1

    print(d) # 8 product, 52 phone - the, new - 9 prod , 1 phone
    #his prod 3, phone 1 in file, should be, 1 phone, 2 prod
                

                


    # if left_word not in d:
        # d[left_word]={}
        # d[left_word]["product"]=0
        # d[left_word]["phone"]=0

        # if sense =="phone":
        #     d[left_word]["phone"]+=1
        # else:
        #     d[left_word]["product"]+=1






       
    





   


def split_list(finTrain):
    return[item.split() for item in finTrain]

    



    


















    






if __name__ == "__main__":
    #print('---------------------------------------------------------------------------------------------')
    #print('Basima Zafar')
    main(sys.argv)