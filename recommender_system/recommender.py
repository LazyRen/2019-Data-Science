#!/usr/bin/env python3

import sys

output_file = ""


# load data from file.
def loadData(fileName, rows):
    # [user_id] [item_id] [rating] [time_stamp]
    with open(fileName, 'r') as openedFile:
        rows.extend(line.rstrip('\n').split('\t') for line in openedFile.readlines())


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("2 arguments are required to run the program")
        print("***** USAGE *****")
        print("%s [train file] [test file]" % sys.argv[0])
        sys.exit("argv error")
    output_file = "u" + sys.argv[1][sys.argv[1].find(".base")-1] + ".base_prediction.txt"
    print(output_file)
