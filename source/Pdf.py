import PyPDF2   #PDF Reader
import re       #Regex
import csv      #CSV

#Grab PDF and create outpute file
pdfFileObj = open("../testPDFs/ValpoTest.pdf", 'rb')
pdf = PyPDF2.PdfFileReader(pdfFileObj)
file = open("Output.txt","w")

start = False   #Variable used to avoid writing everything before first class is found
details = []    #Array stuff inbetween courses

#Go through every page
for page in range(pdf.numPages):
    #Formating pdf into array of lines (has issue with newlines)
    pageObj = pdf.getPage(page)
    text = pageObj.extractText()
    updated = text.split("\n")
    #Go through every line
    for line in range(len(updated)):
        print(repr(updated[line]))
        #Current fix to the newline issue, will be removed when fixed (but doesnt have to be)
        if updated[line] != " ":
            #Check for course level (MATH 240)
            newClass = bool(re.search("[A-Z]{3,5}\s[0-9]{3,4}[A-Z]{0,1}", updated[line]))

            #Check for course title (Intro to Art)
            if newClass and (line+2)<len(updated):
                newClass = bool(re.search("^[A-Z][a-z]",updated[line+2]) or re.search("^[A-Z]\s",updated[line+2]))
            else:
                newClass = False

            #Check for Course descript to start with Capital letter and lowercase (or for an A and space)
        #    if newClass and (line+9)<len(updated):
        #        newClass = bool(re.search("^[A-Z][a-z]",updated[line+9]) or re.search("^[A-Z]\s",updated[line+9]))
        #    else:
        #        newClass = False

            #If you are a new class title:
            if newClass:
                #Combine everything between finding a class at the beginning and another at the end
                output = '|'.join(details)
                file.write(output+"\n")
                #Once you write the class details, forget it
                details.clear()
                #Used to avoid tripping the elif to not write the beginning of a catalog
                start = True
                #Put the first thing in the array the Couse title (MATH 240)
                details.append(updated[line])
            #Once one class header is found, you can start recording information into details
            elif start:
                #This is potential for avoiding newlines? Kinda bootleg atm and would be better to remove comments from the getgo
                #if len(details) > 6:
                details.append(updated[line])

file.close()
pdfFileObj.close()
