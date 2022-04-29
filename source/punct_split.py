"""
    Contains punct_split, a wrapper function for wordnina.split that: applies pre-semantic split based on punctuation
    and course codes, and applies semantic split (wordninja split only when split results in actual meaningful words);

    and all helper methods called in punct_split.
"""

import spacy
import wordninja
import sys
import re
import enchant
import en_core_web_sm

# word tokenizer
nlp = spacy.load("en_core_web_sm")

# spell checker
spell = enchant.Dict()

no_space_punct = {'-', '/'}
post_space_punct = {"(", "[", "{", "<"}
pre_space_punct = {" ", ".", ",", ":", ";", "!", "?", ")", "]", "}", ">"}


def correct_apostrophe(input_string):
    """
    sometimes, apostrophe is represented as UTF-8 character ’ with ordinal 8217, which is not processed correctly by
    wordninja;
    replace every instance of ’ (ordinal 8217) with ' (ordinal 39), which wordninja can handle
    """

    return input_string.replace(chr(8217), chr(39))


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


def punct_split(input_string):
    """
    main split method that combines all the above pre-processing
    """

    # apply all pre-wordninja preprocessing
    pre_ninja = space_coursecodes(space_punct(space_parantheses(correct_apostrophe(input_string))))

    doc = nlp(pre_ninja)

    doc_chunks = []

    # apply semantic split to all non-punctuation tokens
    for token in doc:
        if token.is_punct:
            doc_chunks.append(token.text)
        else:
            doc_chunks.append(semantic_split(token.text))

    final_string = ""

    # add all the chunks together with correct spacing (e.g. space after '.' but before '{')
    for i in range(len(doc_chunks)):
        final_string += doc_chunks[i]

        if (doc_chunks[i] in post_space_punct) or (doc_chunks[i] in no_space_punct):
            continue

        if (i != len(doc_chunks)-1) and (doc_chunks[i+1] not in pre_space_punct) and \
                (doc_chunks[i+1] not in no_space_punct):
            final_string += " "

    # trick to remove extra white space
    final_string_lines = final_string.split("\n")
    for i in range(len(final_string_lines)):
        final_string_lines[i] = " ".join(final_string_lines[i].split())
    final_string = "\n".join(final_string_lines)

    return final_string


def main(argv):
    """
    testing for all the strings in input_strings
    """

    # test strings
    input_strings = [
        "Foursemestersofchemistry(CHM111/113,CHM112/114,CHM211/213,andCHM212-/214),twosemestersofphysics (PCS201/20" +
        "3andPCS202/204) andmathematicsthroughcalculusI(MAT160)arerequired.",
        "Mathematicsmajorsarerequiredtocomplete:MAT 160, MAT 260, andMAT 360(CalculusI, II, andIII:12credits), MAT" +
        " 302 (LinearAlgebra:3credits), plusatleastfouradditionalupperlevelmathematicscourses(atleast12credits) and" +
        "CSC110 (IntroductiontoComputerProgramming:2-4 credits),or MAT151I(Computer ApplicationsforScienceand Mathem" +
        "atics: 3 credits).EachstudentmustalsocompleteaJunior Seminar (MAT398/399:2 credits)andSenior Experience(MAT4" +
        "98/499: 4 credits)inmathematics. ",
        "EQUALEDUCATIONALANDEMPLOYMENTOPPORTUNITYPOLICY",
        "Caldwell, New Jersey, has seen\n many changes over the years and was recently ranked by NJMonthly Magazine " +
        "as one of the best places to live in all of New Jersey. A short walk brings students to the revitalized " +
        "center of town, where shops, a movie theater, wi-fi hot spots andlotsoftastyrestaurantsprovidegreatoptions" +
        "forfun. Manyshopsparticipateinadiscount program for Caldwell University students, making the town affordable" +
        " on student budgets.",
        "If there is anaturaldisaster that interrupts a student’slong-termparticipationinacourse(s),CarlowUniversity" +
        "willapprise students oftheoptionsavailabletocompletetheiracademic coursework. ",
        "PREREQUISITES:BSM103 ANDBSM226. ",
        "Continuum and atomistic descriptions of diffusion in solids. Reactionsinvolving surfaces and interfaces, in" +
        "cluding evaporation, adsorption,grain growth, and coarsening. Phase transformation kinetics, includingnucle" +
        "ation, growth, solidification, spinodal decomposition, and martensitictransformations. Analysis of systems " +
        "with multiple kinetic mechanisms(typical examples include oxidation, crystal growth, and sintering).Prerequ" +
        "isite: background in basic thermodynamics. Recommended:ENGN 1410 or 2410 or equivalent.",
        "poststructuralistsmisusethewordduetoNewton'sthirdlaw"]

    for input_string in input_strings:
        processed = punct_split(input_string)

        print(input_string)
        print(processed)
        print()


if __name__ == "__main__":
    main(sys.argv)
