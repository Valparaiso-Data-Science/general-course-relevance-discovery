"""
    XML parser that uses the wordninja package to reintroduce spaces into words that are crammed together.
"""

import sys
import xml.etree.ElementTree as ET

from punct_split import punct_split

# node trackers for progress print statement
current_element_num = 0
total_num_elements = 0


def clean_recursively(root):
    """
    At current node, reintroduce spaces into the text. Then proceed to child nodes.
    """
    if root.text is not None:
        root.text = punct_split(root.text)

        global current_element_num
        current_element_num += 1
        if current_element_num % 150 == 0:
            print("\rProcessed %.2f%% of all XML nodes." % (current_element_num * 100 / total_num_elements), end='')

    for child in root:
        clean_recursively(child)


def main(argv):
    '''
    filename = "../fullPDFs/Carlow.xml"

    # if user specified another file as input
    if len(argv) > 1:
        filename = argv[1]
    '''
    filename = argv
    # read xml file as a tree
    tree = ET.parse(filename, ET.XMLParser(encoding="utf-8"))
    root = tree.getroot()

    # count how many total children and subchildren have information in their text field
    global total_num_elements
    total_num_elements = sum(1 if el.text else 0 for el in root.iter("*"))

    # reintroduce spaces at every node
    clean_recursively(root)

    if total_num_elements >= 150:
        print("\rProcessed 100.00%% of all XML nodes.")
    tree.write(filename[:filename.rfind(".")] + "_wordninjaed" + filename[filename.rfind("."):], encoding="utf8")


if __name__ == "__main__":
    main(sys.argv)
