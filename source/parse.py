"""
    Contains functions that apply space correction (when needed) and extract course titles and descriptions out of
    preprocessed XML.
"""

import re
import xml.etree.ElementTree as ET
import pandas as pd
import os
from lxml import etree
import wordninja
#from punct_split import punct_split
from new_reintroduce_spaces import reintroduce_spaces

#course id regex string
c_id_re_s = r"[A-Z]{2,5}(-|\s+)[0-9]{3,4}[A-Z]{0,1}" #Works for all course catalog
c_id_re = re.compile(c_id_re_s)

def parseXML(filepath, courseTag, descTag, descTagsFromID):
    '''
    Extracts course titles and descriptions from preprocessed XML.

    IN: the file path, the tag for courses, the tag for descriptions, and the number of tags down the description will be
    OUT: a Pandas dataframe of the courses
    '''
    # Get xml (tree) into a list (stack) and find courses (courseID & descriptions)
    #why stack? LIFO
    parser = etree.XMLParser(recover=True)
    tree = ET.parse(filepath, parser=parser)
    text = tree.getroot()
    #List of Course ID's that will be appended to CSV
    courseID = []
    #List of Descriptions that will be appended to CSV
    descriptions = []
    #The aforementioned stack
    stack = []
    #Boolean to keep us from getting an index out of bounds (O.O.B) error
    oob = False
    #Gets us the filename (ex:  Alma.xml)
    match = re.search('superTrimmedPDFs/',filepath) # < potential for a bug here!!!!!
    filename = filepath[match.end():]
    #Check if the college we are parsing is known to have Course ID's and Descriptions in one <P> tag
    special_colleges = ['Alma', 'Northwestern','Sagu'] #tested on other colleges, these have special catalogs?
    for college in special_colleges:
        if re.match(college,filename) is not None:
            extParse = True
            break
        else:
            extParse = False
    # Convert xml text into stack list
    for subLevel in text:
        createStack(subLevel, stack)
    #Allows us to keep track of a numeric index in the stack
    counter = 0
    #For each element in the stack:
    for elm in stack: #for every line in the xml
        if elm.text is not None: #when casting each line as text, if it is not empty, move forward
            if counter + descTagsFromID >= len(stack): #checking if out of bounds
                oob = True
            if not oob:
                # print("descTagsFromID:", descTagsFromID)
                # print("descTag:", descTag)
                # print("elm.text:", elm.text)
                # print("counter + descTagsFromID:", counter + descTagsFromID)
                #Check if we match the Course ID pattern at the beginning of the line
                #Check if we are looking at a <P> tag
                #Checks if the next element is a <P> tag
                #Checks that the Course ID is less than 19 words
                #Checks if the description is longer than 6 words (updated to 19 so that small description where courses are listed are not counted)
                #Checks that there is only 1 Course ID in the line
                #Checks that the next <P> tag doesn't start with a Course ID
                # (line below) looking for the first occurance of the courseID in a line, checking if the p tag is a courseID
                if re.match(c_id_re, elm.text) is not None and \
                        (elm.tag == courseTag) and \
                        (stack[counter + descTagsFromID].tag) == descTag and \
                        len(re.findall(r'\w+', elm.text)) < 19 and \
                        len(re.findall(r'\w+', stack[counter + descTagsFromID].text)) > 19 and \
                        len(re.findall(c_id_re, elm.text)) < 2:
                        #re.match("^.{0,10}([A-Z]{2,5}(-|\s+)[0-9]{3,4}[A-Z]{0,1})", stack[counter + descTagsFromID].text) is None:
                        #removed ^ because listing situation is already prevented by checking line length earlier on
                    #Sets the description to the <P> tag after the identified Course ID
                    description = stack[counter + descTagsFromID].text
                    #Check to see if the description is split into multiple <P> tags
                    for extTags in range(1,7):
                        #Make sure we don't go out of bounds
                        #Checks if we are looking at a <P> tag
                        #Checks if the tag is at least 6 words
                        #Checks that the tag doesn't start with a Course ID
                        if (counter + descTagsFromID + extTags) < len(stack) and \
                            (stack[counter + descTagsFromID + extTags].tag) == descTag and \
                            len(re.findall(r'\w+',stack[counter + descTagsFromID + extTags].text)) >= 6 and \
                            re.match(c_id_re, stack[counter + descTagsFromID + extTags].text) is None:
                                #Append the tag to the already existing description
                                description += stack[counter + descTagsFromID + extTags].text
                                #If we reach the end of our loop, just set the description to what it was before this loop started
                                if extTags == 6:
                                    description = stack[counter + descTagsFromID].text
                                    #IF the final course has a multiple <P> tag description we will not catch it. This is due to the fact that we will never reach a stop case
                        else:
                            #End the loop if we reach a stop case
                            break
                    #Get rid of extra white space at the beginning of the description
                    description = re.sub('^\s+', '', description)
                    #Append Course ID and Description to their respective lists
                    courseID.append(elm.text)
                    descriptions.append(description)
                #This checks for Course ID and Description in one <P>
                #Checks if it starts with a Course ID
                #Checks that there is only one Course ID in the element, unless there is a mention of prerequisites
                #Checks if there is at least 15 words
                #Checks if it is a <P> tag
                #Checks if the college is known to have Course ID's and Descriptions in one <P> tag
                elif re.match(c_id_re, elm.text) is not None and \
                    (len(re.findall(c_id_re, elm.text)) < 2 or (len(re.findall("preq|prereq",elm.text.lower())) >= 1))and \
                    len(re.findall(r'\w+', elm.text)) >= 15 and \
                    (elm.tag == courseTag) and \
                    extParse:
                        #Gives us an index for the start and end of the Course ID
                        matchID = re.match(c_id_re, elm.text)
                        #Sets the Course ID to strictly the captial letters and numbers (ex: DATA 151)
                        courseID.append(elm.text[matchID.start():matchID.end()])
                        #Sets the description as everything besides the Course ID (Note: this means that the course title will be in the description)
                        descriptions.append(elm.text[matchID.end():])
        counter += 1
    #Create a Pandas DataFrame with school being the filename, CourseID & Descriptions are set to their respective lists
    courses_df = pd.DataFrame(
        {'School': os.path.basename(filepath.replace(".xml", "")), 'CourseID': courseID, 'Descriptions': descriptions})
    return courses_df


