import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import sys

def extractTextFromXMLBrown(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    test = root.findall("Div")
    df = pd.DataFrame(columns = ["Section", "Description"])
    for element in test:
        Ptags = element.findall("P")
        if(len(Ptags) > 2):
            df = df.append({"Section": Ptags[0].text, "Description": Ptags[1].text}, ignore_index=True)
    df.to_csv("./output.csv")

def extractTextFromXMLPurdue(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    test = root.findall("Part/Div")
    df = pd.DataFrame(columns = ["Section", "Description"])
    for element in test:
        Ptags = element.findall("P")
        df = df.append({"Section": Ptags[0].text, "Description": Ptags[1].text}, ignore_index=True)
    df.to_csv("./output.csv")