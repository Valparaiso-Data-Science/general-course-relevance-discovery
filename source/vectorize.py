#import csv
#import os
#import sys
#from nltk.corpus import stopwords
#import matplotlib.pyplot as plt
#import pyfpgrowth
#from pyspark.ml.fpm import FPGrowth
#from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
import pandas as pd
from nltk.stem.porter import *
from nltk.tokenize import word_tokenize
from pycm import ConfusionMatrix
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter


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
def newClean(df):
    import string
    schoolID = []
    courseID = []
    description = []
    stopwords = ['credits','spring','fall','course','students','offered','hours','credit','grade','typically']
    for i, row in df.iterrows():
        cleanDesc = row['Descriptions']
        cleanDesc = cleanDesc.translate(cleanDesc.maketrans(string.punctuation, "\\" * len(string.punctuation)))
        cleanDesc = cleanDesc.replace("\\", '')
        cleanDesc = ' '.join([word for word in cleanDesc.split() if word.lower() not in stopwords])
        schoolID.append(row['School'])
        courseID.append(row['CourseID'])
        description.append(cleanDesc)

    cleanDF = pd.DataFrame(list(zip(schoolID, courseID, description)), columns=['School', 'CourseID', 'Descriptions'])
    print(cleanDF.head())
    return (cleanDF)

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
    vectorizer=CountVectorizer(ngram_range=(1, 1))
    courseDesc_df = courseDesc_df
    print(type(courseDesc_df))
    vectors = vectorizer.fit_transform(courseDesc_df['Descriptions']).toarray()

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
                if (int(df[column].sum()) > 2):
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
        print(word)
        try:
	        df["curricula relevance"] = df[word] | df["curricula relevance"]
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
