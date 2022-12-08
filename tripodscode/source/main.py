'''
Main file that runs the whole pipeline, from raw XML catalogs, to course classification with decision trees.
'''

# files in the current directory

#from topicModel import plot_10_most_common_words, listofDSCourse
import createDATA
import prep
import pandas as pd
import sys

from datetime import date

# container for processed catalogs
topicModel = pd.DataFrame()

# toggle for keeping data from intermediary stages
dirty = False
if len(sys.argv) > 1 and sys.argv[1] == 'dirty':
    dirty = True

# Make all of the required directories; prep the work area
prep.prepare()
# Create 'AllSchools.csv'
createDATA.createCSV()

