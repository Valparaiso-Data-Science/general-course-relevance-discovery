# general-course-relevance-discovery
This repo is intended to house code that allows for data science topics discovery from university course catalogs

# Getting Started
Make sure that you have python 3 installed and optionally a POSIX compliant shell interpreter (bash or dash will work).
To install all of the required dependencies, run:
> python getReqs.py
This is currently only on the 'wordninja' branch, but will be merged into master soon

# Repo Structure

This repo has a number of direcories, each with a function.
* *pre/* - Has shell script that are made for preprocessing XML files
* *source/* - Has all of the python code that does all of the 'magic'
* *source/tests/* - Contains all of the pytest tests for the repo
* *courses/* - The output csvs that we run machine learning on
* *fullPDFs/* - The source XML (aka the raw data)

# XMLs with spacing problems
-2011Cornell
-Brown
-Carlow 
-Caldwell 
-Denison 
-Pittsburgh (broken XML, we're currently working on a fix)
-Youngstown