def createStack(element, stack):
    '''
    Recursively traverse element tree and save any found text to stack.
    '''

    #Remove null and blank lines
    if element.text is not None:
        if not element.text.isspace():
            stack.append(element)
    #Loop to bottom of a nested xml tag
    for subLevel in element:
        createStack(subLevel, stack)


def makeCSV(filename, superTrimmedDir):
    # keep a pointer to the non-space-corrected file
    deletable = filename

        # reintroduce spaces and reassign `filename` to cleaned file
    filename = reintroduce_spaces(superTrimmedDir + "/" + filename)
    filename = filename[filename.rfind("/") + 1:]  # chop off the directory path, only leave name filename

        # remove non-space-corrected file
    os.unlink(superTrimmedDir + "/" + deletable)
    """
    Applies space correction if needed and calls parseXML (for extracting courses descriptions and titles out of XML)

    :param filename: current file name
    :param superTrimmedDir: path of the source directory
    """

    #Checks if we are looking at a college we know needs WordNinja
    """ badspacing_colleges = ['Brown', '2011Cornell', 'Carlow', 'Caldwell', 'Denison', 'Pittsburgh', 'Youngstown']

    for college in badspacing_colleges:
        if re.match(college, filename) is not None:
            needsWN = True
            break
        else:
            needsWN = False

    #Checks if the college needs Word Ninja
    if needsWN: """

    # use parseXML to find course headers and descriptions
    CSV = parseXML(superTrimmedDir+ "/" + filename, 'P', 'P', 1)
    CSV.to_csv("../courses/"+filename.replace("xml","csv"), encoding="utf-8-sig")
