import PyPDF2   #PDF Reader
import re       #Regex
import csv      #CSV

#Open PDF and convert to a string based on new lines
#(PyPDF acknowledges that pdf reading newlines is kinda wonky, natural)
#Cody uses this one for conveincience
pdfFileObj = open("ValpoTest.pdf", 'rb')

#Nate uses this one cause first one didnt work at first
#filePath = input("Please input the file: ")
#pdfFileObj = open(filePath, 'rb')

pdf = PyPDF2.PdfFileReader(pdfFileObj)

file = open("Output.txt","w")
start = False   #Variable used to avoid writing everything before first class is found
details = []    #Array of detail

#Go through every page
for page in range(pdf.numPages):
    pageObj = pdf.getPage(page)
    text = pageObj.extractText()
    updated = text.split("\n")
    #updated = filter(None, updated)
    #Go through every line
    for line in range(len(updated)):
        #print(repr(updated[line]))
        if updated[line] != " ":
            #See if the current line is a header (MATH 240)
            newClass = bool(re.search("[A-Z]{3,5}\s[0-9]{3,4}[A-Z]{0,1}", updated[line]))
            #TODO, the current 'updated' array has a bunch of empty strings, need to filter() them but revert back to an array to we can len(range()) it
            #if newClass and (line+2)<len(updated):
                #newClass = bool(re.search("^[A-Z]",updated[line+2]))
            if newClass:
                #First loop combines nothing, but after that details is an array of details about the class
                #| is for conveince so we see what each detail is being joined into output
                output = '|'.join(details)
                file.write(output+"\n")
                #Once you write the class details, forget it
                details.clear()
                #Once you find a class header, set to true
                start = True
                #print(updated[line])
                details.append(updated[line])
                #Once one class header is found, you can start recording information
            elif start:
                #if len(details) > 6:
                details.append(updated[line])

file.close()
pdfFileObj.close()
