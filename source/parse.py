import re       #Regex
import csv      #CSV

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



def parse(text, regex):
    matches = list(re.finditer(regex, text))

    result  = {}
    lengthMatches = len(matches)
    for i,m in enumerate(matches):
            classID = m.group(0)
            startDesc = m.end()
            if i < lengthMatches-1:
                endDesc = matches[i+1].start()
            else:
                endDesc = len(text)-1
            if classID not in result:
                result[classID] = text[startDesc:endDesc]
            else:
                result[classID] += text[startDesc:endDesc]
    return result
'''
def parse(text,regex):
    indices = getIndices(text, regex)
    output = {}
    for i in indices:
        concatedText = ""
        for j in i:    
            concatedText += text[indices[i][j][0]:indices[i][j][1]]
        output[i] = concatedText
    return output
'''



#print(parse(text,"[A-Z]{2,5}\s[0-9]{3,4}[A-Z]{0,1}"))

