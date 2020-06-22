
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
#import re
#from re import *
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

#read in body of knowledge txt file, convert to list
text_file = open("edison.txt", "r")
bok = text_file.read().split('\n')
for i in range(len(bok)):
  bok[i] = bok[i].lower()



#retain only courses pertinent to Data Science
fake_df = []
for i in range(len(schools)):
  des = schools['Descriptions'][i]
  des = des.lower()
  fake_list = []
  for w in bok:
    if w in des:
      fake_list = [schools['School'][i], schools['CourseID'][i], schools['Descriptions'][i]]
      fake_df.append(fake_list)
      break
new_schools = pd.DataFrame(fake_df)
new_schools.columns = ['School','CourseID','Descriptions']
path_name = 'TFIDF_all' +'.csv'
new_schools.to_csv(data_path + 'Analysis Data/bok_courses.csv') #save all pertinent courses to csv

#stop words definition
stop_words = list(stopwords.words('english'))
nlp = spacy.load('en', disable=['parser', 'ner'])
stop_words.append('-PRON-')


#process words, create dictionaries for future function calls
responses, school_list = process_words(stop_words,new_schools)

#tfidf analysis
tfidf(responses,school_list)
