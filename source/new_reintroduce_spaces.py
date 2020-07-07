import re
import enchant
import wordninja

no_space_punct = {'-', '/'}
post_space_punct = {"(", "[", "{", "<"}
pre_space_punct = {" ", ".", ",", ":", ";", "!", "?", ")", "]", "}", ">"}

fp = "Youngstown.xml"

long_str_re = r"[a-zA-Z]{17,}"

# spell checker
spell = enchant.Dict("en_US")


def space_coursecodes(input_string):
    """
    find course codes and pad them with whitespace
    """

    coursecode_pattern = re.compile(r"[A-Z]{2,6}\s{,1}-{,1}/{,1}[0-9]{2,6}-{,1}/{,1}([0-9]{2,6}){,1}")

    # for any coursecodes in string, find beginning and end index of each
    ind_pairs = [(m.start(0), m.end(0)) for m in re.finditer(coursecode_pattern, input_string)]

    # if no course codes, return original string
    if len(ind_pairs) == 0:
        return input_string

    string_chunks = []  # container for string slices
    prev_end = 0    # end index of previous pattern

    # pad any course codes with spaces
    for i in range(len(ind_pairs)):
        start, end = ind_pairs[i]
        string_chunks.append(input_string[prev_end:start])
        if (start != 0) and (input_string[start - 1] not in post_space_punct) and (input_string[start - 1] != " "):
            string_chunks.append(" ")
        string_chunks.append(input_string[start:end])
        if (end != len(input_string)) and (input_string[end] not in pre_space_punct):
            string_chunks.append(" ")

        prev_end = end

    string_chunks.append(input_string[prev_end:])

    return "".join(string_chunks)

def has_vowels(input_string):
    """
    helper for semantic split; useful to weed out non-words
    """
    vowels = ["e", "a", "i", "o", "u", "y",
              "E", "A", "I", "O", "U", "Y"]

    char_set = set(input_string)

    for v in vowels:
        if v in char_set:
            return True

    return False


def semantic_split(input_string):
    """
    split strings, but only keep splits if they result in actual words
    """

    # if already a word, go back
    if spell.check(input_string):
        return input_string

    word_gain = False

    split_string = wordninja.split(input_string)

    # if at least one word is gained that is not 'a' or 'o'
    for string in split_string:
        if (spell.check(string)) and (has_vowels(string) and (string not in {"a", "o", "A", "O"})):
            word_gain = True

    # check if meaningful words gained; if not, return original
    if word_gain:
        return " ".join(split_string)
    else:
        return input_string

#nlp = spacy.load("en_core_web_sm")

def space_punct(input_string):
    """
    add spaces after any punctuation that is not '(', '[', '{', '<'
    """

    char_list = []

    for i in range(len(input_string)):
        if (input_string[i] in pre_space_punct) and (i != len(input_string) - 1):
            char_list.append(input_string[i])
            char_list.append(" ")
        else:
            char_list.append(input_string[i])

    return "".join(char_list)

def space_parantheses(input_string):
    """
    add spaces before and after parentheses (or square, curly, or angle brackets)
    """

    char_list = []

    for i in range(len(input_string)):
        if (input_string[i] == "(") and (i != 0) and (input_string[i - 1] != " "):
            char_list.append(" ")
            char_list.append("(")

        elif (input_string[i] == "[") and (i != 0) and (input_string[i - 1] != " "):
            char_list.append(" ")
            char_list.append("[")

        elif (input_string[i] == "{") and (i != 0) and (input_string[i - 1] != " "):
            char_list.append(" ")
            char_list.append("{")

        elif (input_string[i] == "<") and (i != 0) and (input_string[i - 1] != " "):
            char_list.append(" ")
            char_list.append("<")

        else:
            char_list.append(input_string[i])

    return "".join(char_list)

def pad_characters(input_string):
    return space_coursecodes(space_punct(space_parantheses(input_string)))


def get_dict_of_bad_words(fp):
    f = open(fp)
    lines = f.readlines()

    bad_strings_dict = {}

    for l in lines:
        pl = pad_characters(l)
        for w in pl.split(" "):
            if re.match(long_str_re, w):
                s_s = semantic_split(w)
                if not w == s_s:
                #print("orig:" + w)
                #print("split:" + s_s)
                #print("-----")
                    if s_s not in bad_strings_dict:
                        bad_strings_dict.update({w: s_s})

    return bad_strings_dict

def make_split_file(fp):
    d = get_dict_of_bad_words(fp)

    f = open(fp, 'r')
    f_data = f.read()
    f.close()

    n_data = f_data
    for i in d:
        n_data = n_data.replace(i, d[i])

    nf = open("WN_" + fp, 'w')
    nf.write(n_data)
    nf.close()
        #re.sub(i, d[i], f_data)

make_split_file(fp)

