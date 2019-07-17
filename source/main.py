from parse import parse
from parse import PDFtoTXT

from parse import getDataFromTxt
#from vectorize import vectorizePDFs
#from vectorize import machine
import time
import csv
import os

d = {}          #Dictionary of all classses
testing = False  #Grab PDF from small files (fast) or big files (slow)
school = "Valpo"
output = open('Terry.txt', 'w', encoding='utf-8')

#Current issues when 2+ files in folder, pdfminer doesnt like it
files = os.listdir('../FullPDFs/')
for x in files:
    filePath = "../%sPDFs/%s" % (("test" if testing else "full"), x)
    print(filePath)
    rawText = PDFtoTXT(filePath)
    cleanText = parse(rawText, "(?!FL)(?!IN)(?!NJ)[A-Z]{2,5}\s(?!2018)(?!4638)(?!2019)[0-9]{3,4}[A-Z]{0,1}")
    for classID in cleanText:
        if classID in d:
            d[classID] += cleanText[classID]
        else:
            d[classID] = cleanText[classID]
 #Write PDFS into CSV format
    with open("../output/Full/%s.csv" % x, "w", encoding='utf8', errors='ignore') as f:
        f.write('ClassID,Desc\n')
         #replace d with x if wanting reduce format
        for key in d:
                f.write('%s,"%s"\n'%(key,d[key]))
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
