from parseValpo import getClasses

pdfFileObj = open("C:/Users/cpacker/Desktop/general-course-relevance-discovery/testPDFs/ValpoTest.pdf", 'rb')
dictionary = getClasses(pdfFileObj)
pdfFileObj.close()
print(dictionary)
print("\n".join("{}\t{}".format(k, v) for k, v in dictionary.items()))
