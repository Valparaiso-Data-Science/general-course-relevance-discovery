import re
import xml.etree.ElementTree as ET
import pandas as pd
import os
from lxml import etree

def parseXML(filepath, courseTag, descTag, descTagsFromID):
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
            # if re.match("[A-Z]{2,5}\s[0-9]{3,4}[A-Z]{0,1}", xml.text) is not None:
            #     print(xml.tag, xml.text)
            #     print("1:",stack[counter+1].tag, stack[counter+1].text)
            #     print("2:",stack[counter+2].tag, stack[counter+2].text)
            #     print("3:", stack[counter + 3].tag, stack[counter + 3].text)
            #     print("")

            #Check not empty, check course tag is proper, check desc tag is proper, check desc word count
            if re.match("[A-Z]{2,5}\s[0-9]{3,4}[A-Z]{0,1}", xml.text) is not None and \
                    (xml.tag == courseTag) and \
                    (stack[counter + descTagsFromID].tag == descTag) and \
                    len(re.findall(r'\w+', stack[counter + descTagsFromID].text)) > 15:
                #
                # print(xml.tag, xml.text)
                # print("1:",stack[counter+1].tag, stack[counter+1].text)
                # print("")
                courseID.append(xml.text)
                descriptions.append(stack[counter + descTagsFromID].text)

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
