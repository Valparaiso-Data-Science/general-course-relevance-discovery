import os
from progress.bar import Bar

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
