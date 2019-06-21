import csv
import os
import numpy as np
import sys
import pandas as pd
from matplotlib import pyplot as plt
from pycm import ConfusionMatrix

np.set_printoptions(threshold=sys.maxsize)
csv.field_size_limit(sys.maxsize)

def graph(xAxis,yAxis):
    plt.scatter(xAxis, yAxis)
    plt.xlabel("Actual Significance")
    plt.ylabel("Predicted Significance")
    plt.show()
    
def machineLearn(type):
    type.fit(X_train, y_train)
    predictions = type.predict(X_test)
    print(type.score(X_test, y_test))
    cm1 = ConfusionMatrix(y_test.values,predictions.tolist())
    #print(cm1)
    #graph(y_test,predictions)
    
    #Once we pick our working machine language
    # output = (type.predict(df[df.bokVocab[2:130]]))
    # row = 0
    # for x in output:
    #     if x > 0:
    #         print(df.loc[[row]])
    #     row = row + 1

desc = []
courseID = []
#Get edison vocab into a list
bokVocab = [line.rstrip('\n').lower() for line in open('../bok.txt')]
bokVocab.insert(0, "CourseID")
bokVocab.insert(1, "relevant")

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

#Output of relevant
# count = 0
# classIndex = 0
# vocabKeyWord = []
# total = 0
# with open("../output/vectorized.csv", "w") as f:
#     for x in vectors:
#         element = 0
#         if np.sum(x) > 0:
#             print(np.sum(x))
#             total = total + 1
#             for vocab in np.nditer(x):
#                 if vocab > 0:
#                     vocabKeyWord.append(bokVocab[element])
#                 element = element + 1
#             f.write('%s,"%s"\n'%(courseID[classIndex],vocabKeyWord))
#             vocabKeyWord.clear()
#         count = count+1
#         classIndex = classIndex + 1
        
#Create target list for machine learning to use
relevant = []
for x in vectors:
    relevant.append(np.sum(x))
    
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
# from sklearn.svm import SVC
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.tree import DecisionTreeRegressor
# from sklearn.naive_bayes import GaussianNB

# 
#plt.title("Ridge")
# machineLearn(slm.Ridge())
# plt.title("SVC")
# machineLearn(SVC())
plt.title("LogisticRegression")
machineLearn(slm.LogisticRegression())
# plt.title("BayesianRidge")
# machineLearn(slm.BayesianRidge())
# plt.title("SGDC")
# machineLearn(slm.SGDClassifier())
# plt.title("SGDR")
# machineLearn(slm.SGDRegressor())
# plt.title("KNeighbors")
# machineLearn(KNeighborsClassifier(n_neighbors=3))
# plt.title("DecisionTree")
# machineLearn(DecisionTreeClassifier())
# plt.title("DecisionTreeRegressor")
# machineLearn(DecisionTreeRegressor())
# plt.title("Gaussiann")
# machineLearn(GaussianNB())