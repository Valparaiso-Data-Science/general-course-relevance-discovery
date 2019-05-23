from parseValpo import getClasses
from parse import parse
import PyPDF2
from RD import findRelevant
import json

d = {}
testing = False

filePath = "../%sPDFs/Valpo.pdf" % ("test" if testing else "full")

pdfFileObj = open(filePath, 'rb')
doc = PyPDF2.PdfFileReader(pdfFileObj)
#dictionary = getClasses(pdfFileObj)
for i in doc.pages:
    #print(i.extractText())
    d.update(parse(i.extractText(),"[A-Z]{2,5}\s[0-9]{3,4}[A-Z]{0,1}"))
pdfFileObj.close()
#print(d)
print(findRelevant(d))


f= open("../output/output.json", "w")
json = json.dumps(findRelevant(d))
f.write(json)
f.close()



#x = ["\n".join("{}\t{}".format(k, v) for k, v in dictionary.items())]
