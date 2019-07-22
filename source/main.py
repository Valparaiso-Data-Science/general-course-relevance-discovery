from parse import parseDirectory
from vectorize import cleanData, vectorizer, cleanVectorizer, labelTargetsdf
from ML import decisionTree,visTree

import os
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn import tree,metrics
from sklearn.tree.export import export_text



pd.options.display.max_columns = 14
pd.set_option('display.width', 600)

courses_dict = parseDirectory("../tempPDFs/")
courses_df = pd.DataFrame(courses_dict,index=[0,1]).transpose()
print("\tfound courses")
cleaned_df = cleanData(courses_df)
print("\tcleaned")
vect_df = vectorizer(cleaned_df)
print("\tvect")
pruned_df = cleanVectorizer(vect_df)
print("\tpruned")
labeled_df = labelTargetsdf(pruned_df)
print("\tfound targets")

#%%
import matplotlib.pyplot as plt
features = labeled_df.drop("curricula relevance",axis = 1)
labels = labeled_df["curricula relevance"]


feature_train, feature_test, answer_train, answer_test = train_test_split(features,
                                                                          labels,
                                                                          test_size=0.2)

dTree = decisionTree(feature_train,answer_train,10)

test_set_prediction = dTree.predict(feature_test)
print("Accuracy:",metrics.accuracy_score(answer_test, test_set_prediction))
    
graph = export_text(dTree,feature_names=list(features.columns))
print(graph)


plot = tree.plot_tree(dTree,feature_names=list(features.columns),fontsize=10)

plot.set_size_inches(15, 10)


