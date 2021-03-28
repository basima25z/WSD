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
    contentsTrain = openTrainFile.read()

    openTestFile = open(testingFile, "r")
    contentsTest = openTestFile.read()

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

    print(finTrain) #this is accurate

    #First rule is k-1
    # the dict should look like: 










    






if __name__ == "__main__":
    #print('---------------------------------------------------------------------------------------------')
    #print('Basima Zafar')
    main(sys.argv)