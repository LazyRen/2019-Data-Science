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
        self.label = -1


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
            dataList[int(pt)].label = cid
    totalCmp = 0
    incorrect = 0
    startTime = datetime.datetime.now()
    for pt1 in dataList:
        for pt2 in dataList:
            totalCmp += 1
            if (pt1 == pt2):
                continue
            if (pt1.idealLabel == pt2.idealLabel):
                continue
            if (pt1.label == pt2.label):
                incorrect += 1
            elif (pt1.label == -1 or pt2.label == -1):
                incorrect += 1
    correct = totalCmp - incorrect
    elapsedTime = datetime.datetime.now() - startTime
    print(str(totalPts*(totalPts-1)/2 - incorrect))
    print(str(totalPts*(totalPts-1)/2))
    print(str(correct) + " / " + str(totalCmp) + " = " + format((correct)/totalCmp*100, ".5f") + "%")
    print("Evaluation took " + str(elapsedTime.total_seconds()) + " seconds")
    print("\n")


if __name__ == "__main__":
    testNameList   = ["input1", "input2", "input3" ]
    clusterNumList = [8,        5,        4        ]
    epsList        = [15,       2,        5        ]
    minPtsList     = [22,       7,        5        ]

    for i in range(len(testNameList)):
        totalPts = len(loadData(inputFileDir + testNameList[i] + ".txt"))
        # totalPts = runDBSCAN(testNameList[i], clusterNumList[i], epsList[i], minPtsList[i])
        runEvaluation(testNameList[i], clusterNumList[i], totalPts)
