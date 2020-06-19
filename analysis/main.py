
# -*- coding: utf-8 -*-

#Import Statements

import pandas as pd
#import numpy as np
import nltk
import spacy
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('averaged_perceptron_tagger')
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
from rename_cols import rename_col
from tfidf_analysis import tfidf
from tokenizer import tokenize

nlp = spacy.load("en")

##Import CSV as Dataframes
schools = pd.read_csv("AllSchools.csv")


#stop words definition
stop_words = list(stopwords.words('english'))
nlp = spacy.load('en', disable=['parser', 'ner'])
stop_words.append('-PRON-')


#process words, create dictionaries for future function calls
responses, school_list = process_words(stop_words,schools)

#tfidf analysis
tfidf(responses,school_list)
