"""
    Simple test that traverses an XML tree and prints text that contains words 17 characters and longer, as well as
    the matches themselves)
"""

import sys
import re
import xml.etree.ElementTree as ET

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

    target = "../fullPDFs/Carlow.xml"

    if len(argv) > 1:
        target = argv[1]

    # read xml file as a tree
    tree = ET.parse(target, ET.XMLParser(encoding="utf-8"))
    root = tree.getroot()

    pattern = re.compile(r"\b[A-Za-z'][A-Za-z']{17,}\b")

    match_stack = []

    # traverse all nodes recursively and collect pattern matches
    traverse_node(root, pattern, match_stack)

    global total_matches
    print("\nTotal matches: %d." % total_matches)


if __name__ == "__main__":
    main(sys.argv)
