import re
import xml.etree.ElementTree as ET
import pandas as pd
import os
from lxml import etree


def parseXML(filepath, courseTag, descTag, descTagsFromID):
    '''
    IN: the file path, the tag for courses, the tag for descriptions, and the number of tags down the description will be
    OUT: a dataframe of the courses
    '''
    # Get xml (tree) into a list (stack) and find courses (courseID & descriptions)
    parser = etree.XMLParser(recover=True)
    tree = ET.parse(filepath, parser=parser)
    text = tree.getroot()
    courseID = []
    descriptions = []
    stack = []
    #Convert xml text into stack list
    #Probably here: if file is .xml do this, if file is .pkl skip this and set stack equal to that
    for subLevel in text:
        recursive(subLevel, stack)

    counter = 0
    for xml in stack:
        if xml.text is not None:
            #Course ID, Tags of ID and desc, CourseID less than 15 words, description longer than 20, CourseID of only 1 in first element, Description doesnt start with courseID
            if re.match("[A-Z]{2,5}\s+[0-9]{3,4}[A-Z]{0,1}", xml.text) is not None and \
                (xml.tag == courseTag) and \
                (stack[counter + descTagsFromID].tag) == descTag and \
                len(re.findall(r'\w+', xml.text)) < 15 and \
                len(re.findall(r'\w+', stack[counter + descTagsFromID].text)) > 6 and \
                len(re.findall("[A-Z]{2,5}\s+[0-9]{3,4}[A-Z]{0,1}", xml.text)) < 2 and \
                re.match("^.{0,10}([A-Z]{2,5}\s+[0-9]{3,4}[A-Z]{0,1})", stack[counter + descTagsFromID].text) is None:
                    # print("0:", xml.tag, xml.text)
                    # print("1:", stack[counter+1].tag, stack[counter+1].text)
                    courseID.append(xml.text)
                    descriptions.append(stack[counter + descTagsFromID].text)
        #list Counter
        counter += 1
    courses_df = pd.DataFrame({'School': os.path.basename(filepath.replace(".xml", "")), 'CourseID': courseID, 'Descriptions': descriptions})
    return (courses_df)

# potential renaming of this function could be 'createStack'?
def recursive(xml, stack):
    '''
    IN: the xml object?
    OUT: the stack
    Responsible for creating the 'stack' (the thing that has all of the parsible xml text in it)
    '''
    #Remove null and blank lines
    if xml.text is not None:
        if not xml.text.isspace():
            stack.append(xml)
    #Loop to bottom of a nested xml tag
    for subLevel in xml:
        recursive(subLevel, stack)

