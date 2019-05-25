#!/usr/bin/env python3

from math import sqrt
from operator import itemgetter
import sys


# load data from file.
def loadData(fileName):
    """read 'fileName' file & return [[(user_id), (item_id), (rating)] * rows]."""
    with open(fileName, 'r') as openedFile:
        # [user_id] [item_id] [rating] ([time_stamp] deleted)
        return [[int(x) for x in line.rstrip('\n').split('\t')[:-1]] for line in openedFile.readlines()]


def preprocessData(data):
    """Create list of ratingDict from a loaded data

    Argument:
    data -- [[(user_id), (item_id), (rating)] * rows]
    Return:
    ratingDict[user][movie]  -- rating of moive of user (user & movie must be int)
    ratingDict[user]['mean'] -- mean of user's all rating
    Time Complexity = O(2r + u) # r = number of rows in data, u = number of users
    """
    maxUID = -1
    for row in data:
        maxUID = max(maxUID, row[0])

    ratingDict = [dict() for row in range(maxUID+1)]
    for row in data:
        uid = row[0]; mid = row[1]; rating = row[2]
        ratingDict[uid][mid] = rating
    for user in range(1, maxUID+1):
        ratingDict[user]['mean'] = sum(ratingDict[user].values()) / len(ratingDict[user])
    return ratingDict


def similarityMeasure(ratingDict):
    """Calculate similarity using PCC & return similarityMatirx in foam of 2D list.

    Time Complexity = O(u^2 * m) # u = number of users, m = number of movies
    Since m in time complexity refers to commonItem of two user, in most cases function will run in O(u^2).
    """
    maxUID = len(ratingDict)
    similarityMatrix = [[0 for col in range(maxUID)] for row in range(maxUID)]

    # Calculate similarity using 'Pearson Correlation Coefficient'
    for user1 in range(1, maxUID):
        for user2 in range(user1+1, maxUID):
            commonItem = set(ratingDict[user1].keys()).intersection(ratingDict[user2].keys())
            commonItem.remove('mean')
            if len(commonItem) is not 0:
                similarity = numerator = denominator1 = denominator2 = 0
                for item in commonItem:
                    val1 = ratingDict[user1][item] - ratingDict[user1]['mean']
                    val2 = ratingDict[user2][item] - ratingDict[user2]['mean']
                    numerator += val1 * val2
                    denominator1 += val1 ** 2
                    denominator2 += val2 ** 2
                if denominator1 and denominator2:
                    similarity = numerator / sqrt(denominator1 * denominator2)
                similarityMatrix[user1][user2] = similarityMatrix[user2][user1] = similarity

    return similarityMatrix


def findNeighbors(maxUID, similarityMatrix):
    """Find & sort neighbors based on the similarity.

    Return:
    neighbors -- 2D list containing (uid, similarity).
                 Each row is sorted in descending order of similarity.
    """
    neighbors = [[] for row in range(maxUID)]
    for user1 in range(1, maxUID):
        for user2 in range(1, maxUID):
            if user1 == user2:
                continue
            neighbors[user1].append((user2, similarityMatrix[user1][user2]))
        neighbors[user1] = sorted(neighbors[user1], key=itemgetter(1), reverse=True)

    return neighbors


def predictRating(uid, mid, ratingDict, similarityMeasure, neighbors):
    """Predict rating of movie(mid) for user(uid) using KNN collaborative filtering.

    Return:
    predicted value in int(1~5)
    """
    maxKNN = 50; checked = 0
    numerator = denominator = 0
    ret = ratingDict[uid]['mean']

    # Run KNN collaborative filtering.
    # Algorithm stops in advance if similarity reaches negative.
    for neighbor in neighbors[uid]:
        user = neighbor[0]; similarity = neighbor[1]
        if ratingDict[user].get(mid) is None:
            continue
        if checked == maxKNN or similarity <= 0:
            break
        numerator += similarity * (ratingDict[user][mid] - ratingDict[user]['mean'])
        denominator += similarity
        checked += 1

    ret = ratingDict[uid]['mean'] if denominator == 0 else ratingDict[uid]['mean'] + numerator / denominator
    if ret >= 5:
        ret = 5
    elif ret < 1:
        ret = 1

    return round(ret)


def createOutputFile(ratingDict, similarityMeasure, neighbors):
    """Predict all rating of <user, movie> pairs from test file and prints to base_prediction."""
    testData = loadData(sys.argv[2])
    outputFile = open(sys.argv[1][:sys.argv[1].find(".base")] + ".base_prediction.txt", 'w')

    for row in testData:
        uid = row[0]; mid = row[1]
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
