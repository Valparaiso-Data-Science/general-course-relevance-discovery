import PyPDF2
import re


#PDF AND OUTPUT PREP
#OUTPUT WILL BE EITHER ALL CLASSES OR ALL DATA SCIENCE RELAVENT CLASSES (DEPENDING HOW WE CAN DO THIS)
filePath = input("Please input the file: ")
pdfFileObj = open(filePath, 'rb')
pdf = PyPDF2.PdfFileReader(pdfFileObj)
file = open("Output.txt","w")

#Go through every page
#for page in range(pdfReader.numPages):
pageObj = pdf.getPage(0)

text = pageObj.extractText()

#this regex grabs 3-4 capital letters, a space, and 3-4 numbers
classCodeRegex = "[A-Z]{3,4}\s[0-9]{3,4}"



for line in text:
    if re.search(classCodeRegex, line):
        print(line)
print(re.findall(classCodeRegex, text))


file.write(pageObj.extractText())
file.close()
pdfFileObj.close()
