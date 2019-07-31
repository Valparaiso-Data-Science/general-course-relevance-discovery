#import csv
#import os
import numpy as np
#import sys
import pandas as pd
from nltk.stem.porter import *
from nltk.tokenize import word_tokenize
#from nltk.corpus import stopwords
from pycm import ConfusionMatrix
#import matplotlib.pyplot as plt
#import pyfpgrowth
#from pyspark.ml.fpm import FPGrowth
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
#from sklearn.feature_extraction.text import TfidfTransformer


#Convert vectorized variable into csv output
def toCSV(vectors):
    classIndex = 0
    vocabKeyWord = []
    with open("../output/vectorized.csv", "w") as f:
        for x in vectors:
            if np.sum(x) > 0:
                element = 0
                for vocab in np.nditer(x):
                    if vocab > 0:
                        vocabKeyWord.append(bokVocab[element])
                    element = element + 1
                try:
                    f.write('%s,"%s"\n'%(courseID[classIndex],vocabKeyWord))
                except:
                    print("1")
                vocabKeyWord.clear()
            classIndex = classIndex + 1
#Use machine learning to predict value
def machineLearn(type,string):
    type.fit(features_train, targets_train.values.ravel())
    predictions = type.predict(features_test)
    print(string)
    print(type.score(features_test, targets_test))
    #print(predictions.tolist())
    #print(targets_test.values)
    #graph(targets_test,predictions)
    cm1 = ConfusionMatrix(actual_vector=targets_test.values.ravel(),predict_vector=predictions.tolist())
    cm1.save_html(string,color=(100,50,250))
    #Once we pick our working machine language
    # output = (type.predict(df[df.bokVocab[2:130]]))
    # row = 0
    # for x in output:
    #     if x > 0:
    #         print(df.loc[[row]])
    #     row = row + 1
    print()
#Reader /output/Full csvs and convert to dataframe of CourseID and
def cleanData(df):
    desc = []
    courseID = []
    basicWords = ['too', 'about', 'hadn', 'before', 'over', 'why', 's', 'had', 'wouldn',
    'shan', "you're", 'herself', 'with', 'if', 'more', 'yourself', 'myself', 'aren', 'in', 'and',
    "wasn't", "haven't", 'now', "that'll", 'out', 'they', 'all', 'should', 'weren', "won't", 'him', 'me',
    'itself', "isn't", 'your', "doesn't", 'don', 'ma', 'each', 'because', 'we', 'there', 'have', 'was', 'themselves',
    'does', 'of', 'yours', 'shouldn', 'but', 'been', 'doesn', 'you', 'are', 'our', 'o', 't', 'my', 'after', 'who',
    'wasn', 'by', 'she', 'only', 'this', 'y', 'her', "don't", "needn't", 'into', 'again', 'during', 'be', 'both',
    'he', 'mightn', 'theirs', 'i', "couldn't", 'while', 'through', 'above', 'd', "you'll", 'no', "shan't", 'or', 'on',
    'ourselves', 'his', "shouldn't", 'won', 'under', "mightn't", 'is', 'a', 'at', 've', 'nor', 'against', 'as', 'yourselves',
    'when', 'will', 'how', 'then', "hadn't", 'whom', 'to', 'once', 'up', "wouldn't", 'which', 'their', 'here', 'having', 'that',
    'has', 'ain', 'not', 'ours', "hasn't", 'isn', 'them', 'other', 'some', 'what', 'were', "didn't", 'am', "weren't", 'for',
    'couldn', "she's", 'mustn', 'haven', 'most', 'it', 'than', 'll', 'its', 'doing', 'any', "aren't", "you've", 'own',
    'do', 'same', 'himself', 'these', 'from', 'an', 're', "you'd", 'just', 'those', 'the', 'hasn', "mustn't", 'being',
    'between', 'off', 'further', 'hers', 'such', "should've", 'did', 'so', 'very', 'where', 'few', 'until', 'need',
    'down', 'can', 'below', 'didn', 'm', "it's"]
    stop_words = ['course','courses','offer','credit','student','cr','study','year','years','require','may','use','major','enroll','work','department','social','next','one','fall','spring','semester','also','permiss','class','seminar','instructor','college','well','fulfill','academic','understand','world','learn','american','and','of','the','in','to','offered','credits','be','for','on','students','with','as','is','this','or','an','are','from','each','years','by','include','will','their','at','enrollment','we','how','both','have','used','such','these','it','about','all','who','must','only','more','can','its','minor','what','do','us', 'topics','that','required','through','other','requirements','not','which','permission','emphasis','they','majors','some','based','but','no','year','century','semesters','our','has','any','within','during','using','should','in','than','the','and','if','when','them','or','many','above','why','was','you','education','general','including','health','humanities','arts','art','experience','skills','skill','includes','history','studies','university','grade','repeated','following','(',
    ')','.',',','/',';',':','?','<','>','|','[',']','~','`','~','!','@','#','$','%','^','&','*','-','_','+','a','{','}',"'","’"]
    stop_words.append(basicWords)
    #,'offer','credit','student','cr','study','year','require','may','use','major','enroll','work','department','social','next','one','fall','spring','semester','also','permiss','class','seminar','instructor','college','well','fulfill','academic','understand','world','learn','american'))
    cleanDesc=[]
    wordsRemoved = 0
    totalWords = 0
    cleanSentences=""
    cleanDataFrame=pd.DataFrame()
    #Wordcount remove low freq words
    word_counts = Counter(word_tokenize('\n'.join(df["Description"])))
    lowFreqWords = []
    for word, count in word_counts.items():
        #WE CAN ALSO GET RID OF MISSED HIGHLY OCCURING WORDS
        if count < 2 or len(word) < 3:
            lowFreqWords.append(word.lower())
    for i, row in df.iterrows():
        for words in word_tokenize(row[1].lower()):
            if words not in stop_words:
                if words not in lowFreqWords:
                            #cleanSentences+=(ps.stem(words)+" ")
                    cleanSentences+=(words+" ")
                    totalWords +=1
            else:
                wordsRemoved += 1
                totalWords += 1
        cleanDataFrame = cleanDataFrame.append({"CourseID" : row[0],'Description':cleanSentences},ignore_index=True)
        cleanDataFrame["Description"] = cleanDataFrame["Description"]
        #I have to add the courseID to the description so labeling targets searches it aswell (or fix xml to dataframe to put name in description)+ cleanDataFrame["CourseID"]
        cleanSentences = ""
    #print(wordsRemoved/totalWords)
    word_counts = Counter(word_tokenize('\n'.join(cleanDataFrame["Description"])))
    return cleanDataFrame
