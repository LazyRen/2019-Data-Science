#!/usr/bin/env python3

"""
This file is intended to be used by anyone with own output files & ideal files.
Change global dir variables properly before use.
"""

from math import sqrt
import datetime
import subprocess

idealFileDir  = "data/"
outputFileDir = "data/"


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
        # total += sub ** 2
        total += abs(sub)

    RMSE = sqrt(total/tested)
    elapsedTime = datetime.datetime.now() - startTime
    # 0.8454584 .714799906 14296 DIFF:5862
    # 1.595384 2.545250107 50905
    print("tested: ", tested)
    print("RMSE: " + format(RMSE, ".7f"))
    print(total, tested, total/tested)
    print(sorted(diff.items()))
    for k, v in sorted(diff.items()):
        print(k ** 2 * v, end="\t")
    print("Evaluation took " + str(elapsedTime.total_seconds()) + " seconds")
    print("\n")


if __name__ == "__main__":
    testNameList   = ["u1", "u2", "u3", "u4", "u5" ]

    for i in range(len(testNameList)):
        runEvaluation(testNameList[i])
