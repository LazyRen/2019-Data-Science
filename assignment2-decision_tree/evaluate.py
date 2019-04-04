#!/usr/bin/env python3

from collections import defaultdict
from dt import loadData, generateTree, classification, generateResult, reducedErrorPruning
from random import shuffle
from copy import deepcopy
import datetime

def runTest(trainFile, testFile, resultFile, answerFile):
	attrHeader = list()
	samples = list()

	startTime = datetime.datetime.now()
	attrValues = loadData(trainFile, attrHeader, samples, True)

	# shuffle(samples)
	# pruneCut = int(9/10 * len(samples))
	# pruneHeader = deepcopy(attrHeader)
	# pruneSamples = deepcopy(samples)

	decisionTree = generateTree(None, attrHeader, samples, attrValues)
	# reducedErrorPruning(decisionTree, pruneHeader, pruneSamples[pruneCut:])
	cut = 0 if trainFile.find('/') == -1 else trainFile.find('/') + 1
	elapsedTime = datetime.datetime.now() - startTime
	print("Generating decision tree for " + trainFile[cut:] + " took " + str(elapsedTime.total_seconds()) + " seconds")

	cut = 0 if testFile.find('/') == -1 else testFile.find('/') + 1
	startTime = datetime.datetime.now()
	generateResult(testFile, resultFile, decisionTree, attrHeader)
	elapsedTime = datetime.datetime.now() - startTime
	wrongAns = []
	correct, total = score(answerFile, resultFile, wrongAns)
	print(str(correct) + "/" + str(total))
	print("Classification for " + testFile[cut:] + " took " + str(elapsedTime.total_seconds()) + " seconds\n")
	if correct != total:
		print("Check diffrence?")
		inp = input()
		if inp == 'y' or inp == 'Y':
			for wa in wrongAns:
				line = wa[1:-1]
				classification(decisionTree, attrHeader, line, True)
				print("       ", end='')
				printHeader = deepcopy(attrHeader)
				printHeader = printHeader[:-1] + ["prediction", "answer"]
				for attr in printHeader:
					print(f"{attr:15}", end='')
				print(f"\n{wa[0]:4}:  ", end='')
				for col in wa[1:]:
					print(f"{col:15}", end='')
				print("\n\n")

def score(answerFile, resultFile, wrongAns = None):
	answer = []
	prediction = []
	correct = 0

	with open(answerFile, 'r') as openedFile:
		openedFile.readline()
		answer.extend(line.rstrip('\n') for line in openedFile.readlines())
	with open(resultFile, 'r') as openedFile:
		openedFile.readline()
		prediction.extend(line.rstrip('\n') for line in openedFile.readlines())

	if len(answer) != len(prediction):
		print("ERROR: Length of two files are not matching!")
		return 0, 0
	for row in range(len(answer)):
		if answer[row] == prediction[row]:
			correct += 1
		else:
			if wrongAns is not None:
				wa = [row] + prediction[row].split('\t') + [answer[row].split('\t')[-1]]
				wrongAns.append(wa)

	return correct, len(answer)


if __name__ == "__main__":
	trainFiles = ["data/dt_train.txt", "data/dt_train1.txt"]
	testFiles = ["data/dt_test.txt", "data/dt_test1.txt"]
	outputFiles = ["test/dt_result.txt", "test/dt_result1.txt"]
	answerFiles = ["test/dt_answer.txt", "test/dt_answer1.txt"]

	for i in range(len(testFiles)):
		runTest(trainFiles[i], testFiles[i], outputFiles[i], answerFiles[i])
