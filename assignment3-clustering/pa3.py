#!/usr/bin/env python3

"""
This file is intended to be used by anyone with own output files & ideal files.
Change global dir variables properly before use.
"""

import datetime

inputFileDir  = "data/"
idealFileDir  = "test/"
outputFileDir = "test/"


class Point:
    def __init__(self, id):
        self.id = int(id)
        self.idealLabel = -1
        self.clusteredLabel = -1


def loadClusters(testName, maxClusterNum, suffix):
    clusterList = []
    for i in range(maxClusterNum):
        cluster = [line.rstrip('\n') for line in open(testName + "_cluster_" + str(i) + suffix + ".txt", 'r')]
        clusterList.append(cluster)
    return clusterList


def runEvaluation(testName, maxClusterNum, totalPts):
    print("Starting Evaluation: " + testName)
    idealClusterList = loadClusters(idealFileDir + testName, maxClusterNum, "_ideal")
    createdClusterList = loadClusters(outputFileDir + testName, maxClusterNum, "")
    dataList = [Point(i) for i in range(totalPts)]
    totalIdealPts = 0
    totalCreatedPts = 0
    for cid, cluster in enumerate(idealClusterList):
        totalIdealPts += len(cluster)
        for pt in cluster:
            dataList[int(pt)].idealLabel = cid
    for cid, cluster in enumerate(createdClusterList):
        totalCreatedPts += len(cluster)
        for pt in cluster:
            dataList[int(pt)].clusteredLabel = cid
    print(str(totalIdealPts) + " points are clustered in ideal files")
    print(str(totalCreatedPts) + " points are clustered in output files")

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
    totalPts       = [8000,     2000,     2100     ]

    for i in range(len(testNameList)):
        runEvaluation(testNameList[i], clusterNumList[i], totalPts[i])
