# files in the current directory
import parse
#from topicModel import plot_10_most_common_words, listofDSCourse
from vectorize import newClean, vectorizer, cleanVectorizer, labelTargetsdf
from ML import decisionTree,visTree, randForest,undersample
#from xml_fix_utils import correct_ampersands, ignore_bad_chars

import Prep
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
Prep.prepare()


# trim the xml files (whenever line number information available, otherwise keep whole file)
Parallel(n_jobs=-1)(delayed(Prep.trimFile)(const.SOURCE_DIR, const.TRIMMED_DIR, filename, Prep.makeLineNumDict(const.TRIM_CSV))
                    for filename in Bar('Trimming Files').iter(os.listdir(const.SOURCE_DIR)))


# clean the xml files (fix problems and make it parseable)
Parallel(n_jobs=-1)(delayed(Prep.cleanXML)(const.TRIMMED_DIR , const.SUPERTRIMMED_DIR , filename)
                    for filename in Bar('Fixing Files').iter(os.listdir(const.TRIMMED_DIR)))


# make a csv from the files in temp_data/superTrimmedPDFs
Parallel(n_jobs=-1)(delayed(parse.makeCSV)(filename, const.SUPERTRIMMED_DIR, dirty) # maybe make makeCSV take an output directory?
                    for filename in Bar('Making CSVs').iter(os.listdir(const.SUPERTRIMMED_DIR)))

# collect all data frames in one list
df_container = []
for filename in Bar('Making topicModel').iter(os.listdir(const.CSV_DIR)):
    df_container.append(pd.read_csv(const.CSV_DIR + "/" + filename))
# concatenate list into one joint data frame
topicModel = pd.concat(df_container)


cleaned_df = newClean(topicModel)
print("Creating '" + const.CSV_DIR + "/" + const.ALL_CSV + "'...")
cleaned_df.to_csv(const.CSV_DIR + "/" + const.ALL_CSV, encoding="utf-8-sig")

# import createDATA
# createDATA.createCSV()

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

randForest(features, labels)
#svm(features,labels,5)
#undersample(features, labels)

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
