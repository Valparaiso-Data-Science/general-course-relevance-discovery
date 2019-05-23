import PyPDF2   #PDF Reader
from parse import getClasses

pdfFileObj = open("C:/Users/cpacker/Desktop/general-course-relevance-discovery/testPDFs/ValpoTest.pdf", 'rb')
dictionary = getClasses(pdfFileObj)
pdfFileObj.close()
print("\n".join("{}\t{}".format(k, v) for k, v in dictionary.items()))
