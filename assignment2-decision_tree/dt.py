#!/usr/bin/env python3

from collections import defaultdict, Counter
import math
import sys

class Node:
	def __init__(self, parent, attr, isLeaf=False):
		self.parent = parent
		self.attr = attr
		self.children = dict()
		self.isLeaf = isLeaf
		self.classLabel = ""
		if parent == None:
			self.level = 1
		else:
			self.level = parent.level + 1

attrHeader = list()
samples = list()

def loadData(fileName, header, rows):
	with open(fileName, 'r') as openedFile:
		header.extend(openedFile.readline().rstrip('\n').split('\t'))
		rows.extend(line.rstrip('\n').split('\t') for line in openedFile.readlines())

def calcEntropy(classified):
	ret = 0.0
	for val in classified:
		# print("val", val)
		p = val / sum(classified)
		ret -= p * math.log(p, 2)
	return ret

def calcGains(rows):
	infoGains = []
	DBsize = len(rows)
	totalEntropy = calcEntropy(Counter([row[-1] for row in rows]).values())
	for col in range(len(rows[0]) - 1):
		entropy = 0.0
		# {attrValue : {className : cnt}}
		classCounter = defaultdict(lambda: defaultdict(lambda: 0))
		for row in rows:
			classCounter[row[col]][row[-1]] += 1
		for classified in classCounter.values():
			# print(sum(classified.values()), DBsize, calcEntropy(classified.values()))
			entropy += sum(classified.values()) / DBsize * calcEntropy(classified.values())
		# print(entropy)
		infoGains.append(totalEntropy - entropy)
	return infoGains

def attributeSelection(rows):
	infoGains = calcGains(rows)
	print(infoGains, max(infoGains))
	return infoGains.index(max(infoGains))

def generateTree(parent, attributes, dataPartitions):
	classList = [row[-1] for row in dataPartitions]
	classCounter = Counter(classList)
	# 1: tuples are all of the same class
	if (classCounter.most_common(1)[0][1] == len(classList)):
		curNode = Node(parent, "", True)
		curNode.classLabel = classCounter.most_common(1)[0][0]
		return curNode

	# 2: attributes lits is empty MAJORITY VOTING
	if len(attributes) == 0:
		curNode = Node(parent, "", True)
		curNode.classLabel = classCounter.most_common(1)[0][0]
		return curNode
	print(attributes)
	selectedAttrIdx = attributeSelection(dataPartitions)
	# print(attributes)
	curNode = Node(parent, attributes[selectedAttrIdx])
	del attributes[selectedAttrIdx]
	partition = defaultdict(lambda: [])
	for idx, row in enumerate(dataPartitions):
		partition[row[selectedAttrIdx]].append(row)
	dataPartitions.clear()
	for item in partition.items():
		curNode.children[item[0]] = generateTree(curNode, attributes, item[1])
	attributes.insert(selectedAttrIdx, curNode.attr)
	# print(attributes)
	return curNode

def _classification(node, attributes, sample):
	if node.isLeaf:
		return node.classLabel


def classification(testFile, resultFile, tree):
	testHeader = list()
	testSamples = list()
	loadData(testFile, testHeader, testSamples)
    with open(resultFile, 'w') as outFile:
		outFile.write('\t'.join(attrHeader))
        for sample in testSamples:
            #찾아낸 class를 바탕으로 정답을 출력한다.
            result = _classification(tree, testHeader, sample)
			outFile.write('\t'.join(sample) + '\t' + result)

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print("3 arguments are required to run the program")
		print("***** USAGE *****")
		print("%s [train file] [test file] [result file]" % sys.argv[0])
		sys.exit("argv error")

	loadData(sys.argv[1], attrHeader, samples)
	# print(attrHeader)
	# print(samples)
	decisionTree = generateTree(None, attrHeader, samples)
	classification(sys.argv[2], sys.argv[3], tree)
