
# -*- coding: utf-8 -*-

#Import Statements

import pandas as pd
#import numpy as np
import nltk
import spacy
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
#import string
import re
from re import *
#from nltk.util import ngrams
from nltk.corpus import stopwords
#from nltk.tokenize import word_tokenize
#from nltk.stem import WordNetLemmatizer
#from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from get_df_name_func import get_df_name
from process_words_funct import process_words
from tfidf_analysis import tfidf
from tokenizer import tokenize

nlp = spacy.load("en")

##Import CSV as Dataframes
schools = pd.read_csv("AllSchools.csv")
del(schools['Unnamed: 0'])
valpo = pd.read_csv("valpo-6-23-2020-spacing-fixed.csv",header=None)
del(valpo[0])
valpo.columns = ['School', 'CourseID', 'Descriptions']
schools = schools.append(valpo,ignore_index=True)

#read in body of knowledge txt file, convert to list
text_file = open(data_path + "edison.txt", "r")
bok = text_file.read().split('\n')
for i in range(len(bok)):
  bok[i] = bok[i].lower()



#retain only courses pertinent to Data Science
fake_df = []
for i in range(len(schools)):
  des = str(schools['Descriptions'][i])
  des = des.lower()
  fake_list = []
  terms = []
  print(i)
  for w in bok:
    pattern = r'\s'
    if re.search(pattern+w+pattern,des):
      if w not in terms:
        terms.append(w)
  if len(terms) != 0:
    fake_list = [schools['School'][i], schools['CourseID'][i], schools['Descriptions'][i],', '.join(terms)]
    fake_df.append(fake_list)
new_schools = pd.DataFrame(fake_df)
new_schools.columns = ['School','CourseID','Descriptions','Data Science Term']
path_name = 'TFIDF_all' +'.csv'
new_schools.to_csv(data_path + 'Analysis Data/bok_courses.csv')

#stop words definition
stop_words = list(stopwords.words('english'))
nlp = spacy.load('en', disable=['parser', 'ner'])
stop_words.append('-PRON-')
#find way to remove all numbers
first_stops = ['cr','ul']

stop_words.extend(first_stops)

#process words, create dictionaries for future function calls
responses, school_list = process_words(stop_words,new_schools)

#tfidf analysis
tfidf(responses,school_list)
