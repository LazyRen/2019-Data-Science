#!/usr/bin/env python3

from clustering import loadData, dbscan, createOutputFile
import datetime

inputFileDir  = "data/"
idealFileDir  = "test/"
outputFileDir = "test/"


class Point:
    def __init__(self, id):
        self.id = int(id)
        self.idealLabel = -1
        self.clusteredLabel = -1


def runDBSCAN(testName, maxClusterNum, eps, minPts):
    print("\nStarting DBSCAN: " + testName)
    dataList = loadData(inputFileDir + testName + ".txt")

    startTime = datetime.datetime.now()
    labelConverter = dbscan(dataList, maxClusterNum, eps, minPts)
    elapsedTime = datetime.datetime.now() - startTime
    print("DBSCAN for " + testName + " took " + str(elapsedTime.total_seconds()) + " seconds")

    startTime = datetime.datetime.now()
    createOutputFile(dataList, maxClusterNum, labelConverter, outputFileDir + testName)
    elapsedTime = datetime.datetime.now() - startTime
    print("creating result files for " + testName + " took " + str(elapsedTime.total_seconds()) + " seconds")
    print("\n")
    return len(dataList)


def loadClusters(testName, maxClusterNum, suffix):
    clusterList = []
    for i in range(maxClusterNum):
        cluster = [line.rstrip('\n') for line in open(testName + "_cluster_" + str(i) + suffix + ".txt", 'r')]
        clusterList.append(cluster)
    return clusterList


def findClusterID(pid, clusterList):
    for i in range(len(clusterList)):
        if pid in clusterList[i]:
            return i

    # point with pid does not exist in clusterList
    # Meaning point was considered as outlier or belongs to extra(removed) cluster.
    return -1


def runEvaluation(testName, maxClusterNum, totalPts):
    print("Starting Evaluation: " + testName)
    idealClusterList = loadClusters(idealFileDir + testName, maxClusterNum, "_ideal")
    createdClusterList = loadClusters(outputFileDir + testName, maxClusterNum, "")
    dataList = [Point(i) for i in range(totalPts)]
    for cid, cluster in enumerate(idealClusterList):
        for pt in cluster:
            dataList[int(pt)].idealLabel = cid
    for cid, cluster in enumerate(createdClusterList):
        for pt in cluster:
            dataList[int(pt)].clusteredLabel = cid

    totalCmp = 0
    incorrect = 0
    startTime = datetime.datetime.now()
    for i in range(len(dataList)-1):
        pt1 = dataList[i]
        for j in range(i+1, len(dataList)):
            pt2 = dataList[j]
            if (pt1.idealLabel == -1 or pt2.idealLabel == -1):
                continue
            totalCmp += 1
            if (pt1.idealLabel == pt2.idealLabel):
                if (pt1.clusteredLabel != pt2.clusteredLabel):
                    incorrect += 1
            elif (pt1.clusteredLabel == pt2.clusteredLabel):
                incorrect += 1

    correct = totalCmp - incorrect
    elapsedTime = datetime.datetime.now() - startTime
    print(str(correct) + " / " + str(totalCmp) + " = " + format((correct)/totalCmp*100, ".5f") + "%")
    print("Evaluation took " + str(elapsedTime.total_seconds()) + " seconds")
    print("\n")


if __name__ == "__main__":
    testNameList   = ["input1", "input2", "input3" ]
    clusterNumList = [8,        5,        4        ]
    epsList        = [15,       2,        5        ]
    minPtsList     = [22,       7,        5        ]

    userInput = -1
    while(True):
        print("******************** USAGE *********************")
        print("1. Use existing outputfiles at " + outputFileDir)
        print("2. Run DBSCAN to create new outputFiles")
        userInput = int(input("Input: "))
        print("\n")
        if (userInput == 1 or userInput == 2):
            break

    for i in range(len(testNameList)):
        if (userInput == 1):
            totalPts = len(loadData(inputFileDir + testNameList[i] + ".txt"))
        elif (userInput == 2):
            totalPts = runDBSCAN(testNameList[i], clusterNumList[i], epsList[i], minPtsList[i])
        runEvaluation(testNameList[i], clusterNumList[i], totalPts)
