# -*- coding: utf-8 -*-

#Import Statements

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

male_pronouns = {'he', 'him', 'his', 'himself'}
female_pronouns = {'she', 'her', 'hers', 'herself'}

nonbinary_pronouns = {'they', 'them', 'their', 'theirs', 'themself', 
                    'e', 'ey', 'em', 'eir', 'eirs', 'eirself', 
                    'fae', 'faer', 'faers', 'faerself', 
                    'per', 'pers', 'perself',
                    've', 'ver', 'vis', 'verself',
                    'xe', 'xem', 'xyr', 'xyrs', 'xemself',
                    'ze', 'zie', 'hir', 'hirs', 'hirself', 
                    'sie', 'zir', 'zis', 'zim', 'zieself', 
                    'emself', 'tey', 'ter', 'tem', 'ters', 'terself'} 

# Load "usual" stop words from package
stop_words = list(stopwords.words('english'))

# not clear on this one
nlp = spacy.load('en', disable=['parser', 'ner'])

# I think this is an attempt to add all pronouns. This is NOT what it does
stop_words.append('-PRON-')

# Departmental abbreviations 
#    Can we get these from the actual catalog? 
first_stops = ['cr','ul','ii','cog','pp','ps','geog','cosc','biol','el','sesp',
               'eecs','oba','phys','phy','mth','cmsc','nur','ce','cs','iii'] 

# Learning words? Should we extract from Bloom's taxonomy? 
second_stops = ['make','impact','apply','change','involve','reside','vary',
                'may', 'meet','use','include','pertain','tell','cover',
                'devote', 'recognize','carry'] 

# Course descriptors: 
third_stops = ['new','minimum','useful','mainly','large','liberal','formerly',
               'especially','absolutely','graduate','odd','one','throughout',
               'weekly','least','well','hour','common','require','along',
               'least','long','related','prior','open','sophomore','junior',
               'single', 'necessary'] 

# Syllabus kinds of words
fourth_stops = ['treat','prereq','prerequisite','creditsprerequisite',
                'corequisite','either','assignment','major','none','arts',
                'core','andor','semester','hoursprereq','student','instructor',
                'threehour','within','lecturescover','satisfactoryno','summer',
                'yifat','givenfor','term','classroom','area','inquiry',
                'researchintensive','year','via','teacher','ofhow'] 

small_words = list(string.ascii_letters[:26])
small_words.pop(8) # Remove 'i'
small_words.pop(0) # Remove 'a'
small_words.extend(["ll","re","ve"])
# https://stackoverflow.com/questions/252703/what-is-the-difference-between-pythons-list-methods-append-and-extend

stop_words.extend(first_stops)
stop_words.extend(second_stops)
stop_words.extend(third_stops)
stop_words.extend(fourth_stops)

def build_stop_word_list():
	pass

def remove_stop_words(school_df, use_built_in, stopword_list):
	pass

