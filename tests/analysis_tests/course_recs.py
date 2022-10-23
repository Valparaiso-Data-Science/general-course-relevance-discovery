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

	print(schools_df)
	return schools_df
# import_df("test.csv")

def load_terms(term_filename):
	""" Load term list from TERM_FILENAME. Lowercase all terms and remove 
	any duplicates. """

	# Check that the file is a txt
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

def recommend_courses(clean_terms, course_df):
	""" Search a dataframe of courses called COURSE_DF for classes that contain 
	terms from CLEAN_TERMS. (((The last variable SEARCH_COLS lists the columns 
	that are to be searched.)))<-may not be necessary """	
	course_cols = list(course_df.columns)

	# Initialize an empty data frame
	temp_df = []
	temp_list = []

	# Loop over all the courses in a school: 
	for i in range(len(course_df)):

		# Initialize a temporary list of terms:
		found_terms = []

		# Loop over the listed search columns: 
		##is this necessary if parse.py is manually parsing and organizing XML to CSV to fit the course_df["Course ID"]
		course_info = str(course_df["CourseID"][i])
		course_info = course_info.lower()


		for term in clean_terms: 
			print("term:", term, "\n")
			space = r'\s' #regex space pattern
			if re.search(space+term+space,course_info):
				if term not in found_terms:
					found_terms.append(term)

		if len(found_terms) > 0:
			# Create a new row that the OG data frame row, plus the list of 
			# found terms
			##course_row = list(course_df.iloc[i])
			#course_row.append(found_terms)
			temp_list = [course_df['School'][i], course_df['CourseID'][i], course_df['Descriptions'][i],', '.join(found_terms)] #append course to new list
    		#temp_df.append(temp_list) #append list to new dataframe
			# add this to the temp_df
			temp_df.append(temp_list)

	#Create a dataframe of the recommended courses
	courses_rec_cols = course_cols
	courses_rec_cols = courses_rec_cols.append("FoundTerms")

	courses_rec_df = pd.DataFrame(temp_df)
	##courses_rec_df.columns = courses_rec_cols
	courses_rec_df.columns = ['School','CourseID','Descriptions','FoundTerms'] #label columns

	return courses_rec_df

def save_course_recs(dir_name, out_filename, course_dataframe):
	""" Save the data frame of courses to a CSV"""

	assert out_filename[-3:] == 'csv', "File must be a CSV"

	# Create the output file name:
	full_out_file = dir_name + out_filename

	print("Saving data frame to directory" , str(dir_name)) 
	course_dataframe.to_csv(full_out_file,encoding="utf-8-sig")

	return out_filename


##### 
# Need to run: python -m spacy download en_core_web_sm for main.py