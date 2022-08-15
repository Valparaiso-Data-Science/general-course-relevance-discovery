# -*- coding: utf-8 -*-

#Import Statements

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

"""
Idea is to build the stopword list based on user preferences. There are seven 
bins: 
1. Small words - Individual letters plus 'll,' 're,' and 've.'
2. Pronouns - List of male, female, and non-binary pronouns
3. Descriptors - These are words that are generally describing meetings
4. School words - Words specifically describing college related meetings
5. `nltk` built in stop words
6. Verbs - These are ones from Bloom's taxonomy
7. Dept Codes - These are from the school's catalog directly

If the user elects to remove stopwords the first four bins are included. Then 
the user can opt to include the `nltk` stopwords (with its caveats) and/or the 
verbs from Bloom's taxonomy. 

The last bin is the dept codes, which come from the user's catalog, and is 
optional to include, but it will be the default if the user supplies the xml
"""

## Bin 1: Small words
small_words = list(string.ascii_letters[:26])
small_words.pop(8) # Remove 'i'
small_words.pop(0) # Remove 'a'
small_words.extend(["ll","re","ve"])
# https://stackoverflow.com/questions/252703/ ...
#         what-is-the-difference-between-pythons-list-methods-append-and-extend


## Bin 2: Pronouns
male_pronouns = ['he', 'him', 'his', 'himself']
female_pronouns = ['she', 'her', 'hers', 'herself']
nonbinary_pronouns = ['they', 'them', 'their', 'theirs', 'themself', 
                    'e', 'ey', 'em', 'eir', 'eirs', 'eirself', 
                    'fae', 'faer', 'faers', 'faerself', 
                    'per', 'pers', 'perself',
                    've', 'ver', 'vis', 'verself',
                    'xe', 'xem', 'xyr', 'xyrs', 'xemself',
                    'ze', 'zie', 'hir', 'hirs', 'hirself', 
                    'sie', 'zir', 'zis', 'zim', 'zieself', 
                    'emself', 'tey', 'ter', 'tem', 'ters', 'terself']
pronouns = []
pronouns.extend(male_pronouns)
pronouns.extend(female_pronouns)
pronouns.extend(nonbinary_pronouns)

## Bin 3: Descriptors
meeting_words = ['new','minimum','useful','mainly','large','liberal','formerly',
               'especially','absolutely','graduate','odd','one','throughout',
               'weekly','least','well','hour','hours','common','require',
               'along','least','long','related','prior','open','monthly',
               'daily','Monday','Tuesday','Wednesday','Thursday','Friday',
               'single','necessary','first','year'] 

## Bin 4: School words - Syllabus kinds of words
school_words = ['prereq','prerequisite','creditsprerequisite','corequisite',
                'prereqs','prerequisites','creditsprerequisites', 'credits',
                'corequisites','either','assignment','major','assignments',
                'majors','none','arts','minor','minors','core','andor',
                'semester','semesters','hoursprereq','student','instructor',
                'instructors','threehour','within','lecturescover',
                'satisfactoryno','summer','givenfor','term','terms',
                'classroom','area','classrooms','areas','inquiry','research'
                'researchintensive','year','via','teacher','ofhow', 
                'freshman','firstyear','sophomore','junior','senior'] 
# Question: Not sure what the double words are? Must be an artifact from the 
#           original data processing. TBD by TT. (remove 'yifat' from list)


## Bin 5: `nltk` stopwords --> Load "usual" stop words from package
sw_nltk = list(stopwords.words('english'))

# TO-DO: What are the caveats for using the built-in stopwords. KMK find ref

## Bin 6: Verbs (from Bloom's)
verbs = ['make','impact','apply','change','involve','reside','vary', 'treat',
         'may','meet','use','include','pertain','tell','cover', 'devote', 
         'recognize','carry','understand'] 

## Bin 7: Departmental abbreviations 
#    Can we get these from the actual catalog? 
ex_codes= ['cr','ul','ii','cog','pp','ps','geog','cosc','biol','el','sesp',
               'eecs','oba','phys','phy','mth','cmsc','nur','ce','cs','iii'] 

def check_last_char(depart_code):
    """ Check if the last character is a letter or not."""

    # Check that there are no numbers in the code
    final_ord_val = ord(dept_code[-1])

    cap_letter_check = (final_ord_val >= 65 and final_ord_val <= 90)
    lower_letter_check = (final_ord_val >= 97 and final_ord_val <= 122)

    letter = cap_letter_check or lower_letter_check

    return letter

def extract_dept_codes(school_df, nam_col):
    """ Search a dataframe of courses called COURSE_DF for classes that contain 
    terms from CLEAN_TERMS. The last variable SEARCH_COLS lists the columns 
    that are to be searched. """    

    # Initialize an empty list for the codes
    temp_codes = []

    # Extract the column where there course names are
    code_col = school_df[nam_col]

    # Loop over all the courses in a school: 
    for i in range(len(school_df)):

        # Pull the course name 
        course_name = code_col[i]

        # Extract the dept code
        dept_code = course_name.split()[0]

        # Check if the last character is a letter
        letter = check_last_char(dept_code)

        while not letter:
            # Cut off the last character of the department code
            dept_code = dept_code[:-1]

            # Check if the new last character is a letter
            letter = check_last_letter(dept_code)

        temp_codes.append(dept_code)

    return list(set(temp_codes))

def build_stop_word_list(school_df = None, nam_col = None, 
                         inc_sw = False, inc_verbs = False, inc_codes = True):
    """ Build a stopword list based on certain preferences. The defaults add 
    just the departmental codes from the school's dataframe if it is supplied. 
    Including the verbs from Bloom's taxonomy and the NLTK stopwords needs to 
    be specified by the user. """
    
    # Start by building the default list with the first four bins: 
	default_list = small_words
    default_list.extend(pronouns)
    default_list.extend(meeting_words)
    default_list.extend(school_words)

    stop_list = default_list 

    # There are three flags for including the `nltk` stopwords (bin 5), verbs 
    #       from Bloom's (bin 6), and then the departmental codes (bin 7)

    # Including the `nltk` stopwords
    if inc_sw: 
        stop_list.extend(sw_nltk)

    # Including Bloom's verbs
    if inc_verbs:
        stop_list.extend(verbs)

    # Including departmental codes 
    if inc_codes and (school_df != None) and (nam_col != None):
        dept_codes = extract_dept_codes(school_df, nam_col)
        stop_list.extend(dept_codes)

    return stop_list

def terms_remove_stops(term_list, stopword_list):
    """ This removes any stopwords from the term list. 
    Recommended to run before searching for terms but not required."""

	# set difference https://www.geeksforgeeks.org/python-set-difference/
    term_set = set(term_list)
    stop_set = set(stopword_list)

    new_terms = list(term_set.difference(stop_set))

    return new_terms
