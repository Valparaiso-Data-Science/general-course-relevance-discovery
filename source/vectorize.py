import csv
import os
import numpy as np
import sys
#np.set_printoptions(threshold=sys.maxsize)

#Grab vocab into a list
bokVocab = [line.rstrip('\n').lower() for line in open('../bok.txt')]
desc = []
courseID = []

#Create list of all class descriptions and course IDs
with open('../output/outputValpo.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for column in reader:
        desc.append(column[0]+column[1])
        courseID.append(column[0])

#Vectorize using bok.txt
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
vectorizer = CountVectorizer( vocabulary=bokVocab)
vectors = vectorizer.fit_transform(desc).toarray()
vocab = np.array(vectorizer.get_feature_names())
count = 0
classIndex = 0

#Print all "relevant" courses
for x in vectors:
    if np.sum(line) > 0:
        print(courseID[classIndex])
        print(x)
        count = count+1
    classIndex = classIndex + 1
print(count)
