
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
schools = pd.read_csv("AllSchools_updatedWordNinja.csv")
del(schools['Unnamed: 0'])
valpo = pd.read_csv("valpo-6-23-2020-spacing-fixed.csv",header=None)
del(valpo[0])
valpo.columns = ['School', 'CourseID', 'Descriptions']
schools = schools.append(valpo,ignore_index=True)

#read in body of knowledge txt file, convert to list
text_file = open("edison.txt", "r")
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
print("Creating '../csvs/bok_courses.csv'...")
new_schools.to_csv('../csvs/bok_courses.csv',encoding="utf-8-sig")

#creating new columns with key words
body = ['Data Science Analytics','Data Science Engineering','Data Management','Research Methods and Project Management','Business Analytics']
dsana = ['accuracy metrics','data analytics','data analysis','data analytics assessment',
         'data lifecycle','data mining','data preparation','graph data analytics',
         'machine learning','natural language processing','open data','operations research',
         'optimisation','optimization','predictive analytics','prescriptive analytics',
         'qualitative analytics','reinforced learning','simulation']
dseng = ['big data infrastructures','cloud computing','cloud powered services',
         'collaborative system','continuous improvement cycle','data access',
         'data anonymisation','data driven','data handling','data lifecycle',
         'data science engineering','data security','data warehouse solution',
         'devops','dmp','engineering principles','etl','extract transform load',
         'federated access control','ipr protection','nosql','olap','oltp',
         'relational databases','simulation','sql','systems software']
dman = ['data architecture','data archive services','data curation','data factories',
        'data formats','data governance strategy','data handling','data integration',
        'data lifecycle','data management','data management plan','data modeling',
        'data modeling design','data provenance','data registries','data storage systems',
        'data types','digital libraries','etl','extract transform load','linked data',
        'meta data','metadata','meta-data','olap','oltp','open access','open data',
        'open science','operational models','pid']
remeprma = ['data collection','data driven','data lifecycle','data quality evaluation',
            'project management','quality evaluation','research methods','team management',
            'use cases analysis']
busana = ['agile data driven','bpm','business analytics','business intelligence',
          'cognitive technologies','crp','customer relations management',
          'data marketing technologies','data driven marketing','data integration analytics',
          'data warehouses technologies','econometrics','enterprises','open data',
          'optimization','processes management','use cases analysis','user experience','ux']
bok_cats = {}
bodies = []
bodies.append(dsana)
bodies.append(dseng)
bodies.append(dman)
bodies.append(remeprma)
bodies.append(busana)
i=0
for i in range(len(body)):
  bok_cats[body[i]] = bodies[i]
print(bok_cats)


ellie = ['Website','Data Visualization','Statistics','Experimental Design','Programming','Algorithms/Modeling/AI','Data Collection','Data Sources','Data Types','Data Analysis','Application','Simulation','Software','Lab']
website = ['information technology','web design','website','network','webpage','web',
           'shiny']
datavis = ['graph','graphs','chart','charts','color theory','barplot','bar plot','visualization',
           'visualisation','visualizations','visual','visuals','box plot','boxplot',
           'color','colors','ggplot2','dashboard','boxplot','barplot','pie chart','piechart','tableau']
statistics = ['anova','linear regression','chi squared','probability',
              'hypothesis test','regression','statistics','statistic','distribution',
              'variability','variance','percentile','standard deviation','mean',
              'median','mode','average','trendline','trend line']
resmeth = ['research methods','research','research process','design of experiment',
           'design of experiments','research question','design study','design studies',
           'research design']
proglang = ['r','python','c++','mysql','c','spss','sql','nosql','programming language',
            'programming languages','tools','sas','programming','pandas','package',
            'library','coding','code']
algmodai = ['artificial intelligence','ai','algorithm','algorithms','model','models','modeling',
            'machine learning','predict','natural language processing','nlp',
            'topic model','supervised learning','unsupervised learning',
            'neural network','k-means cluster','clustering','decision tree']
collect = ['data collection','collect','sample size','raw data','collection','collections']
sources = ['data source','data sources','retrieve','database','databases','import']
types = ['medicalpharmecutical','qualitative','quantitative','econometrics',
         'public health','big data','large volumes']
anal = ['data analysis','analyze data','analysis','summary','summarize','summarizing']
applic = ['communication','results','interpretation','application',
          'data representation','presentation']
sim = ['simulation','simulations']
software = ['software','github','rstudio','excel','microsoft','gis','colab','jupyter',
            'tableau']
lab = ['lab','labs','laboratory']
ellie_cats = {}
ellies = []
ellies.append(website)
ellies.append(datavis)
ellies.append(statistics)
ellies.append(resmeth)
ellies.append(proglang)
ellies.append(algmodai)
ellies.append(collect)
ellies.append(sources)
ellies.append(types)
ellies.append(anal)
ellies.append(applic)
ellies.append(sim)
ellies.append(software)
ellies.append(lab)
i=0
for i in range(len(ellie)):
  ellie_cats[ellie[i]] = ellies[i]
print(ellie_cats)

#adding keywords to columns
for b in body:
  new_schools[b] = 0
for e in ellie:
  new_schools[e] = 0

j=0
for j in range(len(new_schools)):
  for b in bok_cats:
    i = 0
    for i in range(len(bok_cats[b])):
      comp = str(new_schools['Descriptions'][j]).lower()
      if re.search('\s'+re.escape(bok_cats[b][i])+'\s',comp):
        new_schools[b][j] = 1

  for e in ellie_cats:
    i = 0
    for i in range(len(ellie_cats[e])):
      comp = str(new_schools['Descriptions'][j]).lower()
      if re.search('\s'+re.escape(ellie_cats[e][i])+'\s',comp):
        new_schools[e][j] = 1
print("Creating '../csvs/bok_courses_cat_ellie.csv'...")
new_schools.to_csv('../csvs/bok_courses_cat_ellie.csv',index=False)


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
