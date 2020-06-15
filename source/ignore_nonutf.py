"""
    Simple utility for ignoring specific characters (by ordinal)
"""

import sys


def main(argv):

    if len(argv) < 2:
        print("USAGE: %s <file to parse>" % argv[0])
        exit(0)

    in_path = argv[1]
    out_path = in_path[:in_path.rfind(".")] + "_clean_encoded" + in_path[in_path.rfind("."):]
    exclusion_path = in_path[:in_path.rfind(".")] + "_exclusions" + in_path[in_path.rfind("."):]

    excludable_ords = {65535}
    exclusions = {}

    out_lines = []
    exclusion_lines = []

    with open(in_path, "r", encoding="utf-8") as f:
        line_num = 0
        line = f.readline()

        while line:
            line_num += 1

            line_chars = []

            for ch in line:
                if ord(ch) in excludable_ords:
                    if ch in exclusions:
                        exclusions[ch].append(line_num)
                    else:
                        exclusions[ch] = [line_num]

                else:
                    line_chars.append(ch)

            out_lines.append("".join(line_chars))

            line = f.readline()

    with open(out_path, "w") as f:
        f.writelines(out_lines)

    with open(exclusion_path, "w") as f:
        counter = 1
        for key in exclusions.keys():
            f.write(f"%d. `{key}` ord: {ord(key)}. Lines: {*(exclusions[key]),}")


if __name__ == "__main__":
    main(sys.argv)
