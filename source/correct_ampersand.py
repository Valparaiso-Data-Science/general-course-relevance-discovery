"""
    Simple utility for correcting raw ampersands ('&') in a file to XML symbol for ampersand ('&amp;')
"""

import sys


def main(argv):

    if len(argv) < 2:
        print('USAGE: python3 %s <target file>' % argv[0])
        exit(0)

    in_path = argv[1]
    out_path = in_path[:in_path.rfind(".")] + "_ampersanded" + in_path[in_path.rfind("."):]

    # container for the processed lines
    out_lines = []

    with open(in_path, "r") as f:
        line = f.readline()

        while line:
            out_lines.append(line.replace("& ", "&amp; "))
            line = f.readline()

    # write all the processed lines to file
    f = open(out_path, "w")
    f.writelines(out_lines)
    f.close()


if __name__ == "__main__":
    main(sys.argv)
