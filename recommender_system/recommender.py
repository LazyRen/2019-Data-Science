#!/usr/bin/env python3

from math import sqrt
from operator import itemgetter
import sys


# load data from file.
def loadData(fileName):
    with open(fileName, 'r') as openedFile:
        # [user_id] [item_id] [rating] ([time_stamp] deleted)
        return [line.rstrip('\n').split('\t')[:-1] for line in openedFile.readlines()]


def preprocessData(data):
    maxUID = -1
    maxMID = -1
    for row in data:
        maxUID = max(maxUID, int(row[0]))
        maxMID = max(maxMID, int(row[1]))

    # [maxUID * maxMID]
    ratingDict = [dict() for row in range(maxUID+1)]
    for row in data:
        uid = int(row[0]); mid = int(row[1]); rating = int(row[2])
        ratingDict[uid][mid] = rating
    for user in range(1, maxUID+1):
        ratingDict[user]['mean'] = sum(ratingDict[user].values()) / len(ratingDict[user])
    return ratingDict


def similarityMeasure(ratingDict):
    maxUID = len(ratingDict)
    similarityMatrix = [[0 for col in range(maxUID)] for row in range(maxUID)]

    # Calculate similarity using 'Pearson Correlation Coefficient'
    for user1 in range(1, maxUID):
        for user2 in range(user1+1, maxUID):
            commonItem = set(ratingDict[user1].keys()).intersection(ratingDict[user2].keys())
            if len(commonItem) is not 0:
                similarity = numerator = denominator1 = denominator2 = 0
                for item in commonItem:
                    val1 = (ratingDict[user1][item] - ratingDict[user1]['mean'])
                    val2 = (ratingDict[user2][item] - ratingDict[user2]['mean'])
                    numerator += val1 * val2
                    denominator1 += val1 ** 2
                    denominator2 += val2 ** 2
                if denominator1 and denominator2:
                    similarity = numerator / sqrt(denominator1 * denominator2)
                similarityMatrix[user1][user2] = similarityMatrix[user2][user1] = similarity

    return similarityMatrix


def findNeighbors(maxUID, similarityMatrix):
    neighbors = [[] for row in range(maxUID)]
    for user1 in range(1, maxUID):
        for user2 in range(1, maxUID):
            neighbors[user1].append((user2, similarityMatrix[user1][user2]))
        neighbors[user1] = sorted(neighbors[user1], key=itemgetter(1), reverse=True)

    return neighbors


def predictRating(uid, mid, ratingDict, similarityMeasure, neighbors):
    maxKNN = 50; checked = 0
    numerator = denominator = 0
    ret = ratingDict[uid]['mean']

    for neighbor in neighbors[uid]:
        user = neighbor[0]; similarity = neighbor[1]
        if ratingDict[user].get(mid) is None:
            continue
        if checked == maxKNN or similarity <= 0:
            break
        numerator += similarity * (ratingDict[user][mid] - ratingDict[user]['mean'])
        denominator += similarity
        checked += 1

    if denominator is 0:
        return round(ret)
    ret += numerator / denominator
    if ret >= 5:
        ret = 5
    elif ret < 1:
        ret = 1

    return round(ret)


def createOutputFile(ratingDict, similarityMeasure, neighbors):
    testData = loadData(sys.argv[2])
    outputFile = open(sys.argv[1][:sys.argv[1].find(".base")] + ".base_prediction.txt", 'w')

    for row in testData:
        uid = int(row[0]); mid = int(row[1])
        predict = predictRating(uid, mid, ratingDict, similarityMeasure, neighbors)
        outputFile.write('{}\t{}\t{}\n'.format(uid, mid, predict))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("2 arguments are required to run the program")
        print("***** USAGE *****")
        print("%s [train file] [test file]" % sys.argv[0])
        sys.exit("argv error")

    trainData = loadData(sys.argv[1])
    ratingDict = preprocessData(trainData)
    del trainData
    similarityMatrix = similarityMeasure(ratingDict)
    neighbors = findNeighbors(len(ratingDict), similarityMatrix)
    createOutputFile(ratingDict, similarityMatrix, neighbors)
