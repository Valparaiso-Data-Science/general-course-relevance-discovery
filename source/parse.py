import re
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import sys
import io
import os

courseID = []
descriptions = []

def parseXML(filepath):
    #Get xml into a variable to work on
    tree = ET.parse(filepath)
    root = tree.getroot()
    recursive(root)
    courses_df = pd.DataFrame({'CourseID':courseID, 'Descriptions':descriptions, 'School': os.path.basename(filepath.replace(".xml",""))})
    return(courses_df)

def recursive(text):
    try:
        #Check if current tag holds the course ID
        if re.match("[A-Z]{2,5}\s[0-9]{3,4}[A-Z]{0,1}",text[0].text) is not None and len(text[0].text)>20 and text[1].text is not None:
            print("Course: ", text[0].text,"\n")
            print("Desc: ", text[1].text,"\n")
            print("Try3: ", text[2].text,"\n")
            #courses_df = df.append({'CourseID':text[0].text,'Description':text[1].text},ignore_index=True)
            courseID.append(text[0].text)
            descriptions.append(text[1].text)
        #If there are lower levels (nested tags), follow down to the bottom tag
        for subLevel in list(text):
            recursive(subLevel)
    except:
        pass
        