#THINGS TO ADD
    #Once we regex for the "MATH 240" stuff, see if there is a way to check what the next line is
    #we want to see if the next letter is a capital (small detail but will remove a lot of mistake)
    #This would solve some of the cases in which prerequisites are listed in the description, they dont typically have a space or capital letter so we could keep them in the description instead of thinking it is a new class

    #Need to find a way to make an end case, some schools have classes split between departments,
    #we don't want to record every page between Arts & Sci to Nursing, we need a way to know this is extractText
    #easiest way I can think of is over x over the average course description (they only get 200 characters big or something around that, right?)

    #Output to a csv or put into a data frame,
    #Need to be able to access the indexs so everytime we see a new class, we check if we already documented stuff about it
    #If it is a duplicate we want to append to end of the dataframe so we don't have duplicates

import PyPDF2   #PDF Reader
import re       #Regex
import csv      #CSV

#Open PDF and convert to a string based on new lines
#(PyPDF acknowledges that pdf reading newlines is kinda wonky, natural)

#Cody uses this one for conveincience
#pdfFileObj = open("ValpoTest.pdf", 'rb')

#Nate uses this one cause first one didnt work at first
filePath = input("Please input the file: ")
pdfFileObj = open(filePath, 'rb')

pdf = PyPDF2.PdfFileReader(pdfFileObj)

file = open("Output.txt","w")
start = False   #Variable used to avoid writing everything before first class is found
details = []    #Array of detail

#Go through every page
for page in range(pdf.numPages):
    pageObj = pdf.getPage(page)
    text = pageObj.extractText()
    updated = text.split("\n")
    updated = filter(None, updated)
    #Go through every line
    for line in updated:
        if line != " ":
            #print(repr(line))
            #See if the current line is a header (MATH 240)
            newClass = bool(re.search("[A-Z]{3,5}\s[0-9]{3,4}", line))
                #and (not re.search('ANNOUNCEMENTS', line)) and (not re.search('scholarship', line)))
            if newClass:
                #First loop combines nothing, but after that details is an array of details about the class
                #| is for conveince so we see what each detail is being joined into output
                output = '|'.join(details)
                file.write(output+"\n")
                #Once you write the class details, forget it
                details.clear()
                #Once you find a class header, set to true
                start = True
                details.append(line)
                #Once one class header is found, you can start recording information
            elif start:
                details.append(line)

file.close()
pdfFileObj.close()
