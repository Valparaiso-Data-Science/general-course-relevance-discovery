# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 10:14:07 2019

@author: nrandle
"""

import pandas as pd

df = pd.read_csv("desc.csv").dropna()
df = df.drop(df.columns[0],axis=1)

from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()

vectors = vectorizer.fit_transform(df['Description'])
