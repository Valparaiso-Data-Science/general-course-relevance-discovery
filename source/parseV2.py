# -*- coding: utf-8 -*-
import PyPDF2   #PDF Reader
import re       #Regex
import csv      #CSV

#Grab PDF and create outpute file
pdfFileObj = open("C:/Users/cpacker/Desktop/general-course-relevance-discovery/testPDFs/SmithTest.pdf", 'rb')
pdf = PyPDF2.PdfFileReader(pdfFileObj)
#file = open("Output.txt","w")

start = False   #Variable used to avoid writing everything before first class is found
details = []    #Array stuff inbetween courses
newClass = False

#Go through every page
for page in range(pdf.numPages):
    #Formating pdf into array of lines (has issue with newlines)
    pageObj = pdf.getPage(page)
    text = pageObj.extractText()
    #Go through every line
    updated = (text.encode("utf-8").split())
    for line in range(len(updated)):
        print(updated[line])
    #for line in text:
        #print(text)
        #print(line)
            #Check for course level (MATH 240)
            #newClass = bool(re.search("[A-Z]{2,5}\s[0-9]{3,4}[A-Z]{0,1}", line))
#        if newClass:
#            #If you are a new class title:
#            if newClass:
#                #Combine everything between finding a class at the beginning and another at the end
#                output = '|'.join(details)
#                file.write(output+"\n\n")
#                details.clear()
#                start = True
#                details.append(updated[line])
#            elif start:
#                details.append(updated[line])
#file.close()
pdfFileObj.close()
