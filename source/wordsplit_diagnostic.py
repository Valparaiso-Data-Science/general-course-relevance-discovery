"""
    Simple test that finds long words (17 characters and longer) and computes some statistics about them that help us
    understand whether the long words are legitimate words or incorrectly spaced phrases
"""

# pre-made
import sys
import re
import spacy
import enchant
import xml.etree.ElementTree as ET

# home-made
from punct_split import punct_split

# load dictionary into spell checker
spell = enchant.Dict("en_US")

# load language model into tokenizer
nlp = spacy.load("en")

total_matches = 0


def split_gain(long_word, return_words=False):
    """
    Calculate word gain (number of meaningful words gained) after splitting a long string

    :param return_words: whether to return the list of resulting split words. default=False
    :return: number of words gained
            (if return_words) list of strings: split_words
    """

    gain = 0

    split = punct_split(long_word).split(" ")

    for word in split:
        gain += spell.check(word)

    if return_words:
        return gain, split
    else:
        return gain


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

            # counter for number of matches in a given text node
            local_counter = 1

            for match in matches:
                is_word = spell.check(match)
                print("%d. %s -> is_word? %s" % (local_counter, match, is_word))

                local_counter += 1

                global total_matches
                total_matches += 1

            print()

    for child in root:
        traverse_node(child, pattern, match_stack)


def main(argv):

    # target = "../fullPDFs/Carlow.xml"
    #
    # if len(argv) > 1:
    #     target = argv[1]
    #
    # # read xml file as a tree
    # tree = ET.parse(target, ET.XMLParser(encoding="utf-8"))
    # root = tree.getroot()
    #
    # pattern = re.compile(r"\b[A-Za-z'][A-Za-z']{17,}\b")
    #
    # match_stack = []
    #
    # # traverse all nodes recursively and collect pattern matches
    # traverse_node(root, pattern, match_stack)
    #
    # global total_matches
    # print("\nTotal matches: %d." % total_matches)

    split_gain("endocrinology", return_words=True)


if __name__ == "__main__":
    main(sys.argv)
