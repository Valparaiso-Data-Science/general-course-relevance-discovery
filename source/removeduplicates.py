'''
removing duplicates from csv files
'''

import pandas as pd
import csv

def remove():
    data = pd.read_csv("analysis/AllSchools-07-10-2020-FROZEN.csv")
    
    #this assumes that the csv will have a CourseID column
    data = data.drop_duplicates(subset= ['CourseID'], keep=False, inplace= True)

remove()
