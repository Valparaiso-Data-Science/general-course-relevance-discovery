import re       #Regex
import csv      #CSV

###PDFMINER###
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
import io
import fileinput
import pandas
import numpy as np
#resource_manager = PDFResourceManager()
#fake_file_handle = io.StringIO()
#converter = TextConverter(resource_manager, fake_file_handle)
#page_interpreter = PDFPageInterpreter(resource_manager, converter)

#parse is a function that, given a *string* of text, will pull out the class descriptions
def parse(text, regex):
    text = text.replace("\n", "")
    text = text.replace(',', '')
    prereqs = np.array(re.findall(r'((?:Prerequisite.*?\.))', text))
    for prereq in prereqs:
        text = text.replace(prereq, "")
    # reMatches = np.array(re.findall(r'[A-Z]{2,5} [0-9]{2,5}[A-Z]?[.]?', text))
    matches = list(re.finditer(regex, text))
    result = {}
    lengthMatches = len(matches)
    #loop through the match objects, enumerate makes it so the index is available
    for i,m in enumerate(matches):

            #classId is set too the current match's string
            classID = m.group(0)
            #the start of the current class's description starts with the END of the ClassID
            startDesc = m.end()
            #if we are not on the last item,
            #the end of the description will be at the start of the next ClassID found
            #otherwise the description ends at the end of the text
            if i < lengthMatches-1:
                endDesc = matches[i+1].start()
            else:
                endDesc = len(text)-1
            if classID not in result:
                if(len(text[startDesc:endDesc]) > 200 and len(text[startDesc:endDesc]) < 750):
                    print(text[startDesc:endDesc])
                    print()
                    result[classID] = text[startDesc:endDesc]
            else:
                if(len(text[startDesc:endDesc]) > 75 and len(text[startDesc:endDesc]) < 750):
                    print(text[startDesc:endDesc])
                    print()
                    result[classID] += text[startDesc:endDesc]
    #print(result)
    return result

def getDataFromTxt(text):
    courses = np.array(re.findall(r'(?P<SECTION>[A-Z]{2,5} [0-9]{2,5}[A-Z]?[\.]?)(?P<TITLE>[^.]+\.)(?P<DESCRIPTION>.*\n)', text))
    print(courses)
    return courses
    #
    # with open("./output.csv", "w+") as courseList:
    #     courseList.write('SECTION,TITLE,DESCRIPTION\n')
    #     for course in courses:
    #         courseList.write(u'%s,%s,%s' % (course[0], course[1], course[2]))

def PDFtoTXT(filePath):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(filePath, 'rb') as fh:
        ###PDFMiner stuff
        for page in PDFPage.get_pages(fh,caching=True,check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
        converter.close()
        fake_file_handle.close()
        ###End of PDFMiner stuff
    return text




#print(parse(text,"[A-Z]{2,5}\s[0-9]{3,4}[A-Z]{0,1}"))
