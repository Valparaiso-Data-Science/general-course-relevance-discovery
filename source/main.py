from parse import parseXML
from topicModel import plot_10_most_common_words, listofDSCourse
from vectorize import newClean, vectorizer, cleanVectorizer, labelTargetsdf
from ML import decisionTree,visTree

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

topicModel = pd.DataFrame()
for filename in os.listdir('../fullPDFs/'):
    print(filename)
    CSV = parseXML("../fullPDFs/"+filename, 'P', 'P', 1)
    CSV.to_csv("../courses/"+filename.replace("xml","csv"), encoding="utf-8-sig")
    topicModel= pd.concat([topicModel,CSV])

cleanData = newClean(topicModel)

topicModel_df = listofDSCourse(cleanData)

from sklearn.feature_extraction.text import CountVectorizer
count_vectorizer = CountVectorizer(stop_words='english')
count_data = count_vectorizer.fit_transform(topicModel_df['Descriptions'])
plot_10_most_common_words(count_data, count_vectorizer)

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
#
