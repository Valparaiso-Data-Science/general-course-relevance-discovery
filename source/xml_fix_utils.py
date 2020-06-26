import sys


def ignore_bad_chars(filepath, out_filepath=None, write_exclusions=False, excludable_ords={65535}):
    """
    Utility function for reading XML file and writing new version of it with any characters in excludable_ords removed.

    :param filepath: path to source filename.
    :param out_filepath: custom path for "clean" output file.
    :param write_exclusions: whether or not to write file detailing exclusions.
    :param excludable_ords: the set of characters to be excluded. By default only ignores Unicode character 65535.

    :return: path to output file.
    """

    if out_filepath is None:
        out_filepath = filepath[:filepath.rfind(".")] + "_cleanencoded" + filepath[filepath.rfind("."):]

    # path for file with the omitted garbage
    exclusion_path = filepath[:filepath.rfind(".")] + "_exclusions" + filepath[filepath.rfind("."):]

    exclusions = {}
    out_lines = []

    with open(filepath, "r", encoding="utf-8") as f:
        line_num = 0
        line = f.readline()

        while line:
            line_num += 1
            line_chars = []

            for ch in line:
                # if excludable character, skip adding it to line but store it in exclusions
                if ord(ch) in excludable_ords:
                    # if character encountered before, add current line to the record of its appearances
                    if ch in exclusions:
                        exclusions[ch].append(line_num)
                    # if character not encountered before, create new entry for its list of observed occurrences
                    else:
                        exclusions[ch] = [line_num]

                # if character not excludable, just append it to line chars for further writing to file
                else:
                    line_chars.append(ch)

            # join "clean" characters into a string
            out_lines.append("".join(line_chars))

            # next line
            line = f.readline()

    # write out the clean XML
    with open(out_filepath, "w") as f:
        f.writelines(out_lines)

    # if asked for, write out file documenting the excluded characters and where they occurred
    if write_exclusions:
        with open(exclusion_path, "w") as f:
            for key in exclusions.keys():
                f.write(f"%d. `{key}` ord: {ord(key)}. Lines: {*(exclusions[key]),}")

    return out_filepath


def correct_ampersands(filepath, out_filepath=None):
    """
    Utility function for correcting ampersands in "bad" XML files from '&' to '&amp;'.

    :param filepath: source file path.
    :param out_filepath: optional name for the resulting file.

    :return: path to out file.
    """

    if out_filepath is None:
        out_filepath = filepath[:filepath.rfind(".")] + "_ampersanded" + filepath[filepath.rfind("."):]

    # container for the processed lines
    out_lines = []

    with open(filepath, "r") as f:
        line = f.readline()

        while line:
            out_lines.append(line.replace("& ", "&amp; "))
            line = f.readline()

    # write all the processed lines to file
    f = open(out_filepath, "w")
    f.writelines(out_lines)
    f.close()

    return out_filepath


def main(argv):
    # test code for the XML correction functions

    bad_encoded = "../fullPDFs/Alma.xml"

    ignore_bad_chars(bad_encoded, out_filepath="../fullPDFs/Alma_clean_encoded_new.xml")

    bad_ampersanded = "../fullPDFs/Pittsburgh.xml"

    correct_ampersands(bad_ampersanded, out_filepath="../fullPDFs/Pittsburgh_ampersanded_new.xml")


if __name__ == "__main__":
    main(sys.argv)
