# -*- coding: utf-8 -*-

#Import Statements

import pandas as pd
import numpy as np
from re import *


def import_df(school_filename):
	""" Load dataframe in SCHOOL_FILENAME. Delete the first unnamed column.
	FILENAME must be a CSV. """

	# Check that the file is a CSV
	assert school_filename[-3:] == 'csv', "File must be a CSV"

	# Load the file 
	schools_df = pd.read_csv(school_filename)

	# Delete first column if the column has no name
	cols = list(schools_df.columns)
	if cols[0] == 'Unnamed: 0':
		del(schools_df['Unnamed: 0'])

	return schools_df

def load_terms(term_filename):
	""" Load term list from TERM_FILENAME. Lowercase all terms and remove 
	any duplicates. """

	# Check that the file is a CSV
	assert term_filename[-3:] == 'txt', "Terms must be stored in a TXT"

	# Load the file 
	text_file = open(term_filename, "r")
	
	# Create a list of terms by splitting on the carriage return
	bok = text_file.read().split('\n')

	# Drop each term to lowercase
	# -- NOTE: We do this as a for loop to allow for the possibilty that 
	# --       terms are more than just one word.
	for i in range(len(bok)): 
  		bok[i] = bok[i].lower()

  	# Remove any duplicate terms
  	# Code based on this discussion: 
  	# https://stackoverflow.com/questions/12897374/get-unique-values-from-a-list-in-python
  	bok = list(set(bok))

  	return bok

def recommend_courses(clean_terms, course_df, search_cols):
	""" Search a dataframe of courses called COURSE_DF for classes that contain 
	terms from CLEAN_TERMS. The last variable SEARCH_COLS lists the columns 
	that are to be searched. """	
	course_cols = list(course_df.columns)

	# Initialize an empty data frame
	temp_df = []

	# Loop over all the courses in a school: 
	for i in range(len(course_df)):

		# Initialize a temporary list of terms:
		found_terms = []

		# Loop over the listed search columns: 
		for col_name in search_cols:
			course_info = str(course_df[col_name][i])
			course_info = course_info.lower()

			for term in clean_terms: 
				space = r'\s' #regex space pattern
				if re.search(term+space,des) or re.search(space+term,des):
					found_terms.append(term)

		if len(found_terms) > 0:
			pass
			# Create a new row that the OG data frame row, plus the list of 
			# found terms

			# add this to the temp_df

	#Create a dataframe of the recommended courses
	courses_rec_cols = course_cols
	courses_rec_cols = course_rec_cols.append("FoundTerms")

	courses_rec_df = pd.DataFrame(temp_df)
	courses_rec_df.columns = courses_rec_cols

	return courses_rec_df
	


"""
for i in range(len(schools_df)): #for each course
  des = str(schools_df['CourseID'][i])
  des = des.lower()
  temp_list = []
  terms = []
  #print(i)
  for w in bok: #for each bok term
    space = r'\s' #regex space pattern
    if re.search(space+w+space,des): #if the course contains the bok term
      if w not in terms: #if the bok term is not already in the list for that description
        terms.append(w) #append bok term
  if len(terms) != 0: #if at least 1 term is in the description
    temp_list = [schools_df['School'][i], schools_df['CourseID'][i], schools_df['Descriptions'][i],', '.join(terms)] #append course to new list
    temp_df.append(temp_list) #append list to new dataframe
ds_schools_df = pd.DataFrame(temp_df) #create permanent new data frame
ds_schools_df.columns = ['School','CourseID','Descriptions','Data Science Term'] #label columns
print("Creating 'csvs/SMITH_THE_courses.csv'...") #create csv of data science courses
ds_schools_df.to_csv('csvs/SMITH_blank_courses.csv',encoding="utf-8-sig")

"""
