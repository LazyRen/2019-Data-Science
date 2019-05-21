#!/usr/bin/env python3

import sys
from math import sqrt

output_file = ""


# load data from file.
def loadData(fileName):
    with open(fileName, 'r') as openedFile:
        # [user_id] [item_id] [rating] [time_stamp]
        return [line.rstrip('\n').split('\t')[:-1] for line in openedFile.readlines()]


def preprocessData(data):
    maxUID = -1
    maxMID = -1
    for row in data:
        maxUID = max(maxUID, int(row[0]))
        maxMID = max(maxMID, int(row[1]))

    # [maxUID * maxMID]
    ratingMatrix = [[None for col in range(maxMID+1)] for row in range(maxUID+1)]
    ratingDict = [dict() for row in range(maxUID+1)]
    for row in data:
        uid = int(row[0]); mid = int(row[1]); rating = int(row[2])
        ratingMatrix[uid][mid] = rating
        ratingDict[uid][mid] = rating
    for user in range(1, maxUID+1):
        ratingDict[user]['mean'] = sum(ratingDict[user].values()) / len(ratingDict[user])
    return ratingMatrix, ratingDict


def similarityMeasure(ratingMatrix, ratingDict):
    maxUID = len(ratingDict)
    similarityMatrix = [[0 for col in range(maxUID)] for row in range(maxUID)]

    # Calculate similarity using 'Pearson Correlation Coefficient'
    for user1 in range(1, maxUID):
        for user2 in range(user1+1, maxUID):
            commonItem = set(ratingDict[user1].keys()).intersection(ratingDict[user2].keys())
            # user1_meanRating = sum(ratingDict[user1].values()) / len(ratingDict[user1])
            # user2_meanRating = sum(ratingDict[user2].values()) / len(ratingDict[user2])
            if len(commonItem) is not 0:
                similarity = numerator = denominator1 = denominator2 = 0
                for item in commonItem:
                    val1 = (ratingDict[user1][item] - ratingDict[user1]['mean'])
                    val2 = (ratingDict[user2][item] - ratingDict[user2]['mean'])
                    numerator += val1 * val2
                    denominator1 += val1 ** 2
                    denominator2 += val2 ** 2
                if denominator1 and denominator2:
                    similarity = numerator / (sqrt(denominator1 * denominator2))
                similarityMatrix[user1][user2] = similarityMatrix[user2][user1] = similarity
    return similarityMatrix


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("2 arguments are required to run the program")
        print("***** USAGE *****")
        print("%s [train file] [test file]" % sys.argv[0])
        sys.exit("argv error")

    trainData = loadData(sys.argv[1])
    ratingMatrix, ratingDict = preprocessData(trainData)
    del trainData
    similarityMeasure(ratingMatrix, ratingDict)

    output_file = sys.argv[1][sys.argv[1].find("u"):sys.argv[1].find(".base")] + ".base_prediction.txt"
    print(output_file)
