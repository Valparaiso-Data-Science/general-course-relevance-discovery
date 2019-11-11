import re
import xml.etree.ElementTree as ET
import pandas as pd
import os

def parseXML(filepath, courseTag, descTag, descTagsFromID):
    # Get xml (tree) into a list (stack) and find courses (courseID & descriptions)
    tree = ET.parse(filepath)
    text = tree.getroot()
    courseID = []
    descriptions = []
    stack = []

    #Convert xml text into stack list
    for subLevel in text:
        recursive(subLevel, stack)

    counter = 0
    for xml in stack:
        if xml.text is not None:
            #Check if description is greater than 50char? (to remove more tables)
            if re.match("[A-Z]{2,5}\s[0-9]{3,4}[A-Z]{0,1}", xml.text) is not None and \
                    (xml.tag == courseTag) and \
                    (stack[counter + descTagsFromID].tag == descTag) and \
                    len(stack[counter + descTagsFromID].text) > 30:

                courseID.append(xml.tag + " " + xml.text)
                descriptions.append(stack[counter + descTagsFromID].tag + " " + stack[counter + descTagsFromID].text)

                # print(xml.tag, xml.text)
                # print(stack[counter + descTagsFromID].tag, stack[counter + descTagsFromID].text)
        counter += 1

    courses_df = pd.DataFrame({'School': os.path.basename(filepath.replace(".xml", "")), 'CourseID': courseID, 'Descriptions': descriptions})

    return (courses_df)


def recursive(xml, stack):
    #Remove null and blank lines
    if xml.text is not None:
        if not xml.text.isspace():
            stack.append(xml)
    #Loop to bottom of a nested xml tag
    for subLevel in xml:
        recursive(subLevel, stack)
