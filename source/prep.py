'''
    Handles preprocessing raw XML into a form that makes it possible to extract course titles and descriptions.
'''
import os
from progress.bar import Bar
import pandas as pd
import numpy as np
import re
def prepare():
    # make directories for intermediary and final data
    print("Preparing temporary data directory...")
    try:
        os.mkdir('../temp_data')
    except FileExistsError:
        print("../temp_data already exists")
    try:
        os.mkdir('../temp_data/TRIMMED')
    except FileExistsError:
        print("../temp_data/TRIMMED already exists. Clearing all files in it.")
        # clear folder of previous files
        if len(os.listdir('../temp_data/TRIMMED')) > 0:
            for file in Bar("Cleaning TRIMMED...").iter(os.listdir('../temp_data/TRIMMED')):
                os.unlink('../temp_data/TRIMMED/' + file)
    try:
        os.mkdir('../temp_data/superTrimmedPDFs')
    except FileExistsError:
        print("../temp_data/superTrimmedPDFs already exists. Clearing all files in it.")
        # clear folder of previous files
        if len(os.listdir('../temp_data/superTrimmedPDFs')) > 0:
            for file in Bar("Cleaning supertrimmmed...").iter(os.listdir('../temp_data/superTrimmedPDFs')):
                os.unlink('../temp_data/superTrimmedPDFs/' + file)
    try:
        os.mkdir('../courses')
    except FileExistsError:
        print("../courses already exists. Clearing all files in it.")
        # clear folder of previous files
        if len(os.listdir('../courses')) > 0:
            for file in Bar("Cleaning courses...").iter(os.listdir('../courses')):
                os.unlink('../courses/' + file)
def makeLineNumDict(csv_file_path): # maybe add a 'csv_file' as our input?
    # look for a csv file containing line number information
    #   (from which line to which line to trim) and gather the relevant
    #   information (filename, start line, end line) in a dictionary
    line_num_dict = {}
    try:
        cat_df = pd.read_csv(csv_file_path)
        for index, row in cat_df.iterrows():
            if (not np.isnan(row[1])) and (not np.isnan(row[2])):
                line_num_dict[row[0].lower()] = int(row[1]), int(row[2])
    except FileNotFoundError:
        print("CSV file with trimming line numbers not found.")
    return line_num_dict
def trimFile(in_path, out_path, filename, line_num_dict):
    """
    Write out a new file with content from source file that is only between the lines specified in line_num_dict
    :param in_path: source directory
    :param out_path: destination directory
    :param filename: the particular file
    :param line_num_dict: dictionary with keys represented by lowercase versions of filenames (no extension) and values
                        tuples of two numbers (start line and end line)
    """
    # if xml file
    if filename.endswith(".xml"):
       
        # # if information about at which lines to trim file, assign line numbers to `start` and `end`
        # if filename[:filename.rfind(".")].lower() in line_num_dict:
        #     start, end = line_num_dict[filename[:filename.rfind(".")].lower()]
        # new_file_lines = []
        with open(in_path + "/" + filename, "r") as f:
            lines = f.readlines()
        #     # if found information about line numbers, use it to trim out the lines
        #     if filename[:filename.rfind(".")].lower() in line_num_dict:
        #         new_file_lines = lines[start - 1:end]
        #     # otherwise just save the whole file
        #     else:
        #         new_file_lines = lines
        new_file_lines = lines
        new_filename = filename[:filename.rfind(".")] + "TRIMMED" + filename[filename.rfind("."):]
        with open(out_path + "/" + new_filename, "w") as f:
            f.writelines(new_file_lines)
    
def cleanXML(in_path, out_path, filename):
    """
    Removes unnecessary tags, as well as the contents of Figure tags.
    (do we need a more precise/elaborate description here?)
    :param in_path: source directory path (trimmed)
    :param out_path: destination directory path (supertrimmed)
    :param filename: name of the particular file in the directory
    """
    # Boolean to tell us if we are looking in a <Figure> element
    isFig = False
    nOFigs = 0
    # Opens the trimmed XML
    with open(in_path + "/" + filename, "r", encoding='utf-8') as file:
        # Makes a new XML file where the super trimming will be saved
        with open(out_path + "/" + filename.replace("TRIMMED", "SUPERTRIMMED"),
                  "w", encoding='utf-8') as newfile:
            # Writes an open <Part> tag. This allows us to parse the file as an XML later
            newfile.write("<Part>\n")
            if len(re.findall(r"Youngstown", filename)) == 1:
                newfile.write("<P>")
            # Loop through each line in the Trimmed XML
            for line in file:
                # turn file into string
                text = str(line)
                # Remove <Figure> tags and everything in them
                if len(re.findall(r"<Figure\b.*>", text)) == 1:
                    nOFigs += 1
                if len(re.findall(r"</Figure>", text)) == 1:
                    text = ""
                    nOFigs -= 1
                    if nOFigs == 0:
                        isFig = False
                if isFig:
                    text = ""
                if len(re.findall(r"<Figure\b.*>", text)) == 1:
                    text = re.sub(r"<Figure\b.*>", "", text)
                    isFig = True
                # remove Sect tags
                # text = re.sub("^<.*Span.*>", "", text)
                text = text.replace("</Sect>", "")
                text = text.replace("<Sect/>", "")
                text = re.sub(r"<Sect\b.*>", "", text)
                # remove Div tags
                text = text.replace("</Div>", "")
                text = re.sub(r"<Div\b.*>", "", text)
                # remove caption tags
                # text = text.replace("<Caption>","")
                # text = text.replace("</Caption>", "")
                # rmove part tags
                text = re.sub(r"<Part\b.*>", "", text)
                text = text.replace("</Part>", "")
                # remove Span tags
                text = re.sub(r"<Span\b.*>", "", text)
                text = text.replace("</Span>", "")
                text = text.replace("<Span/>", "")
                # remove story tags
                text = re.sub(r"<Story\b.*>", "", text)
                text = text.replace("</Story>", "")
                text = text.replace("<P>\n", "<P>")
                # remove bad utf-8 character
                text = text.replace(str(chr(65535)), "")
                # some files have improperly rendered ampersand; replace with XML-acceptable version
                text = text.replace("& ", "&amp; ")
                # get rid of tags like `<?xml version="1.0" encoding="UTF-8" ?>`
                text = re.sub(r"<[?!].*>", "", text)
                # Writes the processed line to the super trimmed XML
                newfile.write(text)
            # Closing our open <Part> tag so we don't get any errors
            newfile.write("</Part>\n")
