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
            # print("0", xml.tag, xml.text)
            #Check regex for 2 matches (if 2 dont go on)
            if re.match("[A-Z]{2,5}\s+[0-9]{3,4}[A-Z]{0,1}", xml.text) is not None:
                # print("1",xml.tag, xml.text)
                if (xml.tag == courseTag):
                    # print("2", xml.text)
                    if (stack[counter + descTagsFromID].tag) == descTag:
                        # print("3", xml.text)
                        if len(re.findall(r'\w+', xml.text)) < 15:
                            # print("4", xml.text)
                            if len(re.findall("[A-Z]{2,5}\s+[0-9]{3,4}[A-Z]{0,1}", xml.text)) < 2:
                                # print("5", xml.text)
                                if len(re.findall(r'\w+', stack[counter + descTagsFromID].text)) > 20:
                                    # print("6", xml.text)
                                    if re.match("^.{0,10}([A-Z]{2,5}\s+[0-9]{3,4}[A-Z]{0,1})", stack[counter + descTagsFromID].text) is None:
                                        # print("7", xml.text)
                                        # print("0:", xml.tag, xml.text)
                                        # print("1:", stack[counter+1].tag, stack[counter+1].text)
                                        # print()
                                        # print("2:",stack[counter+2].tag, stack[counter+2].text)
                                        # print("3:", stack[counter + 3].tag, stack[counter + 3].text)
                                        # print("4:", stack[counter + 4].tag, stack[counter + 4].text)
                                        # print("5:", stack[counter + 5].tag, stack[counter + 5].text)
                                        # print("6:", stack[counter + 6].tag, stack[counter + 6].text)
                                        # print("7:", stack[counter + 7].tag, stack[counter + 7].text)
                                        # print("")
                                        courseID.append(xml.text)
                                        descriptions.append(stack[counter + descTagsFromID].text)
        #course Counter
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
