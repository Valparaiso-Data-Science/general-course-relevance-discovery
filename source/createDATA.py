'''
Responsible for creaing our csv that we end up running machine learning on.

You may have to change some aspects of this script when you move to grobid.
    * Mainly removing the wordninja step
'''

# files in the current directory
import parse
from vectorize import newClean, vectorizer, cleanVectorizer, labelTargetsdf
import prep
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

    # trim the xml files (whenever line number information available, otherwise keep whole file)
    Parallel(n_jobs=-1)(delayed(prep.trimFile)(const.SOURCE_DIR, const.TRIMMED_DIR, filename, prep.makeLineNumDict(const.TRIM_CSV))
                        for filename in Bar('Trimming Files').iter(os.listdir(const.SOURCE_DIR)))


    # clean the xml files (fix problems and make it parseable)
    Parallel(n_jobs=-1)(delayed(prep.cleanXML)(const.TRIMMED_DIR , const.SUPERTRIMMED_DIR , filename)
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

    # clean up the dataframe; and make our final 'AllSchools.csv' file
    #   * if you are not using the Makefile, you will be missing Valpo's courses
    #   * if you are using the Makefile, the next step that happens is valpo's courses
    #       are added into the csv.
    cleaned_df = newClean(topicModel)
    print("Creating '" + const.CSV_DIR + "/" + const.ALL_CSV + "'...")
    cleaned_df.to_csv(const.CSV_DIR + "/" + const.ALL_CSV, encoding="utf-8-sig")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("You need to provide a directory for this script to work properly!\n(Hint: You probably want to feed it 'source/')")
    else:
        try:
            # this line exists because there is a weird quirk when running the script from the Makefile.
            # if you run it without changing into the directory, the script can't find the imports, because
            # the local files aren't part of the python path
            os.chdir(sys.argv[1])
        except:
            print("Error: Directory doesn't exist. Exiting...")
            os.quit()
    # Make all of the required directories; prep the work area
    prep.prepare()
    createCSV()
