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
with open('../output/fullValpo.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for column in reader:
        desc.append(column[0].lower()+column[1].lower())
        courseID.append(column[0])

#Vectorize using bok.txt
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
vectorizer = CountVectorizer(vocabulary=bokVocab, ngram_range=(1, 5))
vectors = vectorizer.fit_transform(desc).toarray()
#vocab = np.array(vectorizer.get_feature_names())

#Print all "relevant" courses
count = 0
classIndex = 0
for x in vectors:
    if np.sum(x) > 0:
        print(courseID[classIndex])
        print(x)
        count = count+1
    classIndex = classIndex + 1
print(count)

#DebugPrints
#print(bokVocab)
#print(vocab)
#print(courseID[45])
#print(repr(desc[45]))
