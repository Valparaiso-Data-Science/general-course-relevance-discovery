from parseValpo import getClasses
from parse import parse
import PyPDF2
from RD import findRelevant
import json
import csv

d = {}
testing = False
school = "Valpo"

filePath = "../%sPDFs/%s.pdf" % (("test" if testing else "full"), school)

pdfFileObj = open(filePath, 'rb')
doc = PyPDF2.PdfFileReader(pdfFileObj)
#dictionary = getClasses(pdfFileObj)
for i in doc.pages:
    #print(i.extractText())
    newClasses = parse(i.extractText(),"[A-Z]{2,5}\s[0-9]{3,4}[A-Z]{0,1}")
    for classID in newClasses:
        if classID in d:
            d[classID] += newClasses[classID]
        else:
            d[classID] = newClasses[classID]
pdfFileObj.close()

x = findRelevant(d)
with open("../output/output%s.csv" % school, "w") as f:
    f.write('ClassID,Desc\n')
    for key in x:
        f.write('%s,"%s"\n'%(key,x[key]))


#for x in findRelevant(d):
#    print(x)
#f= open("../output/output%s.csv" % school, "w")


#json = json.dumps(findRelevant(d))

#f.write(json)
#f.close()



#x = ["\n".join("{}\t{}".format(k, v) for k, v in dictionary.items())]
