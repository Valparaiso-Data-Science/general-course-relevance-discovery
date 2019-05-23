import re       #Regex
import csv      #CSV


#text is just some sample text to test parse() on
text = '''
ENT 100 Introduction to Entrepreneurship 3 Cr.
An interdisciplinary survey course covering all dimensions of starting and operating a new business venture.
Students will analyze and investigate the current trends and opportunities in entrepreneurship. Topics include
entrepreneurship theory, opportunity recognition, the entrepreneurial process, entrepreneurship in a
corporate context, the characteristics of entrepreneurs, market assessment, and entrepreneurial careers.

ENT 200 Creativity and Innovation 3 Cr.
An examination of the techniques and processes of innovation and creativity that lead to new business
development as an independent new venture or in existing organizations. Exposure to techniques, concepts,
and methods for managing the creative process in individual and group contexts with emphasis on
accountability for creative quality. Lectures, experiential learning, discussions, and guest speakers.

ENT 330 Business Planning and Venture Finance 3 Cr.
A survey course focusing on development of business plans and raising capital. The components of a business
plan are covered, including the research process required to gather necessary information. Sources of seed
and growth capital are covered, as well as financial challenges faced by the entrepreneur. Students develop a
comprehensive business plan that is presented to a panel of entrepreneurs and bankers.

'''


#parse is a function that, given a string of text, will pull out the class descriptions
def parse(text, regex):
    text = text.replace("\n","")
    #create a list of match objects that each contain the indices of the matches
    matches = list(re.finditer(regex, text))

    result  = {}
    
    #computing the length of matches here for that sweet optimization
    lengthMatches = len(matches)
    
    #loop through the match objects, enumerate makes it so the index is available
    for i,m in enumerate(matches):
            #classId is set too the current matches entire string
            classID = m.group(0)
            #the start of the classes description starts with the END of the ClassID
            startDesc = m.end()
            
            
            if i < lengthMatches-1: #if we are not on the last item
                #the end of the description will be at the start of the next ClassID found
                endDesc = matches[i+1].start()
            else: 
                #otherwise the description ends at the end of the text
                endDesc = len(text)-1
                
                #if the class has not been found before, add it to the dict
                #otherwise append the found descriptions together
            if classID not in result:
                result[classID] = text[startDesc:endDesc]
            else:
                result[classID] += text[startDesc:endDesc]
                #print(result[classID])
            #print(classID + ": " + str(startDesc) + "," + str(endDesc))
            #print(text[startDesc:endDesc])
    return result




#print(parse(text,"[A-Z]{2,5}\s[0-9]{3,4}[A-Z]{0,1}"))

