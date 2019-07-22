from parse import parseDirectory
import os
import pandas as pd
from vectorize import cleanData, vectorizer, cleanVectorizer, labelTargetsdf

pd.options.display.max_columns = 14
pd.set_option('display.width', 600)

courses_dict = parseDirectory("../fullPDFs/")
courses_df = pd.DataFrame(courses_dict,index=[0,1]).transpose()
print("\tfound courses")
cleaned_df = cleanData(courses_df)
print("\tcleaned")
vect_df = vectorizer(cleaned_df)
print("\tvect")
pruned_df = cleanVectorizer(vect_df)
print("\tpruned")
labeled_df = labelTargetsdf(pruned_df)
print("\tfound targets")
labeled_df.to_csv("finaloutput.csv")
