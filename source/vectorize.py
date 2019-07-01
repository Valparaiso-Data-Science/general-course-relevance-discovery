import csv
import os
import numpy as np
import sys
import pandas as pd
#from matplotlib import pyplot as plt
from pycm import ConfusionMatrix
np.set_printoptions(threshold=sys.maxsize)
csv.field_size_limit(sys.maxsize)
import matplotlib.pyplot as plt

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

#Vocab and dataframe prep
bokVocab = [line.rstrip('\n').lower() for line in open('../bok.txt')]
bokVocab.insert(0, "CourseID")
bokVocab.insert(1, "relevant")
desc = []
courseID = []

#Read all CSV's into list
files = [f for f in os.listdir('../output/Full/')]
for x in files:
    with open("../output/Full/%s" % x, "r", encoding='utf8', errors='ignore') as f:
        reader = csv.reader(f)
        for column in reader:
            desc.append(column[0].lower()+column[1].lower())
            courseID.append(column[0])

#Vectorize using bok.txt
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
vectorizer = CountVectorizer(vocabulary=bokVocab, ngram_range=(1, 5))
vectors = vectorizer.fit_transform(desc).toarray()

#toCSV(vectors)

#Create target list for machine learning to use
relevant = []
for features in vectors:
    #relevant.append(np.sum(features))
    if np.sum(features)>3:
        relevant.append(2)
    elif np.sum(features)>0:
        relevant.append(1)
    else:
        relevant.append(0)

#Dataframe all information together
courseFeatures_df = pd.DataFrame(vectors, columns = bokVocab)
courseFeatures_df["relevant"] = relevant
courseFeatures_df["CourseID"] = pd.Series(courseID)

from sklearn.model_selection import train_test_split
#2:130 = vocab/features,1:2=target
features_train, features_test, targets_train, targets_test = train_test_split(courseFeatures_df[courseFeatures_df.columns[2:130]],courseFeatures_df[courseFeatures_df.columns[1:2]], train_size=.75)

#import sklearn.linear_model
#slm = sklearn.linear_model
from sklearn.tree import DecisionTreeClassifier

machineLearn(DecisionTreeClassifier(),"DecisionC")
