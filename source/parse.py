import re
import xml.etree.ElementTree as ET
import pandas as pd
import os
from lxml import etree
import wordninja
from reintroduce_spaces import main
from punct_split import punct_split

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
    inCD = True
    match = re.search('superTrimmedPDFs/',filepath)
    filename = filepath[match.end():]
    special_colleges = ['Alma', 'Northwestern','Sagu']
    for college in special_colleges:
        if re.match(college,filename) is not None:
            extParse = True
            break
        else:
            extParse = False
    # Convert xml text into stack list
    # Probably here: if file is .xml do this, if file is .pkl skip this and set stack equal to that
    for subLevel in text:
        recursive(subLevel, stack)

    counter = 0
    for xml in stack:
        if xml.text is not None:
            if counter + descTagsFromID >= len(stack):
                inCD = False
            if inCD:
                # Course ID, Tags of ID and desc, CourseID less than 15 words, description longer than 20, CourseID of only 1 in first element, Description doesnt start with courseID
                if re.match("[A-Z]{2,5}(-|\s+)[0-9]{3,4}[A-Z]{0,1}", xml.text) is not None and \
                        (xml.tag == courseTag) and \
                        (stack[counter + descTagsFromID].tag) == descTag and \
                        len(re.findall(r'\w+', xml.text)) < 19 and \
                        len(re.findall(r'\w+', stack[counter + descTagsFromID].text)) > 6 and \
                        len(re.findall("[A-Z]{2,5}(-|\s+)[0-9]{3,4}[A-Z]{0,1}", xml.text)) < 2 and \
                        re.match("^.{0,10}([A-Z]{2,5}(-|\s+)[0-9]{3,4}[A-Z]{0,1})", stack[counter + descTagsFromID].text) is None:
                    # print("0:", xml.tag, xml.text)
                    # print("1:", stack[counter+1].tag, stack[counter+1].text)
                    description = stack[counter + descTagsFromID].text
                    for extTags in range(1,7):
                        if (counter + descTagsFromID + extTags) < len(stack) and \
                            (stack[counter + descTagsFromID + extTags].tag) == descTag and \
                            len(re.findall(r'\w+',stack[counter + descTagsFromID + extTags].text)) >= 6 and \
                            re.match("[A-Z]{2,5}(-|\s+)[0-9]{3,4}[A-Z]{0,1}", stack[counter + descTagsFromID + extTags].text) is None:
                                description += stack[counter + descTagsFromID + extTags].text
                                if extTags == 6:
                                    description = stack[counter + descTagsFromID].text
                        else:
                            break
                    description = re.sub('^\s+', '', description)
                    courseID.append(xml.text)
                    descriptions.append(description)
                elif re.match("[A-Z]{2,5}(-|\s+)[0-9]{3,4}[A-Z]{0,1}", xml.text) is not None and\
                    (len(re.findall("[A-Z]{2,5}(-|\s+)[0-9]{3,4}[A-Z]{0,1}", xml.text)) < 2 or (len(re.findall("preq|prereq",xml.text.lower())) >= 1))and\
                    len(re.findall(r'\w+', xml.text)) >= 15 and\
                    (xml.tag == courseTag) and \
                    extParse:
                        matchID = re.match("[A-Z]{2,5}(-|\s+)[0-9]{3,4}[A-Z]{0,1}", xml.text) 
                        courseID.append(xml.text[matchID.start():matchID.end()])
                        descriptions.append(xml.text[matchID.end():])
                # list Counter
        #print(counter)
        #print(stack[counter + descTagsFromID].text)
        counter += 1

    courses_df = pd.DataFrame(
        {'School': os.path.basename(filepath.replace(".xml", "")), 'CourseID': courseID, 'Descriptions': descriptions})
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


def textNeedsToBeSplit(text):
    '''
    IN: a string
    OUT: a boolean on whether word ninja thinks it'd be a good idea to split it or not
    '''
    str_split_words = text.split(' ')
    wn_split_words = wordninja.split(text)
    if len(str_split_words) != len(wn_split_words):
        return True
    else:
        return False

def wnSplitText(nstext):
    '''
    IN: a non split text string
    OUT: a split text string (via word ninja)
    '''
    stext=''
    wn_split_words = wordninja.split(nstext)
    for word in wn_split_words:
        stext += ' '+word
    return stext

def cleanXML(filename):
    isFig = False
    wn_colleges = ['Carlow','Caldwell']
    for college in wn_colleges:
        if re.match(college,filename) is not None:
            needsWN = True
            break
        else:
            needsWN = False
    with open("../source/TRIMMED/"+filename, "r",encoding='utf-8') as file:
        with open("../source/superTrimmedPDFs/"+filename.replace("TRIMMED", "SUPERTRIMMED"),
                  "w", encoding='utf-8') as newfile:
            newfile.write("<Part>\n")
            for line in file:
                # turn file into string
                text = str(line)
                # take care of figures
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
                # fix p tags
                text = text.replace("<Span/>","")
                # remove story tags
                text = text.replace("<Story>","")
                text = text.replace("</Story>","")
                if re.match('<P>\n', text) is not None:
                    text = text.replace('\n', '')
                
                #text = text.replace("</Figure>", "")  # fix this later!! this creates extra <P> tags in some xmls (but still works??)
                text = punct_split(text)
                newfile.write(text)
            newfile.write("</Part>\n")
    if needsWN:
        main(filename.replace('TRIMMED','SUPERTRIMMED'))
        os.remove('../source/superTrimmedPDFs/'+filename.replace('TRIMMED','SUPERTRIMMED'))
    
