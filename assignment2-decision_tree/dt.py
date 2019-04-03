#!/usr/bin/env python3

from collections import defaultdict, Counter
from math import log
import sys

class Node:
	def __init__(self, parent, attr, isLeaf = False, classLabel = ""):
		self.parent = parent
		self.attr = attr
		self.children = dict()
		self.isLeaf = isLeaf
		self.classLabel = classLabel
	def __repr__(self):
		if self.isLeaf:
			return "Leaf Node"
		else:
			return "Internal Node"
	def __str__(self):
		ret = repr(self) + "\n"
		if self.isLeaf:
			ret += "classLabel: " + self.classLabel + "\n"
		else:
			ret += "attr: " + self.attr + "\n"
		return ret

def loadData(fileName, header, rows, attrValues = None):
	with open(fileName, 'r') as openedFile:
		header.extend(openedFile.readline().rstrip('\n').split('\t'))
		if attrValues is not None:
			headerLength = len(header)
			for line in openedFile.readlines():
				line = line.rstrip('\n').split('\t')
				rows.extend([line])
				for col in range(headerLength):
					attrValues[header[col]].add(line[col])
		else:
			rows.extend(line.rstrip('\n').split('\t') for line in openedFile.readlines())



def calcEntropy(classified):
	ret = 0.0
	for val in classified:
		p = val / sum(classified)
		ret -= p * log(p, 2)
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
			entropy += sum(classified.values()) / DBsize * calcEntropy(classified.values())
		infoGains.append(totalEntropy - entropy)
	return infoGains

def attributeSelection(rows):
	infoGains = calcGains(rows)
	return infoGains.index(max(infoGains))

def generateTree(parent, attributes, dataPartitions, attrValues):
	classList = [row[-1] for row in dataPartitions]
	classCounter = Counter(classList)
	majorityVoted = classCounter.most_common(1)[0][0]
	# 1: tuples are all of the same class
	if (classCounter.most_common(1)[0][1] == len(classList)):
		return Node(parent, "", True, majorityVoted)

	# 2: attributes lits is empty MAJORITY VOTING
	if len(attributes) == 0:
		return Node(parent, "", True, majorityVoted)

	del classList
	del classCounter
	selectedAttrIdx = attributeSelection(dataPartitions)
	curNode = Node(parent, attributes[selectedAttrIdx])
	del attributes[selectedAttrIdx]
	partition = defaultdict(lambda: [])
	for row in dataPartitions:
		attrValue = row[selectedAttrIdx]
		del row[selectedAttrIdx]
		partition[attrValue].append(row)
	dataPartitions.clear()
	for attrValue in attrValues[curNode.attr]:
		if not partition[attrValue]:# partition is empty
			curNode.children[attrValue] = Node(curNode, "", True, majorityVoted)
		else:# recursively generate subtree
			curNode.children[attrValue] = generateTree(curNode, attributes, partition[attrValue], attrValues)
	attributes.insert(selectedAttrIdx, curNode.attr)
	return curNode

def classification(node, attributes, sample, debugFlag = False):
	if debugFlag:
		print(str(node) + "\n")
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

if __name__ == "__main__":
	attrHeader = list()
	samples = list()
	attrValues = defaultdict(lambda: set())
	if len(sys.argv) != 4:
		print("3 arguments are required to run the program")
		print("***** USAGE *****")
		print("%s [train file] [test file] [result file]" % sys.argv[0])
		sys.exit("argv error")
	loadData(sys.argv[1], attrHeader, samples, attrValues)
	decisionTree = generateTree(None, attrHeader, samples, attrValues)
	generateResult(sys.argv[2], sys.argv[3], decisionTree, attrHeader)
