from parse import parseDirectory
import os
import pandas as pd
from vectorize import cleanData, vectorizer, cleanVectorizer, labelTargetsdf

pd.options.display.max_columns = 14
pd.set_option('display.width', 600)

courses_dict = parseDirectory("../tempPDFs/")
courses_df = pd.DataFrame(courses_dict,index=[0,1]).transpose()
print("found courses")
cleaned_df = cleanData(courses_df)
print("cleaned")
vect_df = vectorizer(cleaned_df)
print("vect")
pruned_df = cleanVectorizer(vect_df)
print("pruned")

labeled_df = labelTargetsdf(pruned_df)


