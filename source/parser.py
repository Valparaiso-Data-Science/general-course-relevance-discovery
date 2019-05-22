import re       #Regex
import csv      #CSV


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
            result[classID] = (startDesc,endDesc)
    return result






