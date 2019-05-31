from parse import parse
import PyPDF2
from RD import findRelevant
import json
import csv

#PDF Miner Initializations
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
import io

resource_manager = PDFResourceManager()
fake_file_handle = io.StringIO()
converter = TextConverter(resource_manager, fake_file_handle)
page_interpreter = PDFPageInterpreter(resource_manager, converter)
#End PDF Miner Intitialization
d = {}
testing = False #testing determines if we are working in the testPDF or the fill pdf
school = "Valpo" #school is the filename of the pdf we want, make sure its in the directory you are working in

filePath = "../%sPDFs/%s.pdf" % (("test" if testing else "full"), school)

#pdfFileObj = open(filePath, 'rb')
#doc = PyPDF2.PdfFileReader(pdfFileObj)

"""
@terry
Currently this program runs on each page of the PDF object, and determines how
to add to the dict after parsing the page. This is bad.
Can you make it so that we just call parse() on a pdf object and it spits out
a dict with all the classes.

"""
with open(filePath, 'rb') as fh:
    for page in PDFPage.get_pages(fh,
                                    caching=True,
                                    check_extractable=True):
        page_interpreter.process_page(page)

    text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()
newClasses = parse(text,"[A-Z]{2,5}\s[0-9]{3,4}[A-Z]{0,1}")
#for i in doc.pages: #for each page in the document
    #parse out the classes found
#    newClasses = parse(i.extractText(),"[A-Z]{2,5}\s[0-9]{3,4}[A-Z]{0,1}")

    #if the class is in the dict, append the class,
    #otherwise just create the class
for classID in newClasses:
    if classID in d:
        d[classID] += newClasses[classID]
    else:
        d[classID] = newClasses[classID]
#pdfFileObj.close()


#Uncomment this for reduced csv of relavant
x = findRelevant(d)
with open("../output/output%s.csv" % school, "w", encoding='utf8', errors='ignore') as f:
    f.write('ClassID,Desc\n')
    #replace d with x if wanting reduce format
    for key in x:
        try:
            f.write('%s,"%s"\n'%(key,x[key]))
        except:
            print(key)
""
