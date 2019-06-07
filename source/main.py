from parse import parse
from parse import PDFtoTXT
from RD import findRelevant
import csv
import os

d = {}          #Dictionary of all classses
testing = False  #Grab PDF from small files (fast) or big files (slow)
school = "Brown"

#Will replace this with a loop of all files when ready
filePath = "../%sPDFs/%s.pdf" % (("test" if testing else "full"), school)
files = [f for f in os.listdir('../testPDFs/')]

#Convert PDF to txt file
text = PDFtoTXT(filePath)

#From the string of the entire pdf, grab all discovered classes using this function and this regex format
newClasses = parse(text,"[A-Z]{2,5}\s[0-9]{3,4}[A-Z]{0,1}")
#Go through dictionary and combine duplicates into 1 row
#   because our regex can only be so specific, and will have to include times when the description isn't mentioned but the class is
for classID in newClasses:
    if classID in d:
        d[classID] += newClasses[classID]
    else:
        d[classID] = newClasses[classID]

#If x is uncommented, will csv discovered relevant classses
#If x is commented, will csv all classes
with open("../output/output%ss.csv" % school, "w", encoding='utf8', errors='ignore') as f:
    f.write('ClassID,Desc\n')
    #replace d with x if wanting reduce format
    for key in d:
        try:
            f.write('%s,"%s"\n'%(key,d[key]))
        except:
            print(key)

x = findRelevant(d)
with open("../output/output%s.csv" % school, "w", encoding='utf8', errors='ignore') as f:
    f.write('ClassID,Desc\n')
    #replace d with x if wanting reduce format
    for key in x:
        try:
            f.write('%s,"%s"\n'%(key,x[key]))
        except:
            print(key)
