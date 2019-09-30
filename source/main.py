from parse import parseDirectory, extractTextFromXMLBrown, extractTextFromXMLValpo, extractTextFromXMLPurdue, parseXML
from vectorize import cleanData, vectorizer, cleanVectorizer, labelTargetsdf
from ML import decisionTree,visTree

import os
import pandas as pd
import sys

from sklearn.model_selection import train_test_split
from sklearn import tree,metrics
from sklearn.tree.export import export_text
from sklearn.tree import export_graphviz



pd.options.display.max_columns = 14
pd.set_option('display.width', 600)

#courses_dict = parseDirectory("../fullPDFs/")
#courses_df = pd.DataFrame(courses_dict,index=[0,1]).transpose()
#brown_df = extractTextFromXMLBrown("../fullPDFs/BrownCourses.xml")
#purdue_df = extractTextFromXMLPurdue("../fullPDFs/Purdue.xml")
young_df = parseXML("../fullPDFs/Youngstown.xml")

# courses_df = pd.concat([brown_df,purdue_df])
# print("\tfound courses")
# cleaned_df = cleanData(courses_df)
# print("\tcleaned")
# vect_df = vectorizer(cleaned_df)
# print("\tvect")
# pruned_df = cleanVectorizer(vect_df)
# print("\tpruned")
# labeled_df = labelTargetsdf(pruned_df)
# print("\tfound targets")
# #%%
# features = labeled_df.drop("curricula relevance",axis = 1).astype("bool")
# labels = labeled_df["curricula relevance"]
# 
# print("Splitting Data")
# feature_train, feature_test, answer_train, answer_test = train_test_split(features,
#                                                                           labels,
#                                                                           test_size=0.2)
# print("training tree")
# dTree = decisionTree(feature_train,answer_train,20)
# test_set_prediction = dTree.predict(feature_test)
# 
# print("Accuracy:",metrics.accuracy_score(answer_test, test_set_prediction))
# 
# graph = export_text(dTree,feature_names=list(features.columns))
# print(graph)
# print(export_graphviz(dTree,feature_names=list(features.columns),filled=True,impurity=False,label='root'))
# 
# 
# mlaoutput = pd.DataFrame(test_set_prediction,columns=["machineAlg"])
# 
# answer_test.append(mlaoutput).to_csv("answer.csv")
# answer_test['Predicted'] = pd.Series(test_set_prediction)

