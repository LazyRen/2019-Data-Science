#!/usr/bin/env python3

import sys
from subprocess import Popen, PIPE

def runExe(fileName, maxLine, maxTxn):

if __name__ == '__main__':
	pathDir = os.path.dirname(os.path.realpath(__file__))
	if len(sys.argv) == 4:
		exeFile1 = pathDir + str(sys.argv[1])
		exeFile2 = pathDir + str(sys.argv[2])
		inputFile = pathDir + str(sys.argv[3])
	elif len(sys.argv) == 6:
		exeFile1 = pathDir + str(sys.argv[1])
		exeFile2 = pathDir + str(sys.argv[2])
		inputFile = pathDir + str(sys.argv[3])
		outputFile1 = pathDir + str(sys.argv[4])
		outputFile2 = pathDir + str(sys.argv[5])
	else:
		print(sys.argv[0] + " Usage")
		print("[" + sys.argv[0] + "]" + " [exe file1]"\
		      + " [exe file2]" + " [input file]"\
		      + " (optional)[output file1]" + " (optional)[output file2]")
		print("IF optional output file names are not given,", end="")
		print(" it will be automatically set to 'output1.txt' & 'output2.txt'")
