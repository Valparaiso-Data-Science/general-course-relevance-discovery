'''
--Needs a more descriptive docstring--

Wordninja related code resides here, utilizes the semantic split method from
    punct_split (wraps the wordninja split function).

Takes in XML files that have spacing issues, finds the offending strings via regex,
    then uses punct_split's wrapper for wordninja (semantic_split) to clean up the XML files.
'''

import re
import punct_split as ps
import sys

#This regex matches any string that is made up of
#at least 8 capital or lowercase letters
long_str_re = r"[a-zA-Z0-9]{8,}"

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
    # uses the 'new' version of the dictionary creation (hence the prefix 'a_')
    d = a_get_dict_of_bad_words(fp)

    # get the data out of the file
    f = open(fp, 'r')
    f_data = f.read()
    f.close()

    n_data = f_data

    for i in d: # this is where the big speed improvement is, it runs through 3500 entries instead of all of the tags in the xml
        n_data = n_data.replace(i, d[i])

    # it might be worth looking into using re.sub for the substitution, instead of '.replace', I don't
    # know the full implementation details of them, so it may be worth trying out.
    #re.sub(i, d[i], f_data)

    # if no name for outfile given, use source name + "_spaced"
    if nfp is None:
        nfp = fp[:fp.rfind(".")] + "_spaced" + fp[fp.rfind("."):]

    nf = open(nfp, 'w') # this command will need to be changed to fit with the rest of the pipeline
    nf.write(n_data)
    nf.close()
    return nfp

def main(argv):

    filename = "../fullPDFs/Youngstown.xml"

    # if user specified another file as input
    if len(argv) > 1:
        filename = argv[1]

    reintroduce_spaces(filename)

# if ran as a standalone file
if __name__ == "__main__":
    main(sys.argv)
