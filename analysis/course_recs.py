# -*- coding: utf-8 -*-

#Import Statements

import pandas as pd
import numpy as np
import re
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
			# Create a new row that the OG data frame row, plus the list of 
			# found terms
			course_row = list(course_df.iloc[i])
			course_row.append(found_terms)

			# add this to the temp_df
			temp_df.append(course_row)

	#Create a dataframe of the recommended courses
	courses_rec_cols = course_cols
	courses_rec_cols = course_rec_cols.append("FoundTerms")

	courses_rec_df = pd.DataFrame(temp_df)
	courses_rec_df.columns = courses_rec_cols

	return courses_rec_df
	
def save_course_recs(dir_name, out_filename, out_dataframe):
	pass 
	
	# Check if the directory has the ending / 
	if dir_name[-1] != "/":
		dir_name = dir_name + "/"
	print("Saving data frame to directory" , str(dir_name)) 
	ds_schools_df.to_csv('csvs/SMITH_blank_courses.csv',encoding="utf-8-sig")