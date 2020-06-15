"""
    Simple test that traverses an XML tree and prints text if it contains a specific pattern (e. g. capital letters
    in the middle of the word)
"""

import sys
import re
import xml.etree.ElementTree as ET
from lxml import etree


total_matches = 0


def traverse_node(root, pattern, match_stack):
    """
    Find matches at current node, then move on to child nodes
    """
    if root.text is not None:
        matches = pattern.findall(root.text)

        if matches:
            print("Full text:")
            print(root.text)
            print("Matches:")

            counter = 1
            for match in matches:
                print("%d. %s" % (counter, match))
                counter += 1

                global total_matches
                total_matches += 1

            print()

    for child in root:
        traverse_node(child, pattern, match_stack)


def main(argv):

    patterns = [r"[a-z][A-Z]",          # midword capitals
                r"\b[A-Za-z'][A-Za-z']{17,}\b"]  # words that are too long (possibly wrongly spaced during PDF->XML)

    target = "../fullPDFs/Carlow.xml"

    if len(argv) > 1:
        target = argv[1]

    # read xml file as a tree
    parser = etree.XMLParser(recover=True)
    tree = ET.parse(target, parser=parser)
    root = tree.getroot()

    pattern = re.compile(patterns[1])

    match_stack = []

    # traverse all nodes recursively and collect pattern matches
    traverse_node(root, pattern, match_stack)

    global total_matches
    print("\nTotal matches: %d." % total_matches)


if __name__ == "__main__":
    main(sys.argv)
