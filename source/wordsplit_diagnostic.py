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
import numpy as np

# home-made
from punct_split import punct_split, has_vowels

# load dictionary into spell checker
spell = enchant.Dict("en_US")

# load language model into tokenizer
nlp = spacy.load("en")

total_matches = 0
total_unsplit = 0
total_split = 0
total_word_gain = []


def split_gain(long_word, return_words=False):
    """
    Calculate word gain (number of meaningful words gained) after splitting a long string

    :param return_words: whether to return the list of resulting split words. default=False
    :return: number of words gained
            (if return_words) list of strings: split_words
    """

    gain = 0

    split_words = punct_split(long_word).split(" ")

    if len(split_words) < 2:
        return gain if not return_words else gain, split_words

    for word in split_words:
        # a word is gained if 3 conditions passed: 1. pass spellcheck. 2. have vowels. 3. not be 'a' or 'o'
        gain += (spell.check(word) and has_vowels(word) and word not in {"a", "A", "o", "O"})

    return gain if not return_words else gain, split_words


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
                word_gain = (0, None)

                if not is_word:
                    word_gain = split_gain(match, return_words=True)

                print(f"{local_counter}. {match} -> is_word? {is_word}. word gain: {word_gain}")

                local_counter += 1

                global total_matches, total_split, total_unsplit, total_word_gain

                # account for whether word is splittable or unsplittable
                if word_gain[0] != 0:
                    total_split += 1
                else:
                    total_unsplit += 1

                total_word_gain.append(word_gain[0])
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

    global total_matches, total_split, total_unsplit, total_word_gain
    print("\nTotal matches: %d." % total_matches)
    print("Total split: %d." % total_split)
    print("Total unsplit: %d." % total_unsplit)

    print("Average word gain: %.2f" % (np.mean(total_word_gain)))

if __name__ == "__main__":
    main(sys.argv)
