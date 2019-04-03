#!/usr/bin/env python3

from collections import defaultdict, Counter
import math
import sys

class Node:
	def __init__(self, parent, attr, isLeaf=False, classLabel=""):
		self.parent = parent
		self.attr = attr
		self.children = dict()
		self.isLeaf = isLeaf
		self.classLabel = classLabel

attrHeader = list()
samples = list()
attrValues = defaultdict(lambda: set())

def loadData(fileName, header, rows, attrValues=None):
	with open(fileName, 'r') as openedFile:
		header.extend(openedFile.readline().rstrip('\n').split('\t'))
		if attrValues is not None:
			headerLength = len(header)
			for line in openedFile.readlines():
				line = line.rstrip('\n').split('\t')
				rows.extend([line])
				for col in range(headerLength):
					attrValues[header[col]].add(line[col])
			print(rows)
		else:
			rows.extend(line.rstrip('\n').split('\t') for line in openedFile.readlines())
			print(rows)



def calcEntropy(classified):
	ret = 0.0
	for val in classified:
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
			entropy += sum(classified.values()) / DBsize * calcEntropy(classified.values())
		infoGains.append(totalEntropy - entropy)
	return infoGains

def attributeSelection(rows):
	infoGains = calcGains(rows)
	return infoGains.index(max(infoGains))

def generateTree(parent, attributes, dataPartitions):
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
		else:
			curNode.children[attrValue] = generateTree(curNode, attributes, partition[attrValue])
	# for item in partition.items():
	# 	curNode.children[item[0]] = generateTree(curNode, attributes, item[1])
	attributes.insert(selectedAttrIdx, curNode.attr)
	return curNode

def _classification(node, attributes, sample):
	if node.isLeaf:
		return node.classLabel
	print(node.attr)
	print(attributes, attributes.index(node.attr), sample[attributes.index(node.attr)])
	print(node.children)
	return _classification(node.children[sample[attributes.index(node.attr)]], attributes, sample)

def classification(testFile, resultFile, tree):
	testHeader = list()
	testSamples = list()
	loadData(testFile, testHeader, testSamples)
	with open(resultFile, 'w') as outFile:
		outFile.write('\t'.join(attrHeader) + '\n')
		for sample in testSamples:
			result = _classification(tree, testHeader, sample)
			outFile.write('\t'.join(sample) + '\t' + result + '\n')

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print("3 arguments are required to run the program")
		print("***** USAGE *****")
		print("%s [train file] [test file] [result file]" % sys.argv[0])
		sys.exit("argv error")
	loadData(sys.argv[1], attrHeader, samples, attrValues)
	decisionTree = generateTree(None, attrHeader, samples)
	classification(sys.argv[2], sys.argv[3], decisionTree)
