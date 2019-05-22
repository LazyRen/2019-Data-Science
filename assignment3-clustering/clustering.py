#!/usr/bin/env python3

import sys
from random import randint
from operator import itemgetter


class Point:
    def __init__(self, id, x, y):
        self.id = int(id)
        self.x = float(x)
        self.y = float(y)
        self.isVisited = False
        self.label = -1

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        ret = "("
        ret += str(self.id) + ": "
        ret += str(self.x) + ", "
        ret += str(self.y) + ")"
        return ret


def loadData(fileName):
    """read 'fileName' and return list of Point objects."""
    with open(fileName, 'r') as openedFile:
        dataList = []
        for line in openedFile.readlines():
            line = line.rstrip('\n').split('\t')
            pt = Point(line[0], line[1], line[2])
            dataList.append(pt)
        return dataList


def findNeighbor(cur, dataList, eps):
    """Find all neighbors from cur pt.
    Neighbors must be positioned within radius of 'eps'.
    Time Complexity = O(n)
    """
    neighbors = []
    for pt in dataList:
        if (cur.x - pt.x) ** 2 + (cur.y - pt.y) ** 2 <= eps ** 2:
            neighbors.append(pt)
    return neighbors


def dbscan(dataList, maxClusterNum, eps, minPts):
    """Iterate all points to classify them as a cluster.
    Return value 'labelConverter' is used to convert labels of cluster with small size to -1
    if (# of clusters > maxClusterNum).
    Time Complexity = O(n^2)
    TODO : recluster converted points since they can be a density-connected to remained clusters.
    """
    unvisitedPt = list(dataList)
    clusterSizeList = []
    lastClusterID = 0
    # lookup all unvisited Points
    while (len(unvisitedPt) != 0):
        idx = randint(0, len(unvisitedPt) - 1)
        cur = unvisitedPt[idx]
        cur.isVisited = True
        del unvisitedPt[idx]

        # Create new cluster if 'cur' pt. is core object
        neighborhood = findNeighbor(cur, dataList, eps)
        if (len(neighborhood) >= minPts):
            cur.label = lastClusterID
            clusterSize = 1
            idx = -1
            # find all density-connected points(neighborhood)
            while (idx < len(neighborhood) - 1):
                idx += 1
                if (neighborhood[idx].isVisited):
                    continue
                neighborhood[idx].isVisited = True
                unvisitedPt.remove(neighborhood[idx])
                nextNeighbor = findNeighbor(neighborhood[idx], dataList, eps)
                if (len(nextNeighbor) >= minPts):
                    # extend neighborhood without duplicate
                    neighborhood = neighborhood + [x for x in nextNeighbor if x not in neighborhood]
                if (neighborhood[idx].label == -1):
                    neighborhood[idx].label = lastClusterID
                    clusterSize += 1
            clusterSizeList.append((lastClusterID, clusterSize))
            lastClusterID += 1

    # Create labelConverter to remove extra clusters if exist.
    labelConverter = dict()
    labelConverter[-1] = -1
    if (lastClusterID <= maxClusterNum):  # no need to remove extra clusters
        for i in range(maxClusterNum):
            labelConverter[i] = i
    else:                                 # create labelConverter that remove extra clusters
        clusterSizeList.sort(key=itemgetter(1), reverse=True)
        for i in range(maxClusterNum):
            labelConverter[clusterSizeList[i][0]] = i
        for i in range(maxClusterNum, lastClusterID):
            labelConverter[clusterSizeList[i][0]] = -1
    return labelConverter


def createOutputFile(dataList, maxClusterNum, labelConverter, filePrefix):
    """Create (maxClusterNum) of output files containing pts' id.
    Each output file represents one cluster.
    If necessary, use labelConverter to reduce number of clusters.
    Time Complexity = O(n)
    """
    outputFileList = []
    for i in range(maxClusterNum):
        outputFileList.append(open(filePrefix + "_cluster_" + str(i) + ".txt", 'w'))

    for pt in dataList:
        matchingCluster = labelConverter[pt.label]
        if matchingCluster == -1:
            continue
        outputFileList[matchingCluster].write(str(pt.id) + '\n')

    for i in range(maxClusterNum):
        outputFileList[i].close()

# data/input1.txt 8 15 22
# data/input2.txt 5 2 7
# data/input3.txt 4 5 5
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("4 arguments are required to run the program")
        print("***** USAGE *****")
        print("%s [input file] [number of clusters] [Eps] [MinPts]" % sys.argv[0])
        sys.exit("argv error")

    dataList = loadData(sys.argv[1])
    maxClusterNum = int(sys.argv[2])
    eps = int(sys.argv[3])
    minPts = int(sys.argv[4])

    labelConverter = dbscan(dataList, maxClusterNum, eps, minPts)
    createOutputFile(dataList, maxClusterNum, labelConverter, sys.argv[1][:sys.argv[1].find(".txt")])
