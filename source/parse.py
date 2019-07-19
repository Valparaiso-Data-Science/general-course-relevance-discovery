import re       
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


import io
import os


#parse is a function that, given a *string* of text, will pull out the class descriptions
def parse(text, regex):
    #clear the new lines
    #print(text)
    text = text.replace("\n","")
    # file1 = open("fullpdftotext.txt","wb")
    # file1.write(text.encode('ascii','ignore'))
    # file1.close()
    #create a list of match objects that each contain the indices of the matches
    matches = list(re.finditer(regex, text))

    result  = {}

    #computing the length of matches here for that sweet optimization
    lengthMatches = len(matches)

    #loop through the match objects, enumerate makes it so the index is available
    for i,m in enumerate(matches):

            #classId is set too the current match's string
            classID = m.group(0)
            #the start of the current class's description starts with the END of the ClassID
            startDesc = m.end()

            #if we are not on the last item,
            #the end of the description will be at the start of the next ClassID found
            #otherwise the description ends at the end of the text
            if i < lengthMatches-1:
                endDesc = matches[i+1].start()
            else:
                endDesc = len(text)-1
            """
            @terry, as you can see this check is does twice, once on the current page
            once after we are done finding the current page.
            This is bad, see if there's a way to do this check as a function or
            if there's a better way to do this
            """
            #if the class has not been found before, add it to the dict
            #otherwise append the found descriptions together
            if classID not in result:
                result[classID] = [text[startDesc:endDesc]]
            else:
                result[classID].append(text[startDesc:endDesc])
            
    for i in result:
        while True:
            longestEntry = max(result[i],key=len)
            print(longestEntry)
            oneEntry = len(result[i]) == 1
            maxTooLong = len(longestEntry) > 1000
            maxContains_x0c = bool(re.search("\\x0c",longestEntry))
            
            if (maxTooLong or maxContains_x0c) and not oneEntry:
                result[i].remove(max(result[i],key=len))
                continue
            else:
                result[i] = longestEntry
                break
            
            
    #print(result)
    return result


def PDFtoTXT(filePath):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(filePath, 'rb') as fh:
        ###PDFMiner stuff
        for page in PDFPage.get_pages(fh,caching=True,check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
        converter.close()
        fake_file_handle.close()
        ###End of PDFMiner stuff
    return text

def parseDirectory(path):
    #our use case will be just "../fullPDFs/", however we will likly run this on others
    d = {}
    files = os.listdir(path)
    for x in files:
        print(x)
        text = PDFtoTXT(path+x)
        print("texted: " + x)
        #From the string of the entire pdf, grab all discovered classes using this function and this regex format
        newClasses = parse(text,"(?!FL)(?!IN)(?!NJ)[A-Z]{2,5}\s(?!2018)(?!4638)(?!2019)[0-9]{3,4}[A-Z]{0,1}")
        print("found classes in: " + x)
        #Go through dictionary and combine duplicates into 1 row
        #   because our regex can only be so specific, 
        #   and will have to include times when the description isn't mentioned but the class is
        for classID in newClasses:
            d[(x,classID)] = newClasses[classID]
                
    return d
