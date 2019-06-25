from parse import parse
from parse import PDFtoTXT
#from vectorize import vectorizePDFs
#from vectorize import machine
from RD import findRelevant
import time
import csv
import os

d = {}          #Dictionary of all classses
testing = True  #Grab PDF from small files (fast) or big files (slow)
school = "Valpo"

#Current issues when 2+ files in folder, pdfminer doesnt like it
files = os.listdir('../TestPDFs/')
for x in files:
    filePath = "../%sPDFs/%s" % (("test" if testing else "full"), x)
    print(filePath)
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

#Write PDFS into CSV format
    with open("../output/Full/%s.csv" % x, "w", encoding='utf8', errors='ignore') as f:
        f.write('ClassID,Desc\n')
        #replace d with x if wanting reduce format
        for key in d:
            try:
                f.write('%s,"%s"\n'%(key,d[key]))
            except:
                print(key)
        d.clear()




#Basic Relevancy Discover
# x = findRelevant(d)
# with open("../output/Reduced%s.csv" % school, "w", encoding='utf8', errors='ignore') as f:
#     f.write('ClassID,Desc\n')
#     #replace d with x if wanting reduce format
#     for key in x:
#         try:
#             f.write('%s,"%s"\n'%(key,x[key]))
#         except:
#             print(key)
