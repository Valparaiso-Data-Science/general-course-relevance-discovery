
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
import string
import re
from re import *
from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from csv_combine.py import combine_csv
from get_df_name.py import get_df_name
from process_words.py import process_words
from rename_cols.py import rename_cols
from tfidf.py import tfidf
from tokenize.py import tokenize


# mount the drive module for importing data from Google Drive
#from google.colab import drive
#drive.mount('/content/drive')

# path to data directory on my drive
#data_path = '/content/drive/My Drive/TRIPODS-Student Accessible Files/Sum2020/Difficulty Protocol/Difficulty Protocol Ellie and Sydney/'

##Import CSVs as Dataframes

#load dataset
schools = pd.read_csv("AllSchools.csv")

"""
##Lemmatize and Tokenize
Groups for Stop Words:
* Verbs that are not specific to data science
* Adjectives
* Adverbs
"""

#stop words definition
stop_words = list(stopwords.words('english'))
nlp = spacy.load('en', disable=['parser', 'ner'])
stop_words.append('-PRON-')
#stop_words.extend(list(set(string.punctuation)))
#extra_verbs = []
#extra_other = ['-PRON-','cr','ul','registration']
#stop_words.extend(extra_verbs)
#stop_words.extend(extra_other)

#process words, create dictionaries for future function calls
responses, school_list = process_words(stop_words,schools)

"""##TF-IDF Calculations"""

tfidf(responses,school_list)

"""##CURRENTLY UNUSED Create Two Overall .csv files (one for each analysis)
#create combined csv for roles
old = []
old.append(pd.read_csv(data_path+"stu.csv"))
old.append(pd.read_csv(data_path+"ta.csv"))
old.append(pd.read_csv(data_path+"prof.csv"))
combine_csv("all_roles.csv",old)
#create combined csv for questions
old = []
old.append(pd.read_csv(data_path+"topics.csv"))
old.append(pd.read_csv(data_path+"struggles.csv"))
old.append(pd.read_csv(data_path+"questions.csv"))
old.append(pd.read_csv(data_path+"surprises.csv"))
combine_csv("all_questions.csv",old)
"""
