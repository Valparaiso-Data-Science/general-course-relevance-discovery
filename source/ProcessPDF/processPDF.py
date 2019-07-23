import io
import re
import fileinput
import csv
import pandas
import numpy as np
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

def extractTextFromPdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
 
        text = fake_file_handle.getvalue()
 
    # close open handles
    converter.close()
    fake_file_handle.close()
    
    with open("./textdump.txt", "w+") as f:
        f.write(text)
    if text:
        return text


def cleanText(text):
    text = text.replace("\n", "")
    text = text.replace(',', '')
    prereqs = np.array(re.findall(r'((?:Prerequisite[s]?.*?\.))', text))
    for prereq in prereqs:
        text = text.replace(prereq, "")
    reMatches = np.unique(np.array(re.findall(r'((?:[A-Z]{2,5} [0-9]{2,5}[A-Z]?)).*?(?:Prerequisites?:?|(?=[A-Z]{2,5} [0-9]{2,5}))', text)))
    for match in reMatches:
        text = text.replace(match, ("\n%s" % match))
    if text:
        return text

def removeOutliers(text):
    lines = text.split("\n")
    validLines = [] #?
    for line in lines:
        if(len(line) > 300 and (re.findall(r'([A-Z]{2,5} [0-9]{2,5}[A-Z]?)\.?', line))): #?
            validLines.append(line)
    return "\n".join(validLines)

def extractDataToCSV(courses):
    csvFile = open("output.csv", "w+")
    csvFile.write("SECTION, TITLE, DESCRIPTION\n")
    lines = np.array(re.findall(r'(?P<SECTION>[A-Z]{2,5} [0-9]{2,5}[A-Z]?[.]?)(?P<TITLE>[^.]+\.)(?P<DESCRIPTION>.*\n)', courses))
    for line in lines:
        try:
            csvFile.write("%s,%s,%s" % (line[0], line[1], line[2]))
        except(UnicodeEncodeError):
            print("error")
    


def main():
    file = open('wordsTestOutput.txt', 'w+', encoding='utf-8', errors = "ignore")
    pdfText = extractTextFromPdf("./testPDFs/Brown.pdf")
    cleanedText = cleanText(pdfText)
    formatted = removeOutliers(cleanedText)
    extractDataToCSV(formatted)
    file.write(formatted)
    
main()