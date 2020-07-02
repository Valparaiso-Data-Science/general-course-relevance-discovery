# files in the current directory
from parse import parseXML, fixTags, trimFile
#from topicModel import plot_10_most_common_words, listofDSCourse
from vectorize import newClean, vectorizer, cleanVectorizer, labelTargetsdf
from ML import decisionTree,visTree
from reintroduce_spaces import reintroduce_spaces
from xml_fix_utils import correct_ampersands, ignore_bad_chars

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
source_dir = "../fullPDFs"
trimmed_dir = "../temp_data/TRIMMED"
supertrimmed_dir = "../temp_data/superTrimmedPDFs"

# toggle for keeping data from intermediary stages
dirty = False
if len(sys.argv) > 1 and sys.argv[1] == 'dirty':
    dirty = True

def prepare():
    # make directories for intermediary and final data
    print("Preparing temporary data directory...")
    try:
        os.mkdir('../temp_data')
    except FileExistsError:
        print("../temp_data already exists")
    try:
        os.mkdir('../temp_data/superTrimmedPDFs')
    except FileExistsError:
        print("../temp_data/superTrimmedPDFs already exists. Clearing all files in it.")
        # clear folder of previous files
        if len(os.listdir('../temp_data/superTrimmedPDFs')) > 0:
            for file in Bar("Cleaning supertrimmmed...").iter(os.listdir('../temp_data/superTrimmedPDFs')):
                os.unlink('../temp_data/superTrimmedPDFs/' + file)
    try:
        os.mkdir('../courses')
    except FileExistsError:
        print("../courses already exists. Clearing all files in it.")

        # clear folder of previous files
        if len(os.listdir('../courses')) > 0:
            for file in Bar("Cleaning courses...").iter(os.listdir('../courses')):
                os.unlink('../courses/' + file)
prepare()


# look for a csv file containing line number information (from which line to which line to trim) and gather the relevant
#   information (filename, start line, end line) in a dictionary
line_num_dict = {}
try:
    cat_df = pd.read_csv("../Catalogs.csv")

    for index, row in cat_df.iterrows():
        if (not np.isnan(row[1])) and (not np.isnan(row[2])):
            line_num_dict[row[0].lower()] = int(row[1]), int(row[2])

except FileNotFoundError:
    print("CSV file with trimming line numbers not found.")

# trim file (whenever line number information available, otherwise keep whole file)
Parallel(n_jobs=-1)(delayed(trimFile)(source_dir, trimmed_dir, filename, line_num_dict)
                    for filename in Bar('Trimming Files').iter(os.listdir(source_dir)))



Parallel(n_jobs=-1)(delayed(fixTags)(trimmed_dir , supertrimmed_dir , filename)
                    for filename in Bar('Fixing Tags').iter(os.listdir(trimmed_dir)))


def makeCSV(filename):

    # indicate that we used `supertrimmed_dir` variable as defined at the top of the file
    global supertrimmed_dir

    #Checks if we are looking at a college we know needs WordNinja
    wn_colleges = ['Brown', '2011Cornell', 'Carlow', 'Caldwell', 'Denison', 'Pittsburgh'] # 'Youngstown']

    for college in wn_colleges:
        if re.match(college,filename) is not None:
            needsWN = True
            break
        else:
            needsWN = False

    #Checks if the college needs Word Ninja
    if needsWN:
        deletable = filename

        # reintroduce spaces and reassign `filename` to cleaned file
        filename = reintroduce_spaces(supertrimmed_dir + "/" + filename)
        filename = filename[filename.rfind("/") + 1:]  # chop off the directory path, only leave name filename

        if not dirty:
            print("\nNow deleting:", deletable)
            os.unlink(supertrimmed_dir + "/" + deletable)

    # use parseXML to find course headers and descriptions
    CSV = parseXML(supertrimmed_dir + "/" + filename, 'P', 'P', 1)
    CSV.to_csv("../courses/"+filename.replace("xml","csv"), encoding="utf-8-sig")

Parallel(n_jobs=-1)(delayed(makeCSV)(filename) for filename in Bar('Making CSVs').iter(os.listdir(supertrimmed_dir)))

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
