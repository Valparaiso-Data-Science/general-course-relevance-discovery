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
from tfidf.py import tfidf
from tokenize.py import tokenize

def rename_col(csv, og_name, new_name):
    csv.rename(columns={og_name:new_name},inplace=True)
