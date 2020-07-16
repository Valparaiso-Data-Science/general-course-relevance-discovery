"""
--Do we need this file?--

"""

from sklearn.model_selection import train_test_split
from sklearn import tree,metrics
from sklearn.tree.export import export_text
from sklearn.tree import export_graphviz
import seaborn as sns
sns.set_style('whitegrid')
import pandas as pd

def listofDSCourse(df):
    DSCourses_df =[]
    courseID = []
    schoolID = []
    vocab = [line.rstrip('\n').lower() for line in open('../bok.txt')]
    for CourseID, desc, school in zip(df['CourseID'],df['Descriptions'],df['School']):
        #Could also check if courseID has an edison body word (like Data 101)
        if any(item in desc for item in vocab):
            courseID.append(CourseID)
            DSCourses_df.append(desc)
            schoolID.append(school)
    DS_df=pd.DataFrame(list(zip(schoolID, courseID, DSCourses_df)),columns =['School','CourseID','Descriptions'])
    return(DS_df)

# Helper function
def plot_10_most_common_words(count_data, count_vectorizer):
    import matplotlib.pyplot as plt
    import numpy as np
    words = count_vectorizer.get_feature_names()
    total_counts = np.zeros(len(words))
    for t in count_data:
        total_counts += t.toarray()[0]

    count_dict = (zip(words, total_counts))
    count_dict = sorted(count_dict, key=lambda x: x[1], reverse=True)[0:15]
    words = [w[0] for w in count_dict]
    counts = [w[1] for w in count_dict]
    x_pos = np.arange(len(words))

    plt.figure(2, figsize=(15, 15 / 1.6180))
    plt.subplot(title='10 most common words')
    sns.set_context("notebook", font_scale=1.25, rc={"lines.linewidth": 2.5})
    sns.barplot(x_pos, counts, palette='husl')
    plt.xticks(x_pos, words, rotation=90)
    plt.xlabel('words')
    plt.ylabel('counts')
    plt.show()
