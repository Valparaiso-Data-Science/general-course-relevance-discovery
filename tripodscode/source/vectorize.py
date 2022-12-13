import pandas as pd
from nltk.stem.porter import *
ps = PorterStemmer()

#Reader /output/Full csvs and convert to dataframe of CourseID and
first_stops = ['cr','ul','ii','cog','pp','ps','geog','cosc','biol','el','sesp',
               'eecs','oba','phys','phy','mth','cmsc','nur','ce','cs','iii'] #unkown/unnecessary abbreviations
second_stops = ['make','impact','apply','change','involve','reside','vary','may',
                'meet','use','include','pertain','tell','cover','devote',
                'recognize','carry'] #verbs that are not useful
third_stops = ['new','minimum','useful','mainly','large','liberal','formerly',
               'especially','absolutely','graduate','odd','one','throughout',
               'weekly','least','well','hour','common','require','along','least',
               'long','related','prior','open','sophomore','junior','single',
               'necessary'] #unuseful descriptors
fourth_stops = ['treat','prereq','prerequisite','creditsprerequisite',
                'corequisite','either','assignment','major','none','arts','core',
                'andor','semester','hoursprereq','student','instructor','threehour',
                'within','lecturescover','satisfactoryno','summer','yifat',
                'givenfor','term','classroom','area','inquiry','researchintensive',
                'year','via','teacher','ofhow'] #other unuseful words
def newClean(df):
    import string
    schoolID = []
    courseID = []
    description = []
    stopwords = ['credits','spring','fall','course','students','offered','hours','credit','grade','typically']
    stopwords += first_stops
    stopwords += second_stops
    stopwords += third_stops
    stopwords += fourth_stops
    for i, row in df.iterrows():
        cleanDesc = row['Descriptions']
        cleanDesc = cleanDesc.translate(cleanDesc.maketrans(string.punctuation, "\\" * len(string.punctuation)))
        cleanDesc = cleanDesc.replace("\\", '')
        cleanDesc = ' '.join([ps.stem(word.lower()) for word in cleanDesc.split() if word.lower() not in stopwords])
        schoolID.append(row['School'])
        courseID.append(row['CourseID'])
        description.append(cleanDesc)

    cleanDF = pd.DataFrame(list(zip(schoolID, courseID, description)), columns=['School', 'CourseID', 'Descriptions'])
    print(cleanDF.head())
    return (cleanDF)