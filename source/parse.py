import re
import xml.etree.ElementTree as ET
import pandas as pd
import os
from lxml import etree
import wordninja
from reintroduce_spaces import main
#from punct_split import punct_split

def parseXML(filepath, courseTag, descTag, descTagsFromID):
    '''
    IN: the file path, the tag for courses, the tag for descriptions, and the number of tags down the description will be
    OUT: a dataframe of the courses
    '''
    # Get xml (tree) into a list (stack) and find courses (courseID & descriptions)
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
    match = re.search('superTrimmedPDFs/',filepath)
    filename = filepath[match.end():]
    #Check if the college we are parsing is known to have Course ID's and Descriptions in one <P> tag
    special_colleges = ['Alma', 'Northwestern','Sagu']
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
    for elm in stack:
        if elm.text is not None:
            if counter + descTagsFromID >= len(stack):
                oob = True
            if not oob:
                #Check if we match the Course ID pattern at the beginning of the line
                #Check if we are looking at a <P> tag
                #Checks if the next element is a <P> tag
                #Checks that the Course ID is less than 19 words
                #Checks if the description is longer than 6 words
                #Checks that there is only 1 Course ID in the line
                #Checks that the next <P> tag doesn't start with a Course ID
                if re.match("[A-Z]{2,5}(-|\s+)[0-9]{3,4}[A-Z]{0,1}", elm.text) is not None and \
                        (elm.tag == courseTag) and \
                        (stack[counter + descTagsFromID].tag) == descTag and \
                        len(re.findall(r'\w+', elm.text)) < 19 and \
                        len(re.findall(r'\w+', stack[counter + descTagsFromID].text)) > 6 and \
                        len(re.findall("[A-Z]{2,5}(-|\s+)[0-9]{3,4}[A-Z]{0,1}", elm.text)) < 2 and \
                        re.match("^.{0,10}([A-Z]{2,5}(-|\s+)[0-9]{3,4}[A-Z]{0,1})", stack[counter + descTagsFromID].text) is None:
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
                            re.match("[A-Z]{2,5}(-|\s+)[0-9]{3,4}[A-Z]{0,1}", stack[counter + descTagsFromID + extTags].text) is None:
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
                elif re.match("[A-Z]{2,5}(-|\s+)[0-9]{3,4}[A-Z]{0,1}", elm.text) is not None and \
                    (len(re.findall("[A-Z]{2,5}(-|\s+)[0-9]{3,4}[A-Z]{0,1}", elm.text)) < 2 or (len(re.findall("preq|prereq",elm.text.lower())) >= 1))and \
                    len(re.findall(r'\w+', elm.text)) >= 15 and \
                    (elm.tag == courseTag) and \
                    extParse:
                        #Gives us an index for the start and end of the Course ID
                        matchID = re.match("[A-Z]{2,5}(-|\s+)[0-9]{3,4}[A-Z]{0,1}", elm.text)
                        #Sets the Course ID to strictly the captial letters and numbers (ex: DATA 151)
                        courseID.append(elm.text[matchID.start():matchID.end()])
                        #Sets the description as everything besides the Course ID (Note: this means that the course title will be in the description)
                        descriptions.append(elm.text[matchID.end():])
        counter += 1
    #Create a Pandas DataFrame with school being the filename, CourseID & Descriptions are set to their respective lists
    courses_df = pd.DataFrame(
        {'School': os.path.basename(filepath.replace(".xml", "")), 'CourseID': courseID, 'Descriptions': descriptions})
    return (courses_df)


def createStack(xml, stack):
    '''
    IN: the xml object?
    OUT: the stack
    Responsible for creating the 'stack' (the thing that has all of the parsable xml text in it)
    '''
    #Remove null and blank lines
    if xml.text is not None:
        if not xml.text.isspace():
            stack.append(xml)
    #Loop to bottom of a nested xml tag
    for subLevel in xml:
        createStack(subLevel, stack)

def superTrimXML(filename):
    #Boolean to tell us if we are looking in a <Figure> element
    isFig = False
    #Checks if we are looking at a college we know needs WordNinja
    wn_colleges = ['Brown','Carlow','Caldwell','Denison','Youngstown']
    for college in wn_colleges:
        if re.match(college,filename) is not None:
            needsWN = True
            break
        else:
            needsWN = False
    #Opens the trimmed XML
    with open("../source/TRIMMED/"+filename, "r",encoding='utf-8') as file:
        #Makes a new XML file where the super trimming will be saved
        with open("../source/superTrimmedPDFs/"+filename.replace("TRIMMED", "SUPERTRIMMED"),
                  "w", encoding='utf-8') as newfile:
            #Writes an open <Part> tag. This allows us to parse the file as an XML later
            newfile.write("<Part>\n")
            #Loop through each line in the Trimmed XML
            for line in file:
                # turn file into string
                text = str(line)
                # Remove <Figure> tags and everything in them
                if len(re.findall("</Figure>", text)) == 1:
                    text = ""
                    isFig = False
                if isFig:
                    text = ""
                if len(re.findall("<Figure>", text)) == 1:
                    text = text.replace("<Figure>","")
                    isFig = True
                # remove Sect tags
                text = text.replace("</Sect>", "")
                text = text.replace("<Sect/>", "")
                text = text.replace("<Sect>", "")
                # remove Div tags
                text = text.replace("</Div>", "")
                text = text.replace("<Div>", "")
                # remove caption tags
                text = text.replace("</Caption>", "")
                # rmove part tags
                text = text.replace("<Part>","")
                text = text.replace("</Part>","")
                # remove Span tags
                text = text.replace("<Span/>","")
                # remove story tags
                text = text.replace("<Story>","")
                text = text.replace("</Story>","")
                #If there is a <P> tag with a new line directly after it, delete the new line
                if re.match('<P>\n', text) is not None:
                    text = text.replace('\n', '')
                #Writes the processed line to the super trimmed XML
                newfile.write(text)
            #Closing our open <Part> tag so we don't get any errors
            newfile.write("</Part>\n")
    #Checks if the college needs Word Ninja
    if needsWN:
        #Pass the super trimmed XML into Word Ninja
        main(filename.replace('TRIMMED','SUPERTRIMMED'))
        #Delete the old, not Word Ninja-ed file
        os.remove('../source/superTrimmedPDFs/'+filename.replace('TRIMMED','SUPERTRIMMED'))

