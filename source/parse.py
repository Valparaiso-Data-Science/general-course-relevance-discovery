import PyPDF2   #PDF Reader
import re       #Regex

def getClasses(fileObj):
    doc = PyPDF2.PdfFileReader(fileObj)
    start = False   #Variable used to avoid writing everything before first class is found
    details = []    #Array stuff inbetween courses
    newClass = False
    #If every attempt is true (meaning each attempt to check for a  new class failed) then newClass = False
    attempt1 = False
    attempt2 = False
    attempt3 = False
    dictionary = {} #Output

    #Go through every page
    for page in range(doc.numPages):
        #Formating pdf into array of numbers (has issue with newnumbers)
        pageObj = doc.getPage(page)
        text = pageObj.extractText()
        line = text.split("\n")
        for number in range(len(line)):
            #print(line[number])
            if line[number] != " ":
                #Check for course level (MATH 240)
                newClass = bool(re.search("[A-Z]{2,5}\s[0-9]{3,4}[A-Z]{0,1}", line[number]))

                #Check for course title ("Intro to Des", or "A Study of")
                if newClass and (number+2)<len(line):
                    newClass = bool(re.search("^[A-Z][a-z]",line[number+2]) or
                                    re.search("^[A-Z]\s",line[number+2]))
                else:
                    newClass = False
                if newClass and (number+6)<len(line):
                    newClass = bool(line[number+6] == " " or
                                    line[number+6] == "-" or line[number+5] == "-")
                else:
                    newClass = False

                #Format 1
                if newClass and (number+7)<len(line) and bool(line[number+3] == " " and line[number+5] == " "):
                    newClass = bool(line[number+5] == " " and line[number+6] == " " and (re.search("^[A-Z][a-z]",line[number+7])) or (re.search("^[A-Z]\s",line[number+7])))
                    #print(line[number])
                else:
                    attempt1 = True

                #Format 2
                if newClass and (number+8)<len(line) and bool(re.search("[A-z]",line[number+3]) and line[number+6] == " "):
                    newClass = bool(line[number+4] == " " and line[number+6] == " " and line[number+7] == " " and (re.search("^[A-Z][a-z]",line[number+8]) or re.search("^[A-Z]\s",line[number+8])))
                else:
                    attempt2 = True

                #Format 3
                if newClass and (number+9)<len(line) and (bool(re.search("-",line[number+6])) or (re.search("-",line[number+5]))):
                    newClass = bool(line[number+8] == " " and line[number+10] == " " and line[number+11] == " " and (re.search("^[a-zA-z]",line[number+12]) or re.search("^[A-Z]\s",line[number+12])) or (line[number+7] == " " and line[number+8] == " " and line[number+3] == " " and (re.search("^[a-zA-z]",line[number+9]) or re.search("^[A-Z]\s",line[number+9]))))
                else:
                    attempt3 = True

                if attempt1 and attempt2 and attempt3:
                    newClass = False
                    attempt1 = False
                    attempt2 = False
                    attempt3 = False

                #If you are a new class title:
                if newClass:
                    #Combine everything between finding a class at the beginning and another at the end
                    output = '|'.join(details)

                    if len(details)>2:
                        level = details.pop(0)
                        title = details.pop(0)
                        dictionary[level]={"Title": title, "Description":".".join(details)}
                        #d = {(details.pop(0):".".join(details)}
                        #dict.update(d)
                    #Once you write the class details, forget it
                    details.clear()
                    #Used to avoid tripping the elif to not write the beginning of a catalog
                    start = True
                    #Put the first thing in the array the Couse title (MATH 240)
                    details.append(line[number])
                #Once one class header is found, you can start recording information into details
                elif start:
                    #This is potential for avoiding newnumbers? Kinda bootleg atm and would be better to remove comments from the getgo
                    #if len(details) > 6:
                    details.append(line[number])
    return dictionary;
