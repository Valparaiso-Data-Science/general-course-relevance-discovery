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
                f.write('%s,"%s"\n'%(courseID[classIndex],vocabKeyWord))
                vocabKeyWord.clear()
            classIndex = classIndex + 1
#Use machine learning to predict value
def machineLearn(type):
    type.fit(X_train, y_train.values.ravel())
    predictions = type.predict(X_test)
    print(type.score(X_test, y_test))
    #print(predictions.tolist())
    #print(y_test.values)
    cm1 = ConfusionMatrix(actual_vector=y_test.values.ravel(),predict_vector=predictions.tolist())
    cm1.save_html("ConfusionMatrix",color=(100,50,250))
    #graph(y_test,predictions)

    #Once we pick our working machine language
    # output = (type.predict(df[df.bokVocab[2:130]]))
    # row = 0
    # for x in output:
    #     if x > 0:
    #         print(df.loc[[row]])
    #     row = row + 1

#Vocab and dataframe prep
bokVocab = [line.rstrip('\n').lower() for line in open('../bok.txt')]
bokVocab.insert(0, "CourseID")
bokVocab.insert(1, "relevant")
desc = []
courseID = []

#Open every file in Full output, and read it into desc and courseID
files = [f for f in os.listdir('../output/Full/')]
for x in files:
    with open("../output/Full/%s" % x, "r", encoding='utf8', errors='ignore') as f:
        reader = csv.reader(f)
        for column in reader:
            desc.append(column[0].lower()+column[1].lower())
            courseID.append(column[0])
courseID = pd.Series(courseID)

#Vectorize using bok.txt
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
vectorizer = CountVectorizer(vocabulary=bokVocab, ngram_range=(1, 5))
vectors = vectorizer.fit_transform(desc).toarray()

#toCSV(vectors)

#Create target list for machine learning to use
relevant = []
for x in vectors:
    relevant.append(np.sum(x))
    #if np.sum(x)>5:
    #     relevant.append(2)
    # elif np.sum(x)>0:
    #     relevant.append(1)
    # else:
    #     relevant.append(0)

#Dataframe all information together
df = pd.DataFrame(vectors, columns = bokVocab)
df["relevant"] = relevant
df["CourseID"] = courseID

#All features and target features
X = df[df.columns[2:130]]
y = df[df.columns[1:2]]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y, train_size=.75)

import sklearn.linear_model
slm = sklearn.linear_model
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.naive_bayes import GaussianNB


plt.title("Ridge")
machineLearn(slm.RidgeClassifier())
# plt.title("SVC")
# machineLearn(SVC())
# plt.title("LogisticRegression")
# machineLearn(slm.LogisticRegression())
# plt.title("BayesianRidge")
# machineLearn(slm.BayesianRidge())
# plt.title("SGDC")
# machineLearn(slm.SGDClassifier())
# plt.title("SGDR")
# machineLearn(slm.SGDRegressor())
# plt.title("KNeighbors")
# #machineLearn(KNeighborsClassifier(n_neighbors=3))
# plt.title("DecisionTree")
# machineLearn(DecisionTreeClassifier())
# plt.title("DecisionTreeRegressor")
# machineLearn(DecisionTreeRegressor())
# plt.title("Gaussiann")
# machineLearn(GaussianNB())
