'''
Main method for reading XML files and outputting a CSV file with course titles and descriptions.

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
    """
    Manages the three stages of the XML->CSV process.
    """

    # toggle for keeping data from intermediary stages
    dirty = False

    # step 1. trim the xml files (whenever line number information available, otherwise keep whole file)
    Parallel(n_jobs=-1)(delayed(prep.trimFile)(const.SOURCE_DIR, const.TRIMMED_DIR, filename, prep.makeLineNumDict(const.TRIM_CSV))
                        for filename in Bar('Trimming Files').iter(os.listdir(const.SOURCE_DIR)))


    # step 2. clean XML: remove most types of tags and contents of 'Figure' tags
    Parallel(n_jobs=-1)(delayed(prep.cleanXML)(const.TRIMMED_DIR , const.SUPERTRIMMED_DIR , filename)
                        for filename in Bar('Fixing Files').iter(os.listdir(const.TRIMMED_DIR)))



    # step 3 . call the parser that figures out course titles and descriptions from XML structure
    Parallel(n_jobs=-1)(delayed(parse.makeCSV)(filename, const.SUPERTRIMMED_DIR) # maybe make makeCSV take an output directory?
                        for filename in Bar('Making CSVs').iter(os.listdir(const.SUPERTRIMMED_DIR)))
    '''

    # step 4.
    # fix the bug that is here; get an error in newClean complaining about a float
    print("Creating 'valpo.csv'...")
    os.system("sh ../pre/parsevalpo.sh ../fullPDFs/ucat1920.xml ../courses/")
    clean_valpo_df = newClean(pd.read_csv(const.CSV_DIR + "/" + "valpo.csv"))
    clean_valpo_df.to_csv(const.CSV_DIR + "/" + "valpo.csv")
    '''
    # collect all data frames in one list
    df_container = []
    for filename in Bar('Making topicModel').iter(os.listdir(const.CSV_DIR)):
        #df_temp = pd.read_csv(const.CSV_DIR + "/" + filename)
        #df_temp = pd.drop_duplicates(subset= ['School','CourseID', 'Descriptions'], keep= 'last') 
        df_container.append(pd.read_csv(const.CSV_DIR + "/" + filename))
        #df_container.append(df_temp)

    # concatenate list into one joint data frame
    topicModel = pd.concat(df_container)

    # clean up the dataframe; and make our final 'AllSchools.csv' file
    #   * if you are not using the Makefile, you will be missing Valpo's courses
    #   * if you are using the Makefile, the next step that happens is valpo's courses
    #       are added into the csv.
    #       * update 7-17 : the Makefile now no longer includes valpo's courses, there
    #           are a few bugs with doing it the previous way, mainly that pandas
    #           complained a lot. This is definitely something that needs to be fixed.

    #investigate newClean 
    cleaned_df = newClean(topicModel)

    print("Creating '" + const.CSV_DIR + "/" + const.ALL_CSV + "'...")
    cleaned_df.to_csv(const.CSV_DIR + "/" + const.ALL_CSV, encoding="utf-8-sig")

    # if not 'dirty' mode, remove data from intermediary stages
    if not dirty:
        for file in os.listdir(const.TRIMMED_DIR):
            os.unlink(const.TRIMMED_DIR + "/" + file)

        for file in os.listdir(const.SUPERTRIMMED_DIR):
            os.unlink(const.SUPERTRIMMED_DIR + "/" + file)


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
