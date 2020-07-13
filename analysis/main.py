
# -*- coding: utf-8 -*-

#Import Statements

import pandas as pd
import numpy as np
import nltk
import spacy
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
import re
from re import *
from nltk.corpus import stopwords
!pip install gower
import gower
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
from get_df_name_func import get_df_name
from process_words_funct import process_words
from tfidf_analysis import tfidf
from tokenizer import tokenize

nlp = spacy.load("en")

##Import CSV as Dataframes
schools = pd.read_csv("AllSchools-07-10-2020-FROZEN.csv")
del(schools['Unnamed: 0'])

#read in body of knowledge txt file, convert to list
text_file = open("edison.txt", "r")
bok = text_file.read().split('\n')
for i in range(len(bok)):
  bok[i] = bok[i].lower()

#retain only courses pertinent to Data Science
temp_df = []
for i in range(len(schools_df)):
  des = str(schools_df['Descriptions'][i])
  des = des.lower()
  temp_list = []
  terms = []
  print(i)
  for w in bok:
    pattern = r'\s'
    if re.search(pattern+w+pattern,des):
      if w not in terms:
        terms.append(w)
  if len(terms) != 0:
    temp_list = [schools_df['School'][i], schools_df['CourseID'][i], schools_df['Descriptions'][i],', '.join(terms)]
    temp_df.append(temp_list)
ds_schools_df = pd.DataFrame(temp_df)
ds_schools_df.columns = ['School','CourseID','Descriptions','Data Science Term']
print("Creating 'csvs/0713_bok_courses.csv'...")
ds_schools_df.to_csv('csvs/0713_bok_courses.csv',enconding="utf-8-sig")

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

#adding keywords to columns
for b in body:
  ds_schools_df[b] = 0
for e in ellie:
  ds_schools_df[e] = 0

j=0
for j in range(len(ds_schools_df)):
  for b in bok_cats:
    i = 0
    for i in range(len(bok_cats[b])):
      comp = str(ds_schools_df['Descriptions'][j]).lower()
      if re.search('\s'+re.escape(bok_cats[b][i])+'\s',comp):
        ds_schools_df[b][j] = 1

  for e in ellie_cats:
    i = 0
    for i in range(len(ellie_cats[e])):
      comp = str(ds_schools_df['Descriptions'][j]).lower()
      if re.search('\s'+re.escape(ellie_cats[e][i])+'\s',comp):
        ds_schools_df[e][j] = 1

#creating summation column
ds_schools_df['Sum'] = ds_schools_df.sum(axis=1)

#creating weights
num = 0
denom = 1
frac = float(num/denom)

#create "others" list with all keywords
others = website
others.extend(datavis)
others.extend(statistics)
others.extend(resmeth)
others.extend(proglang)
others.extend(algmodai)
others.extend(collect)
others.extend(sources)
others.extend(types)
others.extend(anal)
others.extend(applic)
others.extend(sim)
others.extend(software)
others.extend(lab)
others = list(set(others))
others.sort()

#remove items from "others" already in "bok"
i = len(others) - 1
while i >=0:
  if others[i] in bok:
    del others[i]
  i -=1


#stop words definition
stop_words = list(stopwords.words('english'))
nlp = spacy.load('en', disable=['parser', 'ner'])
stop_words.append('-PRON-')
#find way to remove all numbers
first_stops = ['cr','ul','ii','cog','pp','ps','geog','cosc','biol','el','sesp',
               'eecs','oba','phys','phy','mth','cmsc','nur','ce','cs','iii'] #unkown/unnecessary abbreviations
second_stops = ['make','impact','apply','change','involve','reside','vary','may',
                'meet','use','include','pertain','tell','cover','devote',
                'recognize','carry'] #verbs that are not useful
third_stops = ['new','minimum','useful','mainly','large','liberal','formerly',
               'especially','absolutely','graduate','odd','one','throughout',
               'weekly','least','well','hour','common','require','along','least',
               'long','related','prior','open','sophomore','junior','single',
               'necessary'] #unuseful descriptors
