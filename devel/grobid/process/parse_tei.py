import sys
import re
from xml.etree import ElementTree as ET

total_matches = 0
pattern = re.compile(r"[A-Z]{2,6}\s{,1}-{,1}[0-9]{2,6}")


def traverse_node(root, pattern):
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
        traverse_node(child, pattern)


def main(argv):

    target = "../data/out/Alma.tei.xml"

    if len(argv) > 1:
        target = argv[1]

    # read xml file as a tree
    tree = ET.parse(target, ET.XMLParser(encoding="utf-8"))
    root = tree.getroot()

    # traverse all nodes recursively and collect pattern matches
    global pattern  # indicate that we're using pattern as defined at the top of this file
    traverse_node(root, pattern)

    global total_matches
    print("\nTotal matches: %d." % total_matches)


if __name__ == "__main__":
    main(sys.argv)
