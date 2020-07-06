import os
from progress.bar import Bar
import pandas as pd
import numpy as np
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


def makeLineNumDict(): # maybe add a 'csv_file' as our input?
    # look for a csv file containing line number information
    #(from which line to which line to trim) and gather the relevant
    #   information (filename, start line, end line) in a dictionary
    line_num_dict = {}
    try:
        cat_df = pd.read_csv("../Catalogs.csv")

        for index, row in cat_df.iterrows():
            if (not np.isnan(row[1])) and (not np.isnan(row[2])):
                line_num_dict[row[0].lower()] = int(row[1]), int(row[2])

    except FileNotFoundError:
        print("CSV file with trimming line numbers not found.")

    return line_num_dict
