'''
- Basima Zafar
- CMSC: 416 - Natural Language Processing
- April 7th, 2021
- Programming Assignment 4
- This is a utility program that compares the output from wsd.py to the key provided to us
- The purpose of this program is to see how accuracte wsd.py is at classifying a sense (product or phone) to <head>line</head>
- We can see accuracy and precision with the confusion matrix and the accuracy score
- The input through the command line requires two files: my-line-answers.txt and line-key.txt
- The first file is the result of wsd.py (which was printed to STDOUT)
- The output file will be utilizing STDOUT, so the > symbol along with a file name is needed in the command line,
so that the output knows where to be printed - along with the confusion matrix being output to STDOUT, a more easily readibly confusion
will pop up when the command is ran 
- To run this program, type in the command line:python3 scorer.py my-line-answers.txt line-key.txt > report.txt
- It is not necceasry to add the 3.8 after python unless you're IDE defaults to the python 2.7 interpretor
- Note: in order to close out of this program and to write to STDOUT, you must exit the pop up python box which displays the confusion matrix
'''
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import os
import sys
import re
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt

'''
########################################################
# Function: Main
# Parameters: argv
# The main method takes in two files, the first being the outputfile from wsd.py and the second being the line-key.txt provided
# It opens up the two files and removes the dash and period from the line-key.txt file so that it will match the output file from wsd.py
# It then splits the two files and uses regex to just obtain the sense from both the test and the key provided
#########################################################
'''
def main(argv):
    testFile = os.path.basename(sys.argv[1])
    keyFile = os.path.basename(sys.argv[2])

    openTestFile = open(testFile, "r")
    contentsTest = openTestFile.read().lower()

    openKeyFile = open(keyFile, "r")
    contentsKey = openKeyFile.read().lower()


    
    contentsKey=re.sub(r'[!#?,.;-]',"",contentsKey) #need to make the key match format of test --> have to remove periods and dashes

    contentsTestWordSplit = contentsTest.split()
    contentsKeyWordSplit = contentsKey.split()

    '''
    - In order to create the confusion matrix and get the accuracy score, we have gather the sense (product or phone) on each line of the 
    of the output file from wsd.py (my-line-answers.txt) and line-key.txt
    - This is done by utilizing regex, the regex pattern captures anything that starts with senseid and ends with a quotation
    - It then traverses each word in the split files to see if the pattern matches any word, if it does match, it appends it to
    a list 
    - This process is done twice, one for my-line-answers.txt and one for line-key.txt --> in the end, we have two list of senses: senseTest and senseKey
    - SenseTest and SenseKey will be compared to create the confusion matrix and get the accuracy score
    '''

    pattern='senseid="([^"]*)"'
    senseTest=[]


    for i in contentsTestWordSplit:
        match = re.search(pattern, i)
        if match:
            sense=match.group(1)
            senseTest.append(sense)

   

    senseKey=[]


    for index in contentsKeyWordSplit:
        matchKey = re.search(pattern, index)
        if matchKey:
            senseK=matchKey.group(1)
            senseKey.append(senseK)


    '''
    # Using Pandas to create a confusion matrix to find how accurately phone and product were identified in my-line-answers.txt
    # Assigning the list senseKey and senseTest list that was created above and set it to Series (1-d Array)
    # Labeling the y_actKey as Actual and y_predTest as Predicted
    # Using crosstab method to create a confusion matrix 
    # Using accuracy_score method to find the accuracy and multipling it by 100 to get a whole number
    # Utilzing Seaborn and matplotlib to generate an easily readible confusion matrix that pops up, while also writing it and the accuracy score to STDOUT 
    '''

    '''
    #In the end, the highest accuracy achieved was 59%, the True Positives was 52, True Negatives was 23, False Negatives was 20, and the False Positive was 31
    #I believe a better accuracy would have been achieved if I built upon Yarowsky's features, I implemented all of his, and added a new one, but if I had implemented more
    and took into consideration other methods instead of log likelyhood, such as considering mean, I believe I could have achieved a better result as sometimes the max log likely hood
    of multiple if statements would be the same due to them having a similar sense dict for example: telephone-1{product:2, phone:2} and call+1{product:2, phone:2} --> these would have the same log likely hood
    #If there were multiple max log likely hood, a random word was chosen, instead of utilzing this method I could have went a step further and chosen the word that appeared closest to <line>head<line>
    #Due to the picking of a random word (if there were multiple of the same max log likelyhood), the accuracy fulctuates, so everytime you run wsd.py, the senses will change due 
    to the random picking, but even with the random picking, it has never gone below 49%
    '''

    acc = accuracy_score(senseKey, senseTest)
    print("Accuracy: ", acc *100)

    y_actKey = pd.Series(senseKey, name='Actual')
    y_predTest= pd.Series(senseTest, name='Predicted')

    df_conf = pd.crosstab(y_actKey, y_predTest)
    sn.heatmap(df_conf, annot=True)
    plt.show()

    print("\n%s" % df_conf)



if __name__ == "__main__":
    main(sys.argv)