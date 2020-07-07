import re
import wordninja
import punct_split

#fp = "Youngstown.xml"

long_str_re = r"[a-zA-Z]{17,}"

def pad_characters(input_string):
    return punct_split.space_coursecodes(punct_split.space_punct(punct_split.space_parantheses(input_string)))

def get_dict_of_bad_words(fp):
    f = open(fp)
    lines = f.readlines()

    bad_strings_dict = {} # dictionary has all of the strings and what they should be changed into

    for l in lines:
        pl = pad_characters(l)
        for w in pl.split(" "): # split the line based off of spaces
            if re.match(long_str_re, w): # see if the word is more than 17 characters long
                s_s = punct_split.semantic_split(w) # create 'split string' from the word
                if not w == s_s: # if the two strings aren't the same
                    if s_s not in bad_strings_dict: # and the 'split string' is not in the dictionary already
                        bad_strings_dict.update({w: s_s}) # add it into the dictionary

    return bad_strings_dict

def reintroduce_spaces(fp, nfp=None):
    d = get_dict_of_bad_words(fp)

    # get the data out of the file
    f = open(fp, 'r')
    f_data = f.read()
    f.close()

    n_data = f_data # potentially make 'pad_characters(f_data)'
    for i in d: # this is where the big speed improvement is, it runs through 3500 entries instead of all of the tags in the xml
        n_data = n_data.replace(i, d[i])

    # if no name for outfile given, use source name + "_spaced"
    if nfp is None:
        nfp = fp[:fp.rfind(".")] + "_spaced" + fp[fp.rfind("."):]

    #"WN_" + fp < old way
    nf = open(nfp, 'w') # this command will need to be changed to fit with the rest of the pipeline
    nf.write(n_data)
    nf.close()
    #re.sub(i, d[i], f_data)
    return nfp

#make_split_file(fp)

def main(argv):

    filename = "../fullPDFs/Youngstown.xml"

    # if user specified another file as input
    if len(argv) > 1:
        filename = argv[1]

    reintroduce_spaces(filename)


if __name__ == "__main__":
    main(sys.argv)
