# files in the current directory
from parse import parseXML, fixTags
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
        for file in os.listdir('../temp_data/superTrimmedPDFs'):
            os.unlink('../temp_data/superTrimmedPDFs/' + file)
    try:
        os.mkdir('../courses')
    except FileExistsError:
        print("../courses already exists. Clearing all files in it.")

        # clear folder of previous files
        for file in os.listdir('../courses'):
            os.unlink('../courses/' + file)
prepare()

# make trimmed files
try:
    os.system("bash ../pre/fileTrimmer.sh ../Catalogs.csv ../fullPDFs ../temp_data/TRIMMED")
except:
    print("Filetrimming step failed, we'll get em next time.")
    quit()


Parallel(n_jobs=-1)(delayed(fixTags)(trimmed_dir , supertrimmed_dir , filename)
                    for filename in Bar('Fixing Tags').iter(os.listdir(trimmed_dir)))


def makeCSV(filename):

    # indicate that we used `supertrimmed_dir` variable as defined at the top of the file
    global supertrimmed_dir

    #Checks if we are looking at a college we know needs WordNinja
    wn_colleges = ['Brown', '2011Cornell', 'Carlow', 'Caldwell', 'Denison', 'Pittsburgh', 'Youngstown']
    
    for college in wn_colleges:
        if re.match(college,filename) is not None:
            needsWN = True
            break
        else:
            needsWN = False
    #Checks if the college needs Word Ninja
    if needsWN:
        # container of intermediary data files for potential deletion
        deletable_filenames = []

        #Pass the super trimmed XML into Word Ninja
        try:
            # save current name for potential deletion later
            deletable = filename

            # reintroduce spaces and reassign `filename` to cleaned file
            filename = reintroduce_spaces(supertrimmed_dir + "/" + filename)
            filename = filename[filename.rfind("/")+1:]  # chop off the directory path, only leave name filename

            deletable_filenames.append(deletable)

        except xml.etree.ElementTree.ParseError:
            # save current name for potential deletion later
            deletable = filename

            # clean bad characters (so far only utf 65535) and reassign `filename` to cleaned file
            filename = ignore_bad_chars(supertrimmed_dir + "/" + filename)
            filename = filename[filename.rfind("/")+1:]  # chop off the directory path, only leave name filename
            deletable_filenames.append(deletable)


            # save current name for potential deletion later
            deletable = filename

            # correct bad apersands if any (replace `&` with `&amp;`) and reassign `filename` to cleaned file
            filename = correct_ampersands(supertrimmed_dir + "/" + filename)
            filename = filename[filename.rfind("/")+1:]  # chop off the directory path, only leave name filename
            deletable_filenames.append(deletable)

            # save current name for potential deletion later
            deletable = filename

            # correct spaces and reassign `filename` to cleaned file
            filename = reintroduce_spaces(supertrimmed_dir + "/" + filename)
            filename = filename[filename.rfind("/")+1:]  # chop off the directory path, only leave name filename
            deletable_filenames.append(deletable)

        #Delete the old, not Word Ninja-ed file(s)
        if not dirty:
            # print the whole list of deletable filenames
            print(f'\nNow deleting: {*deletable_filenames,}')

            for item in deletable_filenames:
                os.remove(supertrimmed_dir + "/" + item)

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
