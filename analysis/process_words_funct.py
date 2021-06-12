import pandas as pd
import nltk
import spacy
import string
import re
from re import *
from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tokenizer import tokenize
from get_df_name_func import get_df_name

nlp = spacy.load('en_core_web_sm')
def process_words(stops,df):
  og_dict = {} #dictionary of full responses
  responses = {} #dictionary of processed responses
  school = df['School'][0] #assign first school to variable
  og_dict[school] = [] #declare original dictionary
  i=0
  for s in df['School']: #for each school in the dataframe
    if s == school: #if the school is the current being run on
      r = df['Descriptions'][i] #description string
      og_dict[school].append(r) #append description to dictionary
      i+=1
    else: #change school to current school
      school = s
      og_dict[school] = []
      r = df['Descriptions'][i] #description string
      og_dict[school].append(r) #append description to dictionary
      i+=1

  for s in list(og_dict.keys()): #for each school
    temp_list = tokenize(og_dict[s]) #tokenize descriptions
    responses[s] = []
    for lst in temp_list: #for each description
      lst = ' '.join(lst)
      wr_string = lst.lower()
      doc = nlp(wr_string)
      new_sent = " ".join([token.lemma_ for token in doc]) #lemmatize words
      new_sent = new_sent.split()
      new_sent = [re.sub('\d+', '', word) for word in new_sent] #remove digits
      new_sent = [word for word in new_sent if word not in stops] #removed stopwords
      new_sent = ' '.join(new_sent) #completely processed description as string
      responses[s].append(new_sent) #add processed sentence
  return responses, list(og_dict.keys()) #returns processeed response dictionary & school names
