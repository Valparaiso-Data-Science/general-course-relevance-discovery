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
import progress.bar
import joblib
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

# specify path to temporary directory
TEMP_DIR = "temp"

KNOWN_BAD_SPACING = {"2011Cornell", "Brown", "Caldwell", "Carlow", "Denison", "Pittsburgh", "Youngstown"}


def split_gain(long_word, return_words=False):
    """
    Calculate word gain (number of meaningful words gained) after splitting a long string

    :param long_word:  word to be split
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


def analyze_file_to_temp(file_path, temp_dir):
    """
    Wrapper for analyze_file that writes results to a separate file in a temporary directory
    (written this way to allow for processing in parallel)

    :param file_path: path to file to analyze
    :param temp_dir: path to temporary directory to write analysis to
    """

    stats = analyze_file(file_path)

    name = file_path[(file_path.rfind('/') + 1):file_path.rfind('.')]

    with open(temp_dir + "/" + name + ".csv", "w") as f:
        f.write(name + "," +
                str(stats["total_words"]) + "," +
                str(stats["matches"]) + "," +
                str(stats["split"]) + "," +
                str(stats["unsplit"]) + "," +
                str(stats["word_gain"]))


def main(argv):

    target_dir_path = "../../fullPDFs/"

    if len(argv) > 1:
        target_dir_path = argv[1]

    ignorables = [".DS_Store"]
    all_xmls = os.listdir(target_dir_path)

    for ignorable in ignorables:
        if ignorable in all_xmls:
            all_xmls.remove(ignorable)

    print(all_xmls)

    # call word spacing analysis on individual files in parallel (results are written to TEMP_DIR as individual files)
    os.mkdir(TEMP_DIR)
    joblib.Parallel(n_jobs=-1)(
        joblib.delayed(analyze_file_to_temp)(target_dir_path + "/" + filename, TEMP_DIR)
        for filename in progress.bar.Bar('Diagnosing Spacing Errors').iter(all_xmls))

    # read each individual file and write the results to master file
    with open("diagnostic_results.csv", "w") as writeable:
        # write first line of master file
        writeable.write("school,total words,matches,splits,unsplits,average word gain,bad spacing\n")

        # loop over each temporary file
        for file in os.listdir(TEMP_DIR):
            # set to 1 if current file has spacing issues
            bad_spacing = 1 if file[:file.rfind(".")] in KNOWN_BAD_SPACING else 0

            with open(TEMP_DIR + "/" + file, "r") as readable:
                lines = readable.readlines()

                if len(lines) > 1:
                    raise RuntimeError("Something went wrong in %s: more than 1 line." % file)

                # write to the new file the info from the readable plus whether or not file has spacing issues
                writeable.write(lines[0] + "," + str(bad_spacing) + "\n")

    # delete individual files in the temporary directory
    for deletable in os.listdir(TEMP_DIR):
        try:
            os.remove(TEMP_DIR + "/" + deletable)
        except FileNotFoundError:
            pass

    os.rmdir(TEMP_DIR)


if __name__ == "__main__":
    main(sys.argv)
