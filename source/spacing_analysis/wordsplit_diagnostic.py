"""
    Simple test that finds long words (17 characters and longer) and computes some statistics about them that help us
    understand whether the long words are legitimate words or incorrectly spaced phrases
"""

# pre-made
import sys
import os
import re
import spacy
import enchant
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from lxml import etree

# load home-made module from parent directory
sys.path.append("..")
from punct_split import punct_split, has_vowels

# load dictionary into spell checker
spell = enchant.Dict("en_US")

# load language model into tokenizer
nlp = spacy.load("en")


def split_gain(long_word, return_words=False):
    """
    Calculate word gain (number of meaningful words gained) after splitting a long string

    :param return_words: whether to return the list of resulting split words. default=False
    :return: number of words gained
            (if return_words) list of strings: split_words
    """

    gain = 0

    split_words = punct_split(long_word).split(" ")

    if len(split_words) < 2 and return_words:
        return gain, split_words
    elif len(split_words) < 2:
        return gain

    for word in split_words:
        # a word is gained if 3 conditions passed: 1. pass spellcheck. 2. have vowels. 3. not be 'a' or 'o'
        gain += (spell.check(word) and has_vowels(word) and word not in {"a", "A", "o", "O"})

    if return_words:
        return gain, split_words
    else:
        return gain


def traverse_node(root, pattern, match_stack, stats):
    """
    Find matches at current node, then move on to child nodes
    """

    if root.text is not None:
        # total number of words in current node text
        num_words = len(root.text.split())
        stats["total_words"] += num_words

        matches = pattern.findall(root.text)

        if matches:
            for match in matches:
                is_word = spell.check(match)
                word_gain = 0

                if not is_word:
                    word_gain = split_gain(match)

                if type(word_gain) != int:
                    print("ouch")

                # account for whether word is splittable or unsplittable
                if word_gain != 0:
                    stats["split"] += 1
                else:
                    stats["unsplit"] += 1

                stats["matches"] += 1
                stats["word_gain"].append(word_gain)

    for child in root:
        traverse_node(child, pattern, match_stack, stats)


def analyze_file(file_path):
    """
    Package file analysis into one method that returns the results.

    :param file_path: path to the analyzable file
    :return: (tuple) catalog name, proportion of splits, average word gain
    """

    stats = {"total_words": 0, "matches": 0, "split": 0, "unsplit": 0, "word_gain": []}

    # read xml file as a tree (with permissive parser)
    tree = ET.parse(file_path, etree.XMLParser(recover=True))
    root = tree.getroot()

    pattern = re.compile(r"\b[A-Za-z'][A-Za-z']{17,}\b")

    match_stack = []

    # traverse all nodes recursively and collect pattern matches
    traverse_node(root, pattern, match_stack, stats)

    # replace list of word gain by match with average word gain
    stats["word_gain"] = np.mean(stats["word_gain"])

    return stats


def main(argv):

    target = "../fullPDFs/Carlow.xml"

    if len(argv) > 1:
        target = argv[1]

    ignorables = [".DS_Store", "Toy.xml"]
    all_xmls = os.listdir("../fullPDFs")

    for ignorable in ignorables:
        all_xmls.remove(ignorable)

    print(all_xmls)

    schools = np.empty(len(all_xmls)).astype(object)
    total_words = np.empty(len(all_xmls)).astype(int)
    matches = np.empty(len(all_xmls)).astype(int)
    splits = np.empty(len(all_xmls)).astype(int)
    unsplits = np.empty(len(all_xmls)).astype(int)
    avg_wordgain = np.empty(len(all_xmls)).astype(np.float64)

    for i in range(len(all_xmls)):
        print("\rProcessing: %d\\%d" % ((i+1), len(all_xmls)), end='')

        target = all_xmls[i]

        stats = analyze_file("../fullPDFs/" + target)

        schools[i] = target[(target.rfind('/')+1):target.rfind('.')]
        total_words[i] = stats["total_words"]
        matches[i] = stats["matches"]
        splits[i] = stats["split"]
        unsplits[i] = stats["unsplit"]
        avg_wordgain[i] = stats["word_gain"]

    print("\rDone.")

    bads = np.empty(len(schools)).astype(int)
    bad_space_inds = [np.where(schools == bad_spaced)[0] for bad_spaced in ["2011Cornell", "Brown", "Caldwell",
                                                                            "Carlow", "Denison", "Pittsburgh",
                                                                            "Youngstown"]]
    for ind in bad_space_inds:
        bads[ind] = 1

    df = pd.DataFrame()

    df["school"] = schools
    df["total words"] = total_words
    df["matches"] = matches
    df["splits"] = splits
    df["unsplits"] = unsplits
    df["average word gain"] = avg_wordgain
    df["bad spacing"] = bads

    df.to_csv("wordgain_analysis.csv", index=False)


if __name__ == "__main__":
    main(sys.argv)
