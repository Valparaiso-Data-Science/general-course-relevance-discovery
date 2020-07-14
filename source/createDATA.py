# files in the current directory
import parse
#from topicModel import plot_10_most_common_words, listofDSCourse
from vectorize import newClean, vectorizer, cleanVectorizer, labelTargetsdf
#from ML import decisionTree,visTree
#from xml_fix_utils import correct_ampersands, ignore_bad_chars

import Prep
import const

#libraries
import os
import pandas as pd
import sys
from joblib import Parallel, delayed

from progress.bar import Bar

def createCSV():
    # container for processed catalogs
    topicModel = pd.DataFrame()

    # toggle for keeping data from intermediary stages
    dirty = False

    # Make all of the required directories; prep the work area
    Prep.prepare()


    # trim the xml files (whenever line number information available, otherwise keep whole file)
    Parallel(n_jobs=-1)(delayed(Prep.trimFile)(const.SOURCE_DIR, const.TRIMMED_DIR, filename, Prep.makeLineNumDict(const.TRIM_CSV))
                        for filename in Bar('Trimming Files').iter(os.listdir(const.SOURCE_DIR)))


    # clean the xml files (fix problems and make it parseable)
    Parallel(n_jobs=-1)(delayed(Prep.cleanXML)(const.TRIMMED_DIR , const.SUPERTRIMMED_DIR , filename)
                        for filename in Bar('Fixing Files').iter(os.listdir(const.TRIMMED_DIR)))


    # make a csv from the files in temp_data/superTrimmedPDFs
    Parallel(n_jobs=-1)(delayed(parse.makeCSV)(filename, const.SUPERTRIMMED_DIR, dirty) # maybe make makeCSV take an output directory?
                        for filename in Bar('Making CSVs').iter(os.listdir(const.SUPERTRIMMED_DIR)))
    '''
    # fix the bug that is here; get an error in newClean complaining about a float
    print("Creating 'valpo.csv'...")
    os.system("sh ../pre/parsevalpo.sh ../fullPDFs/ucat1920.xml ../courses/")
    clean_valpo_df = newClean(pd.read_csv(const.CSV_DIR + "/" + "valpo.csv"))
    clean_valpo_df.to_csv(const.CSV_DIR + "/" + "valpo.csv")
    '''
    # collect all data frames in one list
    df_container = []
    for filename in Bar('Making topicModel').iter(os.listdir(const.CSV_DIR)):
        df_container.append(pd.read_csv(const.CSV_DIR + "/" + filename))
    # concatenate list into one joint data frame
    topicModel = pd.concat(df_container)


    cleaned_df = newClean(topicModel)
    print("Creating '" + const.CSV_DIR + "/" + const.ALL_CSV + "'...")
    cleaned_df.to_csv(const.CSV_DIR + "/" + const.ALL_CSV, encoding="utf-8-sig")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("You need to provide a directory for this script to work properly!\n(Hint: You probably want to feed it 'source/')")
    else:
        try:
            os.chdir(sys.argv[1])
        except:
            print("Error: Directory doesn't exist. Exiting...")
            os.quit()
    createCSV()
