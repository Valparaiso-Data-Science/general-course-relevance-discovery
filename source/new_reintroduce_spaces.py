'''
--Needs a more descriptive docstring--

Wordninja related code resides here, utilizes the semantic split method from
    punct_split (wraps the wordninja split function).
'''

import re
import punct_split as ps
import sys

#This regex matches any string that is made up of
#at least 8 capital or lowercase letters
long_str_re = r"[a-zA-Z0-9]{8,}"

#potential new re (not adequately tested)
# does a look a head (?=[a-zA-Z]) for a lowercase
# or capital letter, if there is one, then look
# then match a 17 character long string that can
# contain capital/lowercase letters and digits
# i am a little unsure if this re does exactly what
# i want it to do, it needs a lot more testing
# i think that it needs a '.*' after the equal sign
p_long_string_re = r"(?=[a-zA-Z])[a-zA-Z0-9]{17,}"

def pad_characters(input_string):
    # do basically all of the methods in punct_split
    # however it does not use the spacy package at all
    # (the nlp model) or do any splitting here
    return ps.space_coursecodes(ps.space_punct(ps.space_parantheses(ps.correct_apostrophe(input_string))))

def get_dict_of_bad_words(fp):
    '''
    IN: a file path
    OUT: a dictionary of 'bad words' and what they should be replaced with
    '''
    f = open(fp)
    lines = f.readlines()

    bad_strings_dict = {} # dictionary has all of the strings and what they should be changed into

    for l in lines:
        pl = pad_characters(l)
        for w in pl.split(" "): # split the line based off of spaces
            if re.match(long_str_re, w): # see if the word is more than 17 characters long
                s_s = ps.semantic_split(w) # create 'split string' from the word
                if not w == s_s: # if the two strings aren't the same
                    if s_s not in bad_strings_dict: # and the 'split string' is not in the dictionary already
                        bad_strings_dict.update({w: s_s}) # add it into the dictionary

    return bad_strings_dict

# alternate implementation (is faster)
# captures 6 more courses than above method (on youngstown)
def a_get_dict_of_bad_words(fp):
    '''
    IN: a file path
    OUT: a dictionary of 'bad words' and what they should be replaced with
    '''
    f = open(fp)
    data = f.read()

    bad_strings_dict = {} # dictionary has all of the strings and what they should be changed into
    matches = list(set(re.findall(long_str_re, data)))

    for w in matches:
        s_s = ps.semantic_split(w)
        if not w == s_s: # if the original string doesn't match the split string
            bad_strings_dict.update({w: s_s}) # add it to the dictionary
            # we don't have to lookup if w is in the dictionary because of the set above

    # currently the only issue is that there are no padded characters with this method
    # however, based off of some testing on my local machine, it doesn't seem to be that
    # big of an issue

    return bad_strings_dict

def reintroduce_spaces(fp, nfp=None):
    '''
    IN: a file path
    OUT: a file path to the 'wordninja-ed' xml
    '''
    #d = get_dict_of_bad_words(fp)
    d = a_get_dict_of_bad_words(fp)

    # get the data out of the file
    f = open(fp, 'r')
    f_data = f.read()
    f.close()

    n_data = f_data # potentially make 'pad_characters(f_data)'; do NOT do that, it reduced the number of courses I was getting from 59k to 43k, definitely not a good move

    #potentially can move this to re.sub? I don't know what the speed difference would be
    for i in d: # this is where the big speed improvement is, it runs through 3500 entries instead of all of the tags in the xml
        n_data = n_data.replace(i, d[i])

    # it might be worth looking into using re.sub for the substitution, instead of '.replace', I don't
    # know the full implementation details of them, so it may be worth trying out.
    #re.sub(i, d[i], f_data)

    # if no name for outfile given, use source name + "_spaced"
    if nfp is None:
        nfp = fp[:fp.rfind(".")] + "_spaced" + fp[fp.rfind("."):]

    #"WN_" + fp < old way
    nf = open(nfp, 'w') # this command will need to be changed to fit with the rest of the pipeline
    nf.write(n_data)
    nf.close()
    return nfp

#make_split_file(fp)

def main(argv):

    filename = "../fullPDFs/Youngstown.xml"

    # if user specified another file as input
    if len(argv) > 1:
        filename = argv[1]

    reintroduce_spaces(filename)

# if ran as a standalone file
if __name__ == "__main__":
    main(sys.argv)
