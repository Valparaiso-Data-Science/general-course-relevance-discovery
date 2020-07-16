# -*- coding: utf-8 -*-
"""
Prints out a simple summary of the courses extracted from the school catalogs.

Created on Mon Jun  8 11:51:22 2020

@author: Francisco Vazquez
"""

import os
import pandas as pd

n_colleges=0
n_courses = 0
for filename in os.listdir('../courses'):

    # if current file is the one for all schools, skip it
    if filename == "AllSchools.csv":
        continue

    csv = pd.read_csv('../courses/'+filename,encoding = 'utf-8')
    n_colleges +=1
    n_courses += len(csv['CourseID'])
    print('number of courses in ' + filename + ': ' + str(len(csv['CourseID'])))

print('\n')
print('number of colleges: ' + str(n_colleges))
print("number of courses: " +str(n_courses))
print("average number of courses per college: " + str((n_courses/n_colleges)))