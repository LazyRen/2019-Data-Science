#!/usr/bin/env python3

import sys
import math

attrHeader = []
attributes = []

def loadData(fileName, header, rows):
	with open(fileName, 'r') as trainFile:
		header.append(trainFile.readline().rstrip('\n').split('\t'))
		rows.append([line.rstrip('\n').split('\t') for line in trainFile.readlines()])

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print("3 arguments are required to run the program")
		print("***** USAGE *****")
		print("%s [train file] [test file] [result file]" % sys.argv[0])
		sys.exit("argv error")

	loadData(sys.argv[1], attrHeader, attributes)
	print(attrHeader)
	print(attributes)
