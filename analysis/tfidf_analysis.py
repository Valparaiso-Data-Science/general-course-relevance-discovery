import pandas as pd
import nltk
import spacy
import string
import re
from re import *
from nltk.util import ngrams
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from get_df_name_func import get_df_name

nlp = spacy.load('en_core_web_sm')
def tfidf(dictionary, schools):
  answers = dictionary
  overall_denom = 0
  #TF-IDF FOR EACH INDIVIDUAL SCHOOL
  #TERM = WORD/BIGRAM, DOCUMENT = DESCRIPTION, CORPUS = ALL DESCRIPTIONS FROM ONE SCHOOL
  corpus = []
  for school in schools: #for each school
    print("School: %s -----------------" % school)
    corpus=dictionary[school]
    #code from https://www.geeksforgeeks.org/tf-idf-for-bigrams-trigrams/
    #GETTING BIGRAMS
    vectorizer = CountVectorizer(ngram_range = (2,2)) #create bigrams
    X1 = vectorizer.fit_transform(corpus)
    features = (vectorizer.get_feature_names())
    i = len(features) - 1
    while i >= 0: #remove bigrams that are the same word twice
      bi = features[i].split()
      if bi[0] == bi[1]:
        del(features[i])
      i -= 1

    # Applying TFIDF
    vectorizer = TfidfVectorizer(ngram_range = (2,2)) #create tfidf of bigrams
    vectors = vectorizer.fit_transform(corpus)
    scores = (vectors.toarray())
    # Getting top ranking features
    sums = vectors.sum(axis = 0)
    data1 = []
    for col, term in enumerate(features):
        data1.append( (term, sums[0,col] )) #append bigram and tfidf weight to list
    ranking = pd.DataFrame(data1, columns = ['term','rank']) #append list to datframe
    words = (ranking.sort_values('rank', ascending = False)) #sort by weight
    words = words[:10] #keep only top 10 bigrams

    #Getting frequency counts
    freq_list = []
    list_bigram = list(words['term'])
    i = 0
    while i < 10: #loop through all 10 bigrams
      bigram = str(list_bigram[i]).split()
      f_word = str(bigram[0]) #first word in bigram
      s_word = str(bigram[1]) #second word in bigram
      regex = re.escape(f_word) + r"\w*\s+" + re.escape(s_word) #regex for "firstword space secondword"
      count = 0
      for doc in corpus: #for each document
        iterator = finditer(regex, doc) #count how many times bigram appears
        for match in iterator:
          count+=1
      app = str(count)
      freq_list.append(app) #add count to list
      i+=1
    words['frequency'] = freq_list #add list to dataframe
    denom = len(dictionary[school]) #create denominator column
    overall_denom += denom
    words ['overall'] = str(denom) #add denominator to dataframe 
    words = words[['term','frequency','overall','rank']] #reorganize dataframe
    print('\n',words)
    print("\n---------------------------\n")

    #saving dataframe to csv
    print("Creating 'csvs/SMITH_TFIDF_"+school+".csv'...")
    path_name = 'csvs/SMITH_TFIDF_' + school +'.csv'
    words.to_csv(path_name,encoding="utf-8-sig")

#TF-IDF FOR ALL SCHOOLS COMBINED
#TERMS = WORD/BIGRAM, DOCUMENT = EACH SCHOOL'S CATALOG, CORPUS = ALL CATALOGS
#same process as above with differing documents/corpus
  print("All Schools: -----------------")
  corpus = []
  for school in schools:
    doc_string = ' '.join(dictionary[school])
    corpus.append(doc_string)

  #code from https://www.geeksforgeeks.org/tf-idf-for-bigrams-trigrams/
  #GETTING BIGRAMS
  vectorizer = CountVectorizer(ngram_range = (2,2))
  X1 = vectorizer.fit_transform(corpus)
  features = (vectorizer.get_feature_names())
  i = len(features) - 1
  while i >= 0:
    bi = features[i].split()
    if bi[0] == bi[1]:
      del(features[i])
    i -= 1

  # Applying TFIDF
  vectorizer = TfidfVectorizer(ngram_range = (2,2))
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
    s_word = str(bigram[1])
    regex = re.escape(f_word) + r" " + re.escape(s_word)
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
  print("Creating 'csvs/SMITH_TFIDF_all.csv'...")
  words.to_csv('csvs/SMITH_TFIDF_all.csv',encoding="utf-8-sig")
