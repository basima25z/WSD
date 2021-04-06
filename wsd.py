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
    contentsTest=re.sub(r'<[/]?corpus(.*)>\s|<[/]?lexelt(.*)>\s|<[/]?context>\s|</instance>\s',"",contentsTest)

    contentsTrain=re.sub(r'<s>|</s>|<@>|</@>|<p>|</p>',"",contentsTrain)
    contentsTest=re.sub(r'<s>|</s>|<@>|</@>|<p>|</p>',"",contentsTest)

    contentsTrain=re.sub(r'[!#?,.:;]',"",contentsTrain) #did remove periods before but added space in 4.5 so it was 4 5
    contentsTest=re.sub(r'[!#?,.;]',"",contentsTest) #got rid of period, may affect decimals somwhats like the 4.5

    #period only
    #contentsTrain=re.sub(r'((\d+)[\.])(?!([\d]+))',"",contentsTrain)
    #contentsTest=re.sub(r'((\d+)[\.])(?!([\d]+))',"",contentsTest)
    

  

    #contentsTest=re.sub(r'(.*)\.(?!\d)',"",contentsTest)


    #print("train after sub",contentsTrain)
    #print("test after sub", contentsTest)


    contentsTrain = re.sub( r"\<head\>lines\<\/head\>", "<head>line</head>",contentsTrain)
    contentsTest = re.sub( r"\<head\>lines\<\/head\>", "<head>line</head>",contentsTest)

    #print(contentsTrain)
    print("contentsTest", contentsTest)
    
    #need to make a list of sense with freq to help with log 
    #contentsTest = re.sub(r"<[/]?instance id=(.*)>\s", "", contentsTest)

    # matchesIndicies =[]


    contentsTrainSplit=contentsTrain.splitlines() #whole file is split by \n, each \n is put in its own index
    contentsTestSplit = contentsTest.splitlines()
    #print("Contents Train",contentsTrainSplit)
    print("Contents Test SPlit", contentsTestSplit)
    # print("length test", len(contentsTestSplit))

    listInstance=[]
    for x in contentsTestSplit:
        instanceId = re.findall('<instance id="([^"]*)"', x)
        listInstance.append(instanceId)
    
    print("listy",listInstance)

    #contentsTestSplit=re.sub(r"<[/]?instance(.*)>\s", "", contentsTestSplit)

    # listInstance =[]
    # instanceMatch = '<instance id="([^"]*)"'
    # for i in contentsTestSplit:
    #     i=re.sub(instanceMatch, "", i)
        # matchFound = re.search(instanceMatch,i)
        # if matchFound:
        #     print("match found: ",matchFound)
        #     i=re.sub(r"<[/]?instance(.*)>\s", "", matchFound)
            # matchy = matchFound.group(1)
            # listInstance.append(matchy)
            # i = re.sub(matchFound, "")
            # #matchFound.replace("")
            #matchFound=re.sub('<instance id="([^"]*)"',"",matchFound)

    #print("listInstance", listInstance)

    instanceList =[]
    instanceMatch = '<instance id="([^"]*)"'
    #pat = re.compile(r'<instance id="([^"]*)"')
    for i in contentsTestSplit:
        matchy = re.match(instanceMatch,i)
        if matchy:
            instanceMatchy = matchy.group(0)
            instanceList.append(instanceMatchy)
            #i.replace(instanceMatch, "")
            #i = pat.sub("",i)
            #print("idk: ",matchy.group(0))
    
    print("instancee list: ",instanceList)

   
    for i,line in enumerate(contentsTestSplit):
        if line.startswith("<instance id="):
            #i.replace(i,"")
            #alrightTest.append(i)
            contentsTestSplit[i]=""

    while("" in contentsTestSplit):
        contentsTestSplit.remove("")
            



    print("after removal", contentsTestSplit)
    





    # patternI='<instance id="([^"]*)"'
    # matchesIn =[]
    # for k in contentsTestSplit:
    #     matchI = re.search(patternI, k)
    #     if matchI:
    #         matchesIn.append(matchI)
    
    # print("matchesIn", matchesIn)
        

    
   # print("matchfound", listInstance)
    
    #print("listInstance", listInstance)

    


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
    print("fin train", finTrain)




    # finTest =[]

    # for i in contentsTestSplit[2::3]: #list slicing gets rid of the instance id and sense id, now we just have the text we need
    #     finTest.append(i)

    # print("fin test",finTest) #this is accurate

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
    #print("trainwordsList", trainWordsList)
    testWordsList = split_list(contentsTestSplit)
    print("testwordlist", testWordsList)
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

    print("SENSE DICT: ", d) # 8 product, 52 phone - the, new - 9 prod , 1 phone
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


    print("Phone Count: ", phone_freq_count) #178
    print("Product Count: ", prod_freq_count) #196


    #log likely score
    # P1 = "word_sense_k_1" "how many time phone occured within word send k-1" / total phone_freq_count
    # p2 = "Word_sense_k_1" "how many times product occured within word sense k_1"/ total prod_freq_count
    # LL = log (p1/p2) --> this goes into log dict for that word sense --> {word_k-1: LL score, word_k_2: LL score}

    #my dict looks like : {'L-1: access': {'product': 0, 'phone': 15}, 'L-2: 4.5%': {'product': 0, 'phone': 1}, 'R+1: growth': {'product': 0, 'phone': 3}
    

    # for key,value in d:
    #     product = value["product"]
    #     phone = value["phone"]
    #     print(key,product,phone)

    # for i in d.values():
    #     print(i)
    #     for j in d[i].values():
    #         print(j)

    #works
    # for key,value in d.items():
    #     print("Key: ",key) #Key: access
    #     print("Value: ", value) #Value: {'product': 0, 'phone': 15}



    #WORKS
    # for i in d:
    #     for j,k in d[i].items():
    #         print(i,j, "-->",k)

    
    # products_count = 20 
    # result_dict = {word:test_dict[word]['phone']/products_count for word in test_dict.keys()}
    result_dict_phone = {word:d[word]['phone']/phone_freq_count for word in d.keys()}
    result_dict_product = {word:d[word]['product']/prod_freq_count for word in d.keys()}
    print("result_phone: ", result_dict_phone)
    print("result_prod: ", result_dict_product)


    # for key in result_dict_product:
    #     li = d[key]
    #     print("LIT: ", li) #{'product': 0, 'phone': 15}

    for key,value in result_dict_product.items():
        #print("key: ", key)
        #print("value: ", value)
        if (value==0.0):
            result_dict_product[key]=0.1

    print("after replaced - product: ",result_dict_product)

    for key,value in result_dict_phone.items():
        #print("key: ", key)
        #print("value: ", value)
        if (value==0.0):
            result_dict_phone[key]=0.1

    print("after replaced - phone: ",result_dict_phone)



    division_dict ={}
    for i,v in result_dict_phone.items():
        for j,k in result_dict_product.items():
            division_dict[i]={}
            division_dict[i]=(v/k)
    
    print("Division DICT: ", division_dict) #'L-2: establish': 0.0,
    #'L-2: establish': 0.0, 'R+1: as': 0.0, 'R_wind_+1: as': 0.0, 



    log_dict ={}
    for key,value in division_dict.items():
        temp = math.log10(value)
        log_dict[key]=abs(temp)

    print("LOG DICT: ", log_dict)

    # matchKey = "L-1: access"
    # for keyL, valL in log_dict.items():
    #     if keyL ==matchKey:
    #         print("match key log: ", keyL)
    #         print("mtach val log: ", valL)