fourth_stops = ['treat','prereq','prerequisite','creditsprerequisite',
                'corequisite','either','assignment','major','none','arts','core',
                'andor','semester','hoursprereq','student','instructor','threehour',
                'within','lecturescover','satisfactoryno','summer','yifat',
                'givenfor','term','classroom','area','inquiry','researchintensive',
                'year','via','teacher','ofhow'] #other unuseful words
stop_words.extend(first_stops)
stop_words.extend(second_stops)
stop_words.extend(third_stops)
stop_words.extend(fourth_stops)

#remove stopwords from df:
for i in range(len(ds_schools_df)): # for each row
  des = ds_schools_df.loc[i,'Descriptions'].split()
  j = len(des) - 1
  while j >=0:
    if des[j] in stop_words:
      del des[j]
    j-=1
  ds_schools_df.loc[i,'Descriptions'] = ' '.join(des)

#create weights
ds_schools_df["Weights"] = 0
for i in range(len(ds_schools_df)): #for each row
  print(i)
  num = 0
  d = ds_schools_df['Descriptions'][i]
  d = d.split() #split for word count
  denom = len(d) #overall word count
  for b in bok: #for each BoK term
    b = b.split() #split for word count
    b_len = len(b) #num of words in BoK term
    b = ' '.join(b) #join for analysis
    d = ' '.join(d).lower() #join for analysis
    token = nltk.word_tokenize(d) #tokenize for ngrams
    ngram = list(ngrams(token,b_len)) #create ngrams
    for n in range(len(ngram)): #turn tuples to strings
      ngram[n] = ' '.join(ngram[n])
    num += (ngram.count(b) * b_len)
    d = d.split() #split for continuity
  for b in others: #for each "others" term
    b = b.split() #split for word count
    b_len = len(b) #num of words in "others" term
    b = ' '.join(b) #join for analysis
    d = ' '.join(d) #join for analysis
    token = nltk.word_tokenize(d) #tokenize for ngrams
    ngram = list(ngrams(token,b_len)) #create ngrams
    for n in range(len(ngram)): #turn tuples to strings
      ngram[n] = ' '.join(ngram[n])
    num += (ngram.count(b) * 0.5)
    d = d.split() #split for continuity
  frac = float(num/denom)
  ds_schools_df.loc[i, 'Weights'] = frac
  print("Creating 'csvs/0713_bok_courses_cat_weights.csv'...")
  ds_schools_df.to_csv(data_path + 'csvs/0713_bok_courses_cat_weights.csv',index=False)

#process words, create dictionaries for future function calls
responses, school_list = process_words(stop_words,new_schools)

#tfidf analysis
tfidf(responses,school_list)


#MACHINE lEARNING
#make floats finite
for i in range(len(ds_schools_df)):
  ds_schools_df.loc[i, 'Weights'] = float('%.5f'%(ds_schools_df.loc[i,'Weights']))

#create gower matrix & linkage
dm = gower.gower_matrix(ds_schools_df)

# determine k using elbow method

x1 = np.array(ds_schools_df['Sum'])
x2 = np.array(ds_schools_df['Weights'])

plt.plot()
plt.xlim([0, 20])
plt.ylim([0, 1])
plt.title('Dataset')
plt.scatter(x1, x2)
plt.show()

# create new plot and data
plt.plot()
X = np.array(list(zip(x1, x2))).reshape(len(x1), 2)
colors = ['b', 'g', 'r']
markers = ['o', 'v', 's']

# k means determine k
distortions = []
K = range(1,10)
for k in K:
    kmeanModel = KMeans(n_clusters=k).fit(X)
    kmeanModel.fit(X)
    distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])

# Plot the elbow
plt.plot(K, distortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k')
plt.show()

# create kmeans object
kmeans = KMeans(n_clusters=4)
# fit kmeans object to data
kmeans.fit(dm)

# save new clusters for chart
y_km = kmeans.fit_predict(dm)
ds_schools_df['category']=pd.DataFrame(y_km)

groups = ds_schools_df.groupby("category")
for name, group in groups:
    plt.plot(group["Weights"], group["Sum"], marker="o", linestyle="", label=name)
plt.legend()

#save to csv
print("Creating 'csvs/0713_FINAL_all_groups_all_results.csv'...")
ds_schools_df.to_csv(data_path + 'csvs/0713_FINAL_all_groups_all_results.csv', index=False)
