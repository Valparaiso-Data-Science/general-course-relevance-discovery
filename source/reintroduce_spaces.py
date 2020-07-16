"""
    XML parser that calls punct_split to correct spacing issues (words incorrectly concatenated together in the PDF->XML
    process via Adobe Acrobat).
"""

import sys
import xml.etree.ElementTree as ET

from punct_split import punct_split

# node trackers for progress print statement
current_element_num = 0
total_num_elements = 0

verbose = False


def clean_recursively(root):
    """
    At current node, reintroduce spaces into the text. Then proceed to child nodes.
    """
    if root.text is not None:
        root.text = punct_split(root.text)

        global current_element_num
        current_element_num += 1
        if verbose and current_element_num % 150 == 0:
            print("\rProcessed %.2f%% of all XML nodes." % (current_element_num * 100 / total_num_elements), end='')

    for child in root:
        clean_recursively(child)


def reintroduce_spaces(in_file_path, out_file_path=None):
    """
    Read XML file with spacing problems, correct its spaces, and write to a new XML file

    :param in_file_path: source XML with spacing problems
    :param out_file_path: destination XML with corrected spaces
    """

    # if no name for outfile given, use source name + "_spaced"
    if out_file_path is None:
        out_file_path = in_file_path[:in_file_path.rfind(".")] + "_spaced" + in_file_path[in_file_path.rfind("."):]

    # read xml file as a tree
    tree = ET.parse(in_file_path, ET.XMLParser(encoding="utf-8"))
    root = tree.getroot()

    # count how many total children and subchildren have information in their text field
    global total_num_elements
    total_num_elements = sum(1 if el.text else 0 for el in root.iter("*"))

    # reintroduce spaces at every node
    clean_recursively(root)

    if verbose and total_num_elements >= 150:
        print("\rProcessed 100.00%% of all XML nodes.")
    tree.write(out_file_path, encoding="utf8")

    return out_file_path


def main(argv):

    filename = "../fullPDFs/Carlow.xml"

    # if user specified another file as input
    if len(argv) > 1:
        filename = argv[1]

    reintroduce_spaces(filename)


if __name__ == "__main__":
    main(sys.argv)