###############TESTING##############################
    print("###############TESTING##############################")

    maxLog =0
    miniLogDict ={}


    for index in range(0,len(testWordsList)): #testWordsList
        #print("index: ",index)
        contentsTest=testWordsList[index] #pargraph

        #print(len(contents))
        

        #currentSenseLine = senses[index]
        #print(currentSense)

        matchLine = "<head>line</head>"
        for p in range(0,len(contentsTest)):
            matchF=re.search(matchLine,contentsTest[p])
            if matchF:
                locateTest = p
                #print("location: ",locateTest)
        

        if (locateTest-1) >= 0:
            left_word_test = "L-1: " + contentsTest[locateTest-1] 
            print("left test: ",left_word_test)

            # for keyL, valL in log_dict.items():
            #     if keyL == left_word_test:
            #         print("match key log: ", keyL)
            #         print("match val log: ", valL)
            #         maxLog=valL

            for keyL, valL in log_dict.items():
                if keyL ==left_word_test:
                    print("match key log: ", keyL)
                    print("match val log: ", valL)
                    miniLogDict[keyL] = valL
                    max_value = max(miniLogDict.values()) #even if u find maxVal --> you have to know which word in occurs with so you can go to you sense dict so put it in a new mini dict
                    max_keys = [k for k, v in miniLogDict.items() if v == max_value]
        
                    
        if (locateTest-2) >= 0:
            left_word_test_2 = "L-2: " + contentsTest[locateTest-2] 
            print("left test -2: ",left_word_test_2)


            for keyL, valL in log_dict.items():
                if keyL ==left_word_test_2:
                    print("match key log: ", keyL)
                    print("match val log: ", valL)
                    miniLogDict[keyL] = valL
                    max_value = max(miniLogDict.values()) #even if u find maxVal --> you have to know which word in occurs with so you can go to you sense dict so put it in a new mini dict
                    max_keys = [k for k, v in miniLogDict.items() if v == max_value]

        if(locateTest+1) <len(contentsTest):
            right_word_test = "R+1: " + contentsTest[locateTest+1] 
            print("right test: ", right_word_test)

            for keyL, valL in log_dict.items():
                if keyL ==right_word_test:
                    print("match key log: ", keyL)
                    print("match val log: ", valL)
                    miniLogDict[keyL] = valL
                    max_value = max(miniLogDict.values()) #even if u find maxVal --> you have to know which word in occurs with so you can go to you sense dict so put it in a new mini dict
                    max_keys = [k for k, v in miniLogDict.items() if v == max_value]

            
        #Yarowsky's Rule: Word found in -/+2 word window
        if(locateTest-2) and (locateTest+2) <len(contentsTest): #and (locate-2) 
            right_word_wind_test_1 = "R_wind_+1: " + contentsTest[locateTest+1]
            right_word_wind_test_2="R_wind_+2: " +contentsTest[locateTest+2]

            left_word_wind_test_1= "L_wind_-1: " + contentsTest[locateTest-1]
            left_word_wind_test_2= "L_wind_-2: " + contentsTest[locateTest-2]

            print("test",right_word_wind_test_1)
            print("test",right_word_wind_test_2)
            print("test",left_word_wind_test_1)
            print("test",left_word_wind_test_2)

            for keyL, valL in log_dict.items():
                if keyL ==right_word_wind_1:
                    print("match key log: ", keyL)
                    print("match val log: ", valL)
                    miniLogDict[keyL] = valL
                    max_value = max(miniLogDict.values()) #even if u find maxVal --> you have to know which word in occurs with so you can go to you sense dict so put it in a new mini dict
                    max_keys = [k for k, v in miniLogDict.items() if v == max_value]
                if keyL ==right_word_wind_2:
                    print("match key log: ", keyL)
                    print("match val log: ", valL)
                    miniLogDict[keyL] = valL
                    max_value = max(miniLogDict.values()) #even if u find maxVal --> you have to know which word in occurs with so you can go to you sense dict so put it in a new mini dict
                    max_keys = [k for k, v in miniLogDict.items() if v == max_value]
                if keyL ==left_word_wind_1:
                    print("match key log: ", keyL)
                    print("match val log: ", valL)
                    miniLogDict[keyL] = valL
                    max_value = max(miniLogDict.values()) #even if u find maxVal --> you have to know which word in occurs with so you can go to you sense dict so put it in a new mini dict
                    max_keys = [k for k, v in miniLogDict.items() if v == max_value]
                if keyL ==left_word_wind_2:
                    print("match key log: ", keyL)
                    print("match val log: ", valL)
                    miniLogDict[keyL] = valL
                    max_value = max(miniLogDict.values()) #even if u find maxVal --> you have to know which word in occurs with so you can go to you sense dict so put it in a new mini dict
                    max_keys = [k for k, v in miniLogDict.items() if v == max_value]

        if(locateTest-2) and (locateTest-1) <len(contentsTest):
            pair_left_test = "L-2-1: " + contentsTest[locateTest-2] + " " + contentsTest[locateTest-1]
            print("test",pair_left_test)

            for keyL, valL in log_dict.items():
                if keyL ==pair_left_test:
                    print("match key log: ", keyL)
                    print("match val log: ", valL)
                    miniLogDict[keyL] = valL
                    max_value = max(miniLogDict.values()) #even if u find maxVal --> you have to know which word in occurs with so you can go to you sense dict so put it in a new mini dict
                    max_keys = [k for k, v in miniLogDict.items() if v == max_value]

            
        #Yarowsky's Rule: Pair of words at offset -1 and +1
        if(locateTest-1) and (locateTest+1) <len(contentsTest):
            pair_mid_test = "M-1+1: " + contentsTest[locateTest-1] + " " + contentsTest[locateTest+1]
            print("test",pair_mid_test)

            for keyL, valL in log_dict.items():
                if keyL ==pair_mid_test:
                    print("match key log: ", keyL)
                    print("match val log: ", valL)
                    miniLogDict[keyL] = valL
                    max_value = max(miniLogDict.values()) #even if u find maxVal --> you have to know which word in occurs with so you can go to you sense dict so put it in a new mini dict
                    max_keys = [k for k, v in miniLogDict.items() if v == max_value]

        
        #Yarowsky's Rule: Pair of words at offset +1 and +2
        if(locateTest+1) and (locateTest+2) <len(contentsTest):
            pair_right_test = "R+1+2: " + contentsTest[locateTest+1] + " " + contentsTest[locateTest+2]
            print("test",pair_right_test)

            for keyL, valL in log_dict.items():
                if keyL ==pair_right_test:
                    print("match key log: ", keyL)
                    print("match val log: ", valL)
                    miniLogDict[keyL] = valL
                    max_value = max(miniLogDict.values()) #even if u find maxVal --> you have to know which word in occurs with so you can go to you sense dict so put it in a new mini dict
                    max_keys = [k for k, v in miniLogDict.items() if v == max_value]


        #RULE OF YOUR OWN

        if(locateTest-4)>=0:
            left_word_test_4 = "R-4: " + contentsTest[locateTest-4]
            print(left_word_test_4)

            for keyL, valL in log_dict.items():
                if keyL ==left_word_4:
                    print("match key log: ", keyL)
                    print("match val log: ", valL)
                    miniLogDict[keyL] = valL
                    max_value = max(miniLogDict.values()) #even if u find maxVal --> you have to know which word in occurs with so you can go to you sense dict so put it in a new mini dict
                    max_keys = [k for k, v in miniLogDict.items() if v == max_value]
        
        print("dict", miniLogDict)
        #print("max val max key")
        print("fin: ",max_value,max_keys)


        #the first test paragraph won't execute the statments going to the right of the line bc nothing is to the right, bc its the last word

        
        #print("mini: ",miniLogDict)

        # a lot of log values are the same --> what do u do if it is?
        # if there is a same log value --> random or find what occurs the most?
        # need to capture instance number to print instance and sense id
        


            


            

        
    




        
# Now have to clean test data  - cleaned
# if word (which is already split by word ) --> if word matches <head>line</head>
# capture words before, after etc. 
# if word appears in log dict --> keep track of each if statment --> get max 
# whatever max is --> find if in the sense dict, it occurs more with phone or product







def split_list(finTrain):
    return[item.split() for item in finTrain]

    



if __name__ == "__main__":
    #print('---------------------------------------------------------------------------------------------')
    #print('Basima Zafar')
    main(sys.argv)