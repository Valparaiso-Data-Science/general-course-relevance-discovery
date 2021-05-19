'''
Main file that runs the whole pipeline, from raw XML catalogs, to course classification with decision trees.
'''

# files in the current directory
import parse
#from topicModel import plot_10_most_common_words, listofDSCourse
import createDATA
import ML
import prep
import const

#libraries
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import export_text
from sklearn.tree import export_graphviz
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import re
import xml.etree
from joblib import Parallel, delayed
from xml.etree.ElementTree import ParseError

from datetime import date

from progress.bar import Bar

# container for processed catalogs
topicModel = pd.DataFrame()

# toggle for keeping data from intermediary stages
dirty = False
if len(sys.argv) > 1 and sys.argv[1] == 'dirty':
    dirty = True

# Make all of the required directories; prep the work area
prep.prepare()
# Create 'AllSchools.csv'
createDATA.createCSV()
print("Splitting Data")
features, labels, brown_df = ML.preProcess()
print("Features: ")
print(features)
print("Labels: \n")
print(labels)
ML.stratKFold(features, labels)
ML.randForest(features, labels, brown_df)
#svm(features,labels,5)
#undersample(features, labels)
#ML.OldrandForest(features,labels)

'''
feature_train, feature_test, answer_train, answer_test = train_test_split(features, labels, test_size=0.2)

print("training tree")
dTree = decisionTree(feature_train,answer_train,20)
test_set_prediction = dTree.predict(feature_test)

print("Accuracy:",accuracy_score(answer_test, test_set_prediction))

graph = export_text(dTree,feature_names=list(features.columns))
print(graph)
print(export_graphviz(dTree,feature_names=list(features.columns),filled=True,impurity=False,label='root'))


mlaoutput = pd.DataFrame(test_set_prediction,columns=["machineAlg"])

answer_test.append(mlaoutput).to_csv("answer.csv")
answer_test['Predicted'] = pd.Series(test_set_prediction)
'''
