import re
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import sys
import io
import os


def parseXML(filepath):
    #Get xml into a variable to work on
    tree = ET.parse(filepath)
    root = tree.getroot()
    courseID = []
    descriptions = []
    for x in tree.iter():
        #if x.text != None:
        try:
            if re.match("[A-Z]{2,5}\s[0-9]{3,4}[A-Z]{0,1}",x[0].text) is not None and x[1].text is not None:
                courseID.append(x[0].text)
                descriptions.append(x[1].text)
                #print("1: " + x[0].tag + " " + x[0].text)
                #print("\t2: " + x[1].tag + " " + x[1].text)
        except:
            pass
    #recursive(root, courseID, descriptions)
    courses_df = pd.DataFrame({'School': os.path.basename(filepath.replace(".xml","")), 'CourseID':courseID, 'Descriptions':descriptions})
    return(courses_df)

def recursive(text, courseID, descriptions):
        #Check if current tag holds the course ID
        if re.match("[A-Z]{2,5}\s[0-9]{3,4}[A-Z]{0,1}",text[0].text) is not None and text[1].text is not None:
            #courses_df = df.append({'CourseID':text[0].text,'Description':text[1].text},ignore_index=True)
            courseID.append(text[0].text)
            descriptions.append(text[1].text)
            #If there are lower levels (nested tags), follow down to the bottom tag
        for subLevel in list(text):
            recursive(subLevel, courseID, descriptions)