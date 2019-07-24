import io
import re
import fileinput
import csv
import pandas
import numpy as np
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import sys
from pdfminer.layout import LTTextBoxHorizontal

def extractTextFromPDF(pdfPath):
    classPattern = re.compile(r'(^[A-Z]{2,5} [0-9]{2,5}.*\n$)')
    document = open(pdfPath, 'rb')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    courses = []
    descriptions = []
    for page in PDFPage.get_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        for element in layout:
            if(isinstance(element, LTTextBoxHorizontal)):
                for part in element:
                    if(classPattern.match(part.get_text())):
                        courses.append(part.get_text())
    print(len(courses), courses)

                
    #         if(isinstance(element, LTTextBoxHorizontal)):
    #             text = element.get_text()
    #             text = text.replace("\n", " ")
    #             if(classPattern.match(text)):
    #                 courses.append(text)
    #             else:
    #                 if(len(text) > 50):
    #                     descriptions.append(text)
    # df = pandas.DataFrame({"Course": courses, "Description": descriptions})
    # df.to_csv("./output.csv")
                
                
        
    # for page in PDFPage.get_pages(document, caching = True, check_extractable = True):
    #     interpreter.process_page(page)
    #     layout = device.get_result()
    #     for element in layout:
    #         print(type(element))

extractTextFromPDF(sys.argv[1])