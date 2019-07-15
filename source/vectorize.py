import csv
import os
import numpy as np
import sys
import pandas as pd
from nltk.stem.porter import *
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from matplotlib import pyplot as plt
from pycm import ConfusionMatrix
import matplotlib.pyplot as plt
import pyfpgrowth
sys.setrecursionlimit(6000)
csv.field_size_limit(sys.maxsize)
#Matplotlib graph
def graph(xAxis,yAxis):
    plt.scatter(xAxis, yAxis)
    plt.xlabel("Actual Significance")
    plt.ylabel("Predicted Significance")
    plt.show()
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
def cleanData(path):
    desc = []
    courseID = []
    stop_words = set(stopwords.words('english'))
    stop_words.add('topic')
    cleanDesc=[]
    cleanSentences=""
    cleanDataFrame=pd.DataFrame(columns={"CourseID","Description"})
    files = [f for f in os.listdir(path)]
    for x in files:
        with open("../output/Full/%s" % x, "r", encoding='utf8', errors='ignore') as f:
            reader = csv.reader(f)
            for column in reader:
                for words in word_tokenize(column[1].lower()):
                    if words not in stop_words:
                        cleanSentences+=(ps.stem(words)+" ")
                cleanDataFrame = cleanDataFrame.append({"CourseID" : column[0],'Description':cleanSentences},ignore_index=True)
                cleanSentences = ""
    return cleanDataFrame

#get cleaned vocabulary
vocab = [line.rstrip('\n').lower() for line in open('../bok.txt')]
#bokVocab.append("")
bokVocab = []
holderVar =""
#emphasis, sele1cted, comparative,honors,work
ps = PorterStemmer()
for word in vocab:
    for x in word.split():
        holderVar += ps.stem(x) + " "
    holderVar = holderVar[:-1]
    bokVocab.append(holderVar)
    holderVar=""
courseAndDescDataFrame = cleanData('../output/Full/')
#print(courseAndDescDataFrame['Description'].values.tolist())
fpgrowth = []
for x in courseAndDescDataFrame['Description'].values.tolist():
    fpgrowth.append(x.split())
patterns = pyfpgrowth.find_frequent_patterns(fpgrowth, 20)
print(patterns)
#Vectorize using bok.txt
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
#vectorizer = CountVectorizer(vocabulary=bokVocab, ngram_range=(1, 5))
vectorizer = CountVectorizer()
vectors = vectorizer.fit_transform(courseAndDescDataFrame['Description']).toarray()

#toCSV(vectors)

#Create target list for machine learning to use
relevant = []
for features in vectors:
    relevant.append(np.sum(features))

#Dataframe all information together
#courseFeatures_df = pd.DataFrame(vectors, columns = bokVocab)
courseFeatures_df = pd.DataFrame(vectors, columns = vectorizer.get_feature_names())
courseFeatures_df["relevant"] = relevant
courseFeatures_df["CourseID"] = courseAndDescDataFrame['CourseID']
courseFeatures_df.to_csv("full.csv")

from sklearn.model_selection import train_test_split
#2:130 = vocab/features,1:2=target
features_train, features_test, targets_train, targets_test = train_test_split(courseFeatures_df[courseFeatures_df.columns[2:130]],courseFeatures_df[courseFeatures_df.columns[1:2]], train_size=.75)

#import sklearn.linear_model
#slm = sklearn.linear_model
from sklearn.tree import DecisionTreeClassifier

#machineLearn(DecisionTreeClassifier(),"DecisionC")
