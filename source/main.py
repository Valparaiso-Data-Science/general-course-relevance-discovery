# files in the current directory
import parse
#from topicModel import plot_10_most_common_words, listofDSCourse
from vectorize import newClean, vectorizer, cleanVectorizer, labelTargetsdf
from ML import decisionTree,visTree
from reintroduce_spaces import reintroduce_spaces
from xml_fix_utils import correct_ampersands, ignore_bad_chars

import Prep


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

from progress.bar import Bar

# container for processed catalogs
topicModel = pd.DataFrame()

# directory variables
SOURCE_DIR = "../fullPDFs"
TRIMMED_DIR = "../temp_data/TRIMMED"
SUPERTRIMMED_DIR = "../temp_data/superTrimmedPDFs"

# toggle for keeping data from intermediary stages
dirty = False
if len(sys.argv) > 1 and sys.argv[1] == 'dirty':
    dirty = True

Prep.prepare()


# trim file (whenever line number information available, otherwise keep whole file)
Parallel(n_jobs=-1)(delayed(parse.trimFile)(SOURCE_DIR, TRIMMED_DIR, filename, Prep.makeLineNumDict())
                    for filename in Bar('Trimming Files').iter(os.listdir(SOURCE_DIR)))



Parallel(n_jobs=-1)(delayed(parse.cleanXML)(TRIMMED_DIR , SUPERTRIMMED_DIR , filename)
                    for filename in Bar('Fixing Tags').iter(os.listdir(TRIMMED_DIR)))


Parallel(n_jobs=-1)(delayed(parse.makeCSV)(filename, SUPERTRIMMED_DIR)
                    for filename in Bar('Making CSVs').iter(os.listdir(SUPERTRIMMED_DIR)))

# collect all data frames in one list
df_container = []
for filename in Bar('Making topicModel').iter(os.listdir('../courses/')):
    df_container.append(pd.read_csv('../courses/' + filename))
# concatenate list into one joint data frame
topicModel = pd.concat(df_container)


cleaned_df = newClean(topicModel)
print("Creating '../courses/AllSchools.csv'...")
cleaned_df.to_csv('../courses/AllSchools.csv', encoding="utf-8-sig")
'''
#Previously untouched last semester Spring2020 from here down
print("\tcleaned")
vect_df = vectorizer(cleaned_df)
print("\tvect")
pruned_df = cleanVectorizer(vect_df)
print("\tpruned")
labeled_df = labelTargetsdf(pruned_df)
print("\tfound targets")
#%%
features = labeled_df.drop("curricula relevance",axis = 1).astype("bool")
labels = labeled_df["curricula relevance"]

print("Splitting Data")
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
