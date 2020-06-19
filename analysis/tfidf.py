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
from get_df_name.py import get_df_name

def tfidf(dictionary, schools):
  nlp = spacy.load("en")
  answers = dictionary
  overall_denom = 0
  #TF-IDF FOR EACH INDIVIDUAL SCHOOL
  #TERM = WORD/BIGRAM, DOCUMENT = DESCRIPTION, CORPUS = ALL DESCRIPTIONS FROM ONE SCHOOL
  corpus = []
  #for school in schools:
    #doc_string = ' '.join(dictionary[school])
    #corpus.append(doc_string)
  for school in schools:
    print("School: %s -----------------" % school)
    corpus=dictionary[school]
    #code from https://www.geeksforgeeks.org/tf-idf-for-bigrams-trigrams/
    #GETTING BIGRAMS
    vectorizer = CountVectorizer(ngram_range = (1,1))
    X1 = vectorizer.fit_transform(corpus)
    features = (vectorizer.get_feature_names())

    # Applying TFIDF
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(corpus)
    scores = (vectors.toarray())
    # Getting top ranking features
    sums = vectors.sum(axis = 0)
    data1 = []
    for col, term in enumerate(features):
        data1.append( (term, sums[0,col] ))
    ranking = pd.DataFrame(data1, columns = ['term','rank'])
    words = (ranking.sort_values('rank', ascending = False))
    words = words[:10]

    #Getting frequency counts
    freq_list = []
    list_bigram = list(words['term'])
    i = 0
    while i < 10:
      bigram = str(list_bigram[i]).split()
      f_word = str(bigram[0])
      #s_word = str(bigram[1]) -- add if bigram
      regex = re.escape(f_word) #+ r" " + re.escape(s_word) -- add if bigram
      count = 0
      for doc in corpus:
        iterator = finditer(regex, doc)
        for match in iterator:
          count+=1
      app = str(count)
      freq_list.append(app)
      i+=1
    words['frequency'] = freq_list
    denom = len(dictionary[school])
    overall_denom += denom
    words ['overall'] = str(denom)
    words = words[['term','frequency','overall','rank']]
    print('\n',words)
    print("\n---------------------------\n")



#TF-IDF FOR ALL SCHOOLS COMBINED
#TERMS = WORD/BIGRAM, DOCUMENT = EACH SCHOOL'S CATALOG, CORPUS = ALL CATALOGS
  print("All Schools: -----------------")
  corpus = []
  for school in schools:
    doc_string = ' '.join(dictionary[school])
    corpus.append(doc_string)

  #code from https://www.geeksforgeeks.org/tf-idf-for-bigrams-trigrams/
  #GETTING BIGRAMS
  vectorizer = CountVectorizer(ngram_range = (1,1))
  X1 = vectorizer.fit_transform(corpus)
  features = (vectorizer.get_feature_names())

  # Applying TFIDF
  vectorizer = TfidfVectorizer()
  vectors = vectorizer.fit_transform(corpus)
  scores = (vectors.toarray())
  # Getting top ranking features
  sums = vectors.sum(axis = 0)
  data1 = []
  for col, term in enumerate(features):
      data1.append( (term, sums[0,col] ))
  ranking = pd.DataFrame(data1, columns = ['term','rank'])
  words = (ranking.sort_values('rank', ascending = False))
  words = words[:10]

  #Getting frequency counts
  freq_list = []
  list_bigram = list(words['term'])
  i = 0
  while i < 10:
    bigram = str(list_bigram[i]).split()
    f_word = str(bigram[0])
    #s_word = str(bigram[1])
    regex = re.escape(f_word) #+ r" " + re.escape(s_word)
    count = 0
    for doc in corpus:
      iterator = finditer(regex, doc)
      for match in iterator:
        count+=1
    app = str(count)
    freq_list.append(app)
    i+=1
  words['frequency'] = freq_list
  denom = overall_denom
  words ['overall'] = str(denom)
  words = words[['term','frequency','overall','rank']]
  print('\n',words)
  print("\n---------------------------\n")

    #saving dataframe to csv
    path_name = 'TFIDF_' + school +'.csv'
    words.to_csv(path_name)
