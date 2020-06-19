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
from process_words.py import process_words
from rename_cols.py import rename_cols
from tfidf.py import tfidf
from tokenize.py import tokenize

def get_df_name(df):
    name =[x for x in globals() if globals()[x] is df][0]
    return name
