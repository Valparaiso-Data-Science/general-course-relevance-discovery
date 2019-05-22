import PyPDF2   #PDF Reader
import re       #Regex
import csv      #CSV

#Grab PDF and create outpute file
pdfFileObj = open("ValpoUni.pdf", 'rb')
pdf = PyPDF2.PdfFileReader(pdfFileObj)
file = open("Output.txt","w")

start = False   #Variable used to avoid writing everything before first class is found
details = []    #Array stuff inbetween courses
newClass = False
attempt1 = False
attempt2 = False
attempt3 = False
#Go through every page
for page in range(pdf.numPages):
    #Formating pdf into array of lines (has issue with newlines)
    pageObj = pdf.getPage(page)
    text = pageObj.extractText()
    updated = text.split("\n")
    #Go through every line
    for line in range(len(updated)):
        #print(repr(updated[line]))
        #Current fix to the newline issue, will be removed when fixed (but doesnt have to be)
        if updated[line] != " ":
            #Check for course level (MATH 240)
            newClass = bool(re.search("[A-Z]{2,5}\s[0-9]{3,4}[A-Z]{0,1}", updated[line]))
            #Check for course title (Intro to design)
            if newClass and (line+2)<len(updated):
                newClass = bool(re.search("^[A-Z][a-z]",updated[line+2]) or re.search("^[A-Z]\s",updated[line+2]))
            else:
                newClass = False
            if newClass and (line+6)<len(updated):
                newClass = bool(updated[line+6] == " " or updated[line+6] == "-" or updated[line+5] == "-")
            else:
                newClass = False

            #Format 1
            if newClass and (line+7)<len(updated) and bool(updated[line+3] == " " and updated[line+5] == " "):
                print("Attempt1: ",updated[line])
                newClass = bool(updated[line+5] == " " and updated[line+6] == " " and (re.search("^[A-Z][a-z]",updated[line+7])) or (re.search("^[A-Z]\s",updated[line+7])))
                #print(updated[line])
            else:
                attempt1 = True

            #Format 2
            if newClass and (line+8)<len(updated) and bool(re.search("[A-z]",updated[line+3]) and updated[line+6] == " "):
                print("Attempt2: ",updated[line])
                newClass = bool(updated[line+4] == " " and updated[line+6] == " " and updated[line+7] == " " and (re.search("^[A-Z][a-z]",updated[line+8]) or re.search("^[A-Z]\s",updated[line+8])))
            else:
                attempt2 = True

            #Format 3
            if newClass and (line+9)<len(updated) and (bool(re.search("-",updated[line+6])) or (re.search("-",updated[line+5]))):
                print("Attempt3: ",updated[line])
                newClass = bool(updated[line+8] == " " and updated[line+10] == " " and updated[line+11] == " " and (re.search("^[a-zA-z]",updated[line+12]) or re.search("^[A-Z]\s",updated[line+12])) or (updated[line+7] == " " and updated[line+8] == " " and updated[line+3] == " " and (re.search("^[a-zA-z]",updated[line+9]) or re.search("^[A-Z]\s",updated[line+9]))))
            else:
                attempt3 = True

            if attempt1 and attempt2 and attempt3:
                newClass = False
                attempt1 = False
                attempt2 = False
                attempt3 = False
            #if newClass and (line+8)<len(updated) and bool(updated[line+6]== " "):
            #    if newClass and bool(re.search(".",updated[line+3])):
            #        newClass = bool(re.search("^[A-Z][a-z]",updated[line+8]) or re.search("^[A-Z]\s",updated[line+8]))
            #    else:
            #        newClass = bool(re.search("^[A-Z][a-z]",updated[line+7]) or re.search("^[A-Z]\s",updated[line+7]))
            #else:
            #    newClass = False

            #Check for Course descript to start with Capital letter and lowercase (or for an A and space)
        #    if newClass and (line+9)<len(updated):
        #        newClass = bool(re.search("^[A-Z][a-z]",updated[line+9]) or re.search("^[A-Z]\s",updated[line+9]))
        #    else:
        #        newClass = False

            #If you are a new class title:
            if newClass:
                print("YESSSSSSSSS", updated[line])
                #Combine everything between finding a class at the beginning and another at the end
                output = '|'.join(details)
                file.write(output+"\n\n")
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

