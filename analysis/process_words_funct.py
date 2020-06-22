import pandas as pd
#import numpy as np
import nltk
import spacy
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('averaged_perceptron_tagger')
import string
#import re
#from re import *
from nltk.util import ngrams
from nltk.corpus import stopwords
#from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
#from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from tokenizer import tokenize
from get_df_name_func import get_df_name

nlp = spacy.load("en")
def process_words(stops,df):
  og_dict = {} #dictionary of full responses
  responses = {} #dictionary of processed responses
  school = df['School'][0]
  og_dict[school] = []
  i=0
  for s in df['School']:
    if s == school:
      r = df['Descriptions'][i] #description string
      og_dict[school].append(r)
      i+=1
    else:
      school = s
      og_dict[school] = []
      r = df['Descriptions'][i] #description string
      og_dict[school].append(r)
      i+=1

  for s in list(og_dict.keys()):
    temp_list = tokenize(og_dict[s])
    responses[s] = []
    for lst in temp_list:
      lst = ' '.join(lst)
      wr_string = lst.lower()
      doc = nlp(wr_string)
      new_sent = " ".join([token.lemma_ for token in doc])
      new_sent = new_sent.split()
      new_sent = [word for word in new_sent if word not in stops]
      new_sent = [re.sub('\d+', '', word) for word in new_sent] #remove all numbers
      new_sent = ' '.join(new_sent) #completely processed sentence as string
      responses[s].append(new_sent)
  return responses, list(og_dict.keys()) #returns processeed response dictionary & school names
