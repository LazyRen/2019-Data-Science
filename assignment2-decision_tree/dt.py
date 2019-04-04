#!/usr/bin/env python3

from collections import defaultdict, Counter
from math import log
import sys

# Basic Node class that constructs decision tree
class Node:
	def __init__(self, parent, attr, classLabel, cnt, isLeaf = False):
		self.parent = parent
		self.attr = attr
		self.children = dict()
		self.classLabel = classLabel
		self.cnt = cnt
		self.isLeaf = isLeaf
	def __repr__(self):
		if self.isLeaf:
			return "Leaf Node"
		else:
			return "Internal Node"
	def __str__(self):
		ret = repr(self) + "\n"
		if not self.isLeaf:
			ret += "attr: " + self.attr + "\n"
		ret += "classLabel: " + self.classLabel + "\n"
		ret += "count: " + str(self.cnt) + "\n"
		return ret

# load data from file.
def loadData(fileName, header, rows, getAttrValue = False):
	with open(fileName, 'r') as openedFile:
		header.extend(openedFile.readline().rstrip('\n').split('\t'))
		if getAttrValue:
			attrValues = defaultdict(lambda: defaultdict(lambda: 0))
			headerLength = len(header)
			for line in openedFile.readlines():
				line = line.rstrip('\n').split('\t')
				rows.extend([line])
				for col in range(headerLength):
					attrValues[header[col]][line[col]] += 1
			return attrValues
		else:
			rows.extend(line.rstrip('\n').split('\t') for line in openedFile.readlines())
			return None

def calcEntropy(classified):
	info = 0.0
	for val in classified:
		p = val / sum(classified)
		info -= p * log(p, 2)
	return info

def calcSplitInfo(classCounter, totalD):
	splitInfo = 0.0
	for classified in classCounter.values():
		partition = sum(classified.values()) / totalD
		splitInfo -= partition * log(partition, 2)
	return splitInfo

# Calculate gain ratio to be precise.
def calcGains(rows):
	infoGains = []
	totalD = len(rows)
	totalEntropy = calcEntropy(Counter([row[-1] for row in rows]).values())
	for col in range(len(rows[0]) - 1):
		entropy = 0.0
		# {attrValue : {className : cnt}}
		classCounter = defaultdict(lambda: defaultdict(lambda: 0))
		for row in rows:
			classCounter[row[col]][row[-1]] += 1
		for classified in classCounter.values():
			entropy += sum(classified.values()) / totalD * calcEntropy(classified.values())
		infoGains.append((totalEntropy - entropy) / calcSplitInfo(classCounter, totalD))
	return infoGains

# Calculate all gain ratio of attributes at the moment.
# Return index of most highest value.
def attributeSelection(rows):
	infoGains = calcGains(rows)
	return infoGains.index(max(infoGains))

# If there is a tie, return attribute that has least amount.
# 318 -> 322 boosted.
def getMajorityVoted(classCounter, classHeader, attrValues):
	candidates = classCounter.most_common()
	vote = candidates[0][1]
	candidates = [x for x in candidates if x[1] == vote]
	voted = candidates[0][0]
	if len(candidates) == 1:
		return voted
	vote = attrValues[classHeader][voted]
	for candidate in candidates:
		if vote > attrValues[classHeader][candidate[0]]:
			vote = attrValues[classHeader][candidate[0]]
			voted = candidate[0]
	return voted

# Generate decision tree. This function is used recursively to produce it.
# Majority vote will always be saved to the node for the debugging purpose.
# Recursion ends at 3 conditions.
# 1: tuples are all of the same class
# 2: attributes lits is empty MAJORITY VOTING
# 3: partition is empty.
def generateTree(parent, attributes, dataPartitions, attrValues):
	classList = [row[-1] for row in dataPartitions]
	classCounter = Counter(classList)
	majorityVoted = getMajorityVoted(classCounter, attributes[-1], attrValues)
	# majorityVoted = classCounter.most_common(1)[0][0]
	totalLines = len(dataPartitions)

	# 1: tuples are all of the same class
	if (classCounter.most_common(1)[0][1] == len(classList)):
		return Node(parent, "", majorityVoted, totalLines, True)
	# 2: attributes lits is empty MAJORITY VOTING
	if len(attributes) == 0:
		return Node(parent, "", majorityVoted, totalLines, True)

	del classList
	del classCounter
	selectedAttrIdx = attributeSelection(dataPartitions)
	curNode = Node(parent, attributes[selectedAttrIdx], majorityVoted, totalLines)
	del attributes[selectedAttrIdx]
	partition = defaultdict(lambda: [])
	for row in dataPartitions:
		attrValue = row[selectedAttrIdx]
		del row[selectedAttrIdx]
		partition[attrValue].append(row)
	dataPartitions.clear()

	for attrValue in attrValues[curNode.attr]:
		if not partition[attrValue]:# 3: partition is empty no further recursion
			curNode.children[attrValue] = Node(curNode, "", majorityVoted, totalLines, True)
		else:# recursively generate subtree
			curNode.children[attrValue] = generateTree(curNode, attributes, partition[attrValue], attrValues)
	attributes.insert(selectedAttrIdx, curNode.attr)

	return curNode

# Find the prediction of classLabel for the sample.
def classification(node, attributes, sample, debugFlag = False):
	if debugFlag:
		print(node)
	if node.isLeaf:
		return node.classLabel
	return classification(node.children[sample[attributes.index(node.attr)]], attributes, sample, debugFlag)

def generateResult(testFile, resultFile, tree, attrHeader):
	testHeader = list()
	testSamples = list()
	loadData(testFile, testHeader, testSamples)
	with open(resultFile, 'w') as outFile:
		outFile.write("")
		outFile.write('\t'.join(attrHeader) + '\n')
		for sample in testSamples:
			result = classification(tree, testHeader, sample)
			outFile.write('\t'.join(sample) + '\t' + result + '\n')

# Helper fuction for the pruning.
# Calculate how many classifications are correct out of samples based on current tree
# Can be only used for the samples with classLabel.
def getPredictionCnt(tree, attributes, samples):
	cnt = 0
	for row in samples:
		t = classification(tree, attributes, row)
		if row[-1] == classification(tree, attributes, row):
			cnt += 1
	return cnt

# Recursive function for the pruning.
def _pruning(tree, node, attributes, samples, prevCnt):
	if node.isLeaf:
		return False
	node.isLeaf = True
	cnt = getPredictionCnt(tree, attributes, samples)
	node.isLeaf = False
	isSubPruned = False
	for child in node.children.values():
		tmp = _pruning(tree, child, attributes, samples, max(prevCnt, cnt))
		if tmp:
			isSubPruned = True
	if not isSubPruned and cnt > prevCnt:
		node.isLeaf = True
		return True

# function name tells everything.
# Is not activated because pruning decreases the accuracy at the moment.
def reducedErrorPruning(tree, attrHeader, samples):
	_pruning(tree, tree, attrHeader, samples, getPredictionCnt(tree, attrHeader, samples))

if __name__ == "__main__":
	attrHeader = list()
	samples = list()

	if len(sys.argv) != 4:
		print("3 arguments are required to run the program")
		print("***** USAGE *****")
		print("%s [train file] [test file] [result file]" % sys.argv[0])
		sys.exit("argv error")
	attrValues = loadData(sys.argv[1], attrHeader, samples, True)
	decisionTree = generateTree(None, attrHeader, samples, attrValues)
	generateResult(sys.argv[2], sys.argv[3], decisionTree, attrHeader)
