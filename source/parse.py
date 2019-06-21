import re       #Regex
import csv      #CSV

###PDFMINER###
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
import io
resource_manager = PDFResourceManager()
fake_file_handle = io.StringIO()
converter = TextConverter(resource_manager, fake_file_handle)
page_interpreter = PDFPageInterpreter(resource_manager, converter)

#parse is a function that, given a *string* of text, will pull out the class descriptions
def parse(text, regex):
    #clear the new lines
    #print(text)
    text = text.replace("\n","")

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
                result[classID] = text[startDesc:endDesc]
            else:
                result[classID] += text[startDesc:endDesc]
    return result

def PDFtoTXT(filePath):
    with open(filePath, 'rb') as fh:
        ###PDFMiner stuff
        for page in PDFPage.get_pages(fh,
                                        caching=True,
                                        check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
        converter.close()
        fake_file_handle.close()
        ###End of PDFMiner stuff
    return text




#print(parse(text,"[A-Z]{2,5}\s[0-9]{3,4}[A-Z]{0,1}"))
