#!/usr/bin/env python3

from collections import defaultdict
import dt
import datetime

def runTest(trainFile, testFile, resultFile, answerFile):
	attrHeader = list()
	samples = list()
	attrValues = defaultdict(lambda: set())

	startTime = datetime.datetime.now()
	dt.loadData(trainFile, attrHeader, samples, attrValues)
	decisionTree = dt.generateTree(None, attrHeader, samples, attrValues)
	cut = 0 if trainFile.find('/') == -1 else trainFile.find('/') + 1
	elapsedTime = datetime.datetime.now() - startTime
	print("Generating decision tree for " + trainFile[cut:] + " took " + str(elapsedTime.total_seconds()) + " seconds")

	cut = 0 if testFile.find('/') == -1 else testFile.find('/') + 1
	startTime = datetime.datetime.now()
	dt.classification(testFile, resultFile, decisionTree, attrHeader)
	elapsedTime = datetime.datetime.now() - startTime
	correct, total = score(answerFile, resultFile)
	print(str(correct) + "/" + str(total))
	print("Classification for " + testFile[cut:] + " took " + str(elapsedTime.total_seconds()) + " seconds\n")

def score(answerFile, resultFile):
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
	return correct, len(answer)
	print(correct + "/" + len(answer))


if __name__ == "__main__":
	trainFiles = ["data/dt_train.txt", "data/dt_train1.txt"]
	testFiles = ["data/dt_test.txt", "data/dt_test1.txt"]
	outputFiles = ["test/dt_result.txt", "test/dt_result1.txt"]
	answerFiles = ["test/dt_answer.txt", "test/dt_answer1.txt"]

	for i in range(len(testFiles)):
		runTest(trainFiles[i], testFiles[i], outputFiles[i], answerFiles[i])
