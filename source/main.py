# files in the current directory
from parse import parseXML, fixTags
#from topicModel import plot_10_most_common_words, listofDSCourse
from vectorize import newClean, vectorizer, cleanVectorizer, labelTargetsdf
from ML import decisionTree,visTree
from reintroduce_spaces import reintroduce_spaces
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


topicModel = pd.DataFrame()
dirty = False
if len(sys.argv) > 1 and sys.argv[1]=='dirty':
    dirty = True

try:
    os.mkdir('../source/superTrimmedPDFs')
except:
    print("../source/superTrimmedPDFs already exists")
try:
    os.mkdir('../courses')
except:
    print("../courses already exists")

for filename in os.listdir('../source/TRIMMED'):
    fixTags(filename)

for filename in os.listdir('../source/superTrimmedPDFs'):
    #Checks if we are looking at a college we know needs WordNinja
    wn_colleges = ['Brown','Carlow','Caldwell','Denison']
    for college in wn_colleges:
        if re.match(college,filename) is not None:
            needsWN = True
            break
        else:
            needsWN = False
    #Checks if the college needs Word Ninja
    if needsWN:
        #Pass the super trimmed XML into Word Ninja
        try:
            reintroduce_spaces('../source/superTrimmedPDFs/' + filename)
        except:
            filepath = '../source/superTrimmedPDFs/'+filename
            os.system('python3 ignore_nonutf.py '+ filepath)
            os.system('python3 correct_ampersand.py '+ filepath)
            reintroduce_spaces(filepath)
        #Delete the old, not Word Ninja-ed file
        if not dirty:
            print('Now deleting: ../source/superTrimmedPDFs/'+ filename)
            os.remove('../source/superTrimmedPDFs/'+filename)
    if needsWN:
        filename = filename.replace('SUPERTRIMMED','SUPERTRIMMED_spaced')
        CSV = parseXML("../source/superTrimmedPDFs/"+filename, 'P', 'P', 1)
        CSV.to_csv("../courses/"+filename.replace("xml","csv"), encoding="utf-8-sig")
    else:
        CSV = parseXML("../source/superTrimmedPDFs/"+filename, 'P', 'P', 1)
        CSV.to_csv("../courses/"+filename.replace("xml","csv"), encoding="utf-8-sig")
    topicModel= pd.concat([topicModel,CSV])


cleaned_df = newClean(topicModel)
cleaned_df.to_csv('../courses/AllSchools.csv',encoding="utf-8-sig")
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