#Get significance weight of each word in the descriptions
def tfidf(description):
    cv=CountVectorizer()
    word_count_vector=cv.fit_transform(description)
    vectorizer = TfidfVectorizer(use_idf=True)
    vectors = vectorizer.fit_transform(description).toarray()

    df_idf = pd.DataFrame(vectorizer.idf_, index=cv.get_feature_names(),columns=["tf_idf_weights"])
    df_idf.sort_values(by=['tf_idf_weights'])
    return df_idf


def noNumbers(inputString):
    return not any(char.isdigit() for char in inputString)

def vectorizer(courseDesc_df):
    vectorizer=CountVectorizer(ngram_range=(1, 3))
    vectors = vectorizer.fit_transform(courseDesc_df['Description']).toarray()

    courseFeatures_df = pd.DataFrame(vectors, columns = vectorizer.get_feature_names(),index=courseDesc_df["CourseID"])

    return courseFeatures_df
'''
    relevant = []
    for features in vectors:
        relevant.append(np.sum(features))
    courseFeatures_df["relevant"] = relevant
    courseFeatures_df["CourseID"] = courseDesc_df['CourseID']
'''


def cleanVectorizer(df):
    cleanDF = pd.DataFrame()
    list = []
    count = 0
    total = 0
    for column in df:
        if noNumbers(column):
            if column != 'CourseID':
                #change this to greather than 2 or something when we arent using temp pdfs
                if (int(df[column].sum()) > 1):
                    list.append(column)
                    count += 1
                    total +=1
                else:
                    total +=1
    #print(total)
    #print(count)
    #list.append(df.index)
    cleanDF=df[list].copy()
    cleanDF["curricula relevance"] = False

    return(cleanDF)

def labelTargetsdf(df):
    vocab = [line.rstrip('\n').lower() for line in open('../bok.txt')]
    vocabSplit = []
    for word in vocab:
        vocabSplit.append(word.split())
    print(df)
    for words in vocabSplit:
        try:
            df["curricula relevance"] = df[words].all(1) | df["curricula relevance"]
        #Keyword not found at all (so no column to begin with)
        except:
            pass
    return df
#x = tfidf(courseAndDescDataFrame['Description'])
#x.to_csv("test.csv")

#Create target list for machine learning to use
#Dataframe all information together
#courseFeatures_df = pd.DataFrame(vectors, columns = bokVocab)

#courseFeatures_df.to_csv("full.csv")

from sklearn.model_selection import train_test_split
#2:130 = vocab/features,1:2=target
#features_train, features_test, targets_train, targets_test = train_test_split(courseFeatures_df[courseFeatures_df.columns[2:130]],courseFeatures_df[courseFeatures_df.columns[1:2]], train_size=.75)

from sklearn.tree import DecisionTreeClassifier

#machineLearn(DecisionTreeClassifier(),"DecisionC")
