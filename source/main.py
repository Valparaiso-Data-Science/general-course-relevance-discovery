from parse import parseDirectory
import os
import pandas as pd
from vectorize import cleanData, vectorizer, cleanVectorizer, labelTargetsdf
courses_dict = parseDirectory("../fullPDFs/")
courses_df = pd.DataFrame(courses_dict,index=[0,1]).transpose()
x= cleanData(courses_df)
y = vectorizer(x)
w = cleanVectorizer(y)

print(labelTargetsdf(w))
