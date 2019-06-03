import csv
import os
import numpy as np

classes = []
names = []
#Create list of all class descriptions
with open('../output/outputValpo.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for column in reader:
        classes.append(column[0]+column[1])
        names.append(column[0])
#Vectorize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
vectorizer = CountVectorizer(stop_words='english')

count = 0
for x in classes:
    #List of wordcount
    vectors = vectorizer.fit_transform(x.split()).todense()
    #List of unique words
    vocab = np.array(vectorizer.get_feature_names())
    #print(vectors.shape)
    print(names[count])
    print(vocab[0:9742],"\n")
    count = count + 1
