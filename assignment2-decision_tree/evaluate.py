#!/usr/bin/env python3

from collections import defaultdict
from dt import loadData, generateTree, classification, generateResult
import datetime

def runTest(trainFile, testFile, resultFile, answerFile):
	attrHeader = list()
	samples = list()
	attrValues = defaultdict(lambda: set())

	startTime = datetime.datetime.now()
	loadData(trainFile, attrHeader, samples, attrValues)
	decisionTree = generateTree(None, attrHeader, samples, attrValues)
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
				line = wa[wa.find(":")+2 : wa.find("->")-1]
				line = line.split('\t')[:-1]
				classification(decisionTree, attrHeader, line, True)
				print(attrHeader[:-1])
				print(wa)

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
				wrongAns.append(str(row) + ": " + prediction[row] + " -> " + answer[row].split('\t')[-1])

	return correct, len(answer)


if __name__ == "__main__":
	trainFiles = ["data/dt_train.txt", "data/dt_train1.txt"]
	testFiles = ["data/dt_test.txt", "data/dt_test1.txt"]
	outputFiles = ["test/dt_result.txt", "test/dt_result1.txt"]
	answerFiles = ["test/dt_answer.txt", "test/dt_answer1.txt"]

	for i in range(len(testFiles)):
		runTest(trainFiles[i], testFiles[i], outputFiles[i], answerFiles[i])
