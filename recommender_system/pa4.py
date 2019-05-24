#!/usr/bin/env python3

"""
This file is intended to be used by anyone with own output files & ideal files.
Change global dir variables properly before use.
"""

from math import sqrt
import datetime
import subprocess

inputFileDir  = "data/"
idealFileDir  = "data/"
outputFileDir = "data/"
EXECUTABLE_NAME = "recommender.py"
testNameList   = ["u1", "u2", "u3", "u4", "u5"]


def loadData(fileName):
    with open(fileName, 'r') as openedFile:
        # [user_id] [item_id] [rating]
        return [int(line.rstrip('\n').split('\t')[2]) for line in openedFile.readlines()]


def runEvaluation(testName):
    print("Starting Evaluation: " + testName)
    idealTest = loadData(idealFileDir + testName + ".test")
    predictedTest = loadData(outputFileDir + testName + ".base_prediction.txt")
    tested = len(idealTest)
    total = 0
    diff = dict()
    startTime = datetime.datetime.now()

    for i in range(len(idealTest)):
        sub = predictedTest[i] - idealTest[i]
        if sub not in diff:
            diff[sub] = 1
        else:
            diff[sub] += 1
        total += sub ** 2

    RMSE = sqrt(total/tested)
    elapsedTime = datetime.datetime.now() - startTime
    print("RMSE: " + format(RMSE, ".7f") + "\tTotal: " + str(total))
    print(sorted(diff.items()))
    print("Evaluation took " + str(elapsedTime.total_seconds()) + " seconds\n")


if __name__ == "__main__":
    runRecommender = False
    userInput = input("Run recommender program? (Y/N): ")
    if (userInput == 'Y' or userInput == 'y'):
        runRecommender = True
    for testName in testNameList:
        if runRecommender:
            print("Running {} Prediction".format(testName))
            startTime = datetime.datetime.now()
            p = subprocess.Popen(["./"+EXECUTABLE_NAME,
                                  inputFileDir+testName+".base",
                                  idealFileDir+testName+".test"],
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE)
            p.wait()
            elapsedTime = datetime.datetime.now() - startTime
            print("Prediction took " + str(elapsedTime.total_seconds()) + " seconds")
        runEvaluation(testName)
