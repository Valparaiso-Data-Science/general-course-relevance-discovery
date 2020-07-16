"""
    Utility for determining if XML files in a directory have word spacing problems (as a result of PDF->XML via Adobe
    Acrobat).

    Creates a csv file with features: total number of words, number of word-like strings that are 17 chars or longer,
    number of matches that resulted in meaningful words when split "splits", number of matches that did not result in
    meaningful words when split "unsplits", average word gain when splitting, and "bad spacing" – 0 if no known (or
    predicted) spacing errors and 1 if known (or predicted) spacing errors.

    In train mode, only computes these features for 32 files that are known to either have or not have spacing errors.
    Then trains ADALINE classifier on 2 features – log(num long word matches / total number of words) and average word
    gain – to be able to predict existence of spacing issue in any new files.

    In predict mode, uses the ADALINE classifier to determine if any new files have spacing issues.
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

# home-made, same directory
import adaline

# home-made, parent directory
sys.path.append("..")
from punct_split import punct_split, has_vowels

# load dictionary into spell checker
spell = enchant.Dict("en_US")

# load language model into tokenizer
nlp = spacy.load("en")

# specify path to temporary directory
TEMP_DIR = "temp"

KNOWN_OK_SPACING = {'UniofTexas.xml', 'ColgateUni.xml', 'UniOfChicago.xml', 'Alma.xml', 'Williamwoods.xml',
                    'NorthCentralMissouri.xml', 'TexasA&M.xml', 'ucat1920.xml', 'Pepperdine.xml', 'Purdue.xml',
                    'Northwestern.xml', 'Sagu.xml', 'UniversityofWestGeorgia.xml', 'framingham.xml', 'Grandview.xml',
                    'WilliamJewell.xml', 'SouthwestBaptist.xml', 'EastCentral.xml', 'Desales.xml', 'EastStroudsburg.xml',
                    'OregonUni.xml', 'NotreDame.xml', 'McKendree.xml', 'UniofNorthCarolina.xml', 'Smith.xml'}

KNOWN_BAD_SPACING = {"2011Cornell.xml", "Brown.xml", "Caldwell.xml", "Carlow.xml", "Denison.xml", "Pittsburgh.xml",
                     "Youngstown.xml"}


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
    XML DOM traversal utility – find matches at current node, then move on to child nodes
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

    name = file_path[(file_path.rfind('/') + 1):]

    with open(temp_dir + "/" + name + ".csv", "w") as f:
        f.write(name + "," +
                str(stats["total_words"]) + "," +
                str(stats["matches"]) + "," +
                str(stats["split"]) + "," +
                str(stats["unsplit"]) + "," +
                str(stats["word_gain"]))


def analyze_dir(dir_path, out_filename="diagnostic_results.csv", process_set=None, no_process_set=None, lazy=True):
    """
    Applies analyze_file_to_temp to each file in target dir and makes a csv table with the results of all files.

    :param dir_path: target directory with XML files to analyze
    :param out_filename: name of output csv file with results
    :param process_set: set of files to process
    :param no_process_set: set of files to avoid
    :param lazy: whether to skip processing for already processed files

    :return: list of files that can not be determined to have good or bad spacing upon first pass
                (first pass creates dataset for ADALINE training and relies on predetermined labels;
                files that are not labeled in advance will be processed in second pass, using trained ADALINE
                classifier)
    """

    all_dir_files = os.listdir(dir_path)

    # skip useless files
    ignorables = [".DS_Store"]
    for ignorable in ignorables:
        if ignorable in all_dir_files:
            all_dir_files.remove(ignorable)

    # if caller specified set of files to process, only keep files that are both in all_dir_files and in process_set
    if process_set:
        all_dir_files = list(process_set.intersection(all_dir_files))

    # if caller specified files not to process, remove them from list
    if no_process_set:
        all_dir_files = list(set(all_dir_files).difference(no_process_set))

    if lazy:
        try:
            already_processed = set(pd.read_csv(out_filename)["school"].values)
            all_dir_files = list(set(all_dir_files).difference(already_processed))
        except FileNotFoundError:
            pass

    if len(all_dir_files) == 0:
        return

    try:
        # make directory
        os.mkdir(TEMP_DIR)
    except FileExistsError:
        # if already exists, clean it up
        [os.remove(TEMP_DIR + "/" + file) for file in os.listdir(TEMP_DIR)]

    # call word spacing analysis on individual files in parallel (results are written to TEMP_DIR as individual files)
    joblib.Parallel(n_jobs=-1)(joblib.delayed(analyze_file_to_temp)(dir_path + "/" + filename, TEMP_DIR)
                               for filename in progress.bar.Bar('Diagnosing Spacing Errors').iter(all_dir_files))

    if (not lazy) or (not os.path.isfile(out_filename)) or (os.path.getsize(out_filename) == 0):
        with open(out_filename, "w") as writeable:
            # write first line of master file
            writeable.write("school,total words,matches,splits,unsplits,average word gain\n")

    # read each individual file and write the results to master file
    with open(out_filename, "a") as writeable:

        # loop over each temporary file
        for file in os.listdir(TEMP_DIR):

            with open(TEMP_DIR + "/" + file, "r") as readable:
                lines = readable.readlines()

                if len(lines) > 1:
                    raise RuntimeError("Something went wrong in %s: more than 1 line." % file)

                # write to the new file the info from the readable plus whether or not file has spacing issues
                writeable.write(lines[0] + "\n")

    # delete individual files in the temporary directory
    for deletable in os.listdir(TEMP_DIR):
        try:
            os.remove(TEMP_DIR + "/" + deletable)
        except FileNotFoundError:
            pass

    os.rmdir(TEMP_DIR)


def train_mode(diagnostic_filename="diagnostic_results.csv"):
    """
    Compute file statistics for known files for subsequent training. Write results to diagnostic_filename.
    """

    df = pd.read_csv(diagnostic_filename)
    bad_spacing = []

    for school in df["school"].values:
        if school in KNOWN_OK_SPACING:
            bad_spacing.append(0)
        elif school in KNOWN_BAD_SPACING:
            bad_spacing.append(1)
        else:
            raise RuntimeError("Training on school catalog %s with unknown spacing (that is, whether it's good or bad)."
                               % school)

    df["bad spacing"] = bad_spacing
    df.to_csv(diagnostic_filename, index=False)


def append_mode(diagnostic_filename="diagnostic_results.csv", adaline_param_filename="adaline_wts.npy"):
    """
    Compute statistics for directory which may include previously unknown files. Unknown files initially get a NaN in
    the column for 'bad spacing', which is then replaced by label predicted by ADALINE classifier.

    :param diagnostic_filename: name of output file with results
    :param adaline_param_filename: name of .npy file where trained ADALINE parameters are stored
    :return:
    """

    df = pd.read_csv(diagnostic_filename)

    # 1st feature: log of the ratio between long word (>=17 chars) matches and total number of words
    log_match_ratio = np.log(df["matches"].values / df["total words"].values)

    # 2nd feature: average word gain
    avg_word_gain = df["average word gain"].values

    # concatenate
    features = np.vstack((log_match_ratio, avg_word_gain)).T

    spacing_classifier = adaline.AdalineLogistic()
    spacing_classifier.wts = np.load(adaline_param_filename)

    # predict spacing for all files
    predicted_spacing = spacing_classifier.predict(features)

    # indices where prediction is actually necessary (i.e. spacing not previously labeled)
    nan_inds = df["bad spacing"].apply(np.isnan).values

    updated_spacing = df["bad spacing"].values
    updated_spacing[nan_inds] = predicted_spacing[nan_inds]
    df["bad spacing"] = updated_spacing.astype(int)

    df.to_csv(diagnostic_filename, index=False)


def wordsplit_diagnostic(target_dir_path, mode='full'):
    """
    Main method for determining files with good and bad spacing.

    :param mode: specifies what stages of training/predicting to be performed.
                    'full' – train on known files, predict unknown
                    'train' – only train on known files
                    'append' – only analyze new files and predict whether they have spacing issues
    """

    if mode == "full":
        analyze_dir(target_dir_path, process_set=KNOWN_BAD_SPACING.union(KNOWN_OK_SPACING), lazy=False)
        train_mode()

        analyze_dir(target_dir_path, lazy=True)
        append_mode()

    elif mode == "train":
        analyze_dir(target_dir_path, process_set=KNOWN_BAD_SPACING.union(KNOWN_OK_SPACING), lazy=False)
        train_mode()

    elif mode == "append":
        analyze_dir(target_dir_path, lazy=True)
        append_mode()

    else:
        raise RuntimeError("Mode not understood. Please use 'full', 'train', or 'append'.")


def main(argv):

    target_dir_path = "../../fullPDFs/"

    if len(argv) > 1:
        target_dir_path = argv[1]

    wordsplit_diagnostic(target_dir_path, mode='full')


if __name__ == "__main__":
    main(sys.argv)
