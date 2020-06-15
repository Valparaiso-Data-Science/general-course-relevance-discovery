"""
    XML parser that uses the wordninja package to reintroduce spaces into words that are crammed together.
"""

import sys
import wordninja

import xml.etree.ElementTree as ET
from lxml import etree
#from punct_split import punct_split

# node trackers for progress print statement
current_element_num = 0
total_num_elements = 0

# keep this boolean True for now – it applies simple wordninja spacing; we'll make fancy spacing default later,
# when we're done implementing it
wordninja_split = True

if wordninja_split:
    split = lambda text: " ".join(wordninja.split(text))
else:
    split = punct_split


def clean_recursively(root):
    """
    At current node, reintroduce spaces into the text. Then proceed to child nodes.
    """
    if root.text is not None:
        root.text = split(root.text)

        global current_element_num
        current_element_num += 1
        if current_element_num % 150 == 0:
            print("\rProcessed %.2f%% of all XML nodes." % (current_element_num * 100 / total_num_elements), end='')

    for child in root:
        clean_recursively(child)


def main(argv):
    data_in_path = "../source/superTrimmedPDFs/"
    data_out_path = "../source/superTrimmedPDFs/"

    filename = argv

    # if user specified another file as input
    '''
    if len(argv) > 1:
        filename = argv[1]
    '''
    # read xml file as a tree
    tree = ET.parse(data_in_path + str(filename), etree.XMLParser(recover=True))
    root = tree.getroot()

    # count how many total children and subchildren have information in their text field
    global total_num_elements
    total_num_elements = sum(1 if el.text else 0 for el in root.iter("*"))

    # reintroduce spaces at every node
    clean_recursively(root)

    if total_num_elements >= 150:
        print("\rProcessed 100.00%% of all XML nodes.")

    tree.write(data_out_path + "wordninjaed_" + filename, encoding="utf8")


if __name__ == "__main__":
    main(sys.argv)
