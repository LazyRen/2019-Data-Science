#!/usr/bin/env python3

import sys
import random
from timeit import default_timer as timer

originalInput = """7	14
9
18	2	4	5	1
1	11	15	2	7	16	4	13
2	1	16
15	7	6	11	18	9	12	19	14
11	2	13	4
11	13
7	4	2	17	19	3	8	16	1
18	16	15	10	2	8	6	0	4	5
9
10
1	13	8	9	3	16	4
16	0	6	11	8
19	6	3	8	16	17
18	2	9	1	13	15	19	4	10
6	13	1	5	4	12	10	9
13	17	12	6	10	1	16	15
15	14	11	12	10	1	4	6
7
7	17
7	13	3	8	16	5	9	18
8	2
6	10	13	8	0	11	2
10	19	4	17	8	3
1	2	10	11	16	14
16
8	19
4	1	14	13	19	18	0	8	7
8	13	3	16	7	1	10
13	14	9	16	15	11	0	19
18	3	8	16	4	9	2
5	13	3	8	16	7
3	8	16	0	18
0	16	18	1	9	17	12	2	19
17
11	15	8	16	2	14	12	6	13
2	4	16	1	18	11	19	17	12	9
12	0	10	3	8	16	9
8	1
15	3	8	16	2	5	6	17	12	9
1	9	16	8	12
15	14	9	1	12	5
18
19	3	8	16
9	17	6	13	15	16	5	8
15	14	1
11	6	3	8	16	13	15
13	12	8	5	16	1
6	2	1	4	16	9	15	10	13
4	19	12	13	14	10	5
6	13	14	2	8	18	7	5	11	17
14	4	12	19	13
7
18	17	13	10	3	8	16	12
2	0	13	7	19	5
4	3	8	16	12
1	3
5	13	11
2	6	4
7
13
10	15	13	11	0
7	5	10	0	14	15	4
5	16	14	18	2	11	6	13	4	19
0	7	6
17
15
7	3	8	16	18	4	9
6	5	7
14	5	7	9	8	3	16	0
2	3	8	16
1	15	5	4	0	2	16	10
11	7	13	0	10	4	8
0	11	2	9
13
18	5	7	17	0	19	3	8	16	4
8	13	7	1	10	0	4	5
11
15	16	12	10	3
16	6	17	11	9	1
2	17	12	16	5	1	3
9	5	19	12	16	15	13	2	4	14
12	17	9	3	8	16	7
11	15	7	8
18	3	8	16	2	14
1	15
5	1	10	6	14	3	8	16	18	19
13	14
14	16	13	5	2	8	1	0
1	15	2	11
4	18	12	3	8	16	13	0
15	12	18	10
12	15	9	11	0	8	5	10
9	10	5	13	14	11	0	4
15	19	12	5	4	1	3	8	16	9
8	12	17	9	16	1
7	1	9	0	13	14	17	15
13	12	4	1
19	10	8
4	15	6	18	10	7	3	8	16	1
6	3	8	16	10
9	0
2	19	13	11	4
12	10	5	15	19	3	8	16	2
7	4	8	11	13	15	5	12	6
9	2	19	5	4	0	8	18	10
3	8	16	12
12	7	10
1	3	8	16	7
9
5	8	3	16	7
3	8	16	17	9	1	2	0	18
8	6	10	9	3
0
7	16	3	8	15	6	5	18
9	4	8	3
17	6	4	15	18	11	5	1	9	16
15	4	2	13	16
12	6	13	9	4	5	15	16	1
14	16	12	18	2
15	11	10	1	5	17
10	2	14	13	16	12	8
13	14	3
3	8	16	4	17
9	8	0	18
10	15	1	4	3	8	16	9	2
9	8
13	14	0
3	8	16	11
18	19	8	11	3	16	5	1	4
5	13	18
2	18	17	10	1	14	8	19	13	15
17	9	18	0	11	4	15	10	19	12
2	14	5	10	4	0	15	11	1
19	10	18	13	8	17
16	9	13
1	10	3	8	16	4	18	0	11
14	11	13	7	15	8
16	9	10	18	13	6
16
7	8	19	4	1	5	6	16	0	2
4	9
2	13	4	1	5	3
6	8
2	7	1	12	16	10	14	9	4
10	13	16	12	14	5	8
11	12	14	19	18	2	4	15	9
18	3	8	16	6	19	2	13	12	17
7	18	2	10	12	0
19	12	8	2	0	15	7	16	17
17	8	11	16	10	9	5	18	0
0
2	15	12	1	14	18	6	8
18	3	8	16	15	1	14	10	5	4
2	1	4	9	10	3	8	16	13
10	17	16	18	13	14
11	9	15	5	17
17	3	8	16	4
8
1	5	12	13	14	16	6	9	0
19	3	8	16	11
9	19
5	16	10	15	9	4
13	14	9	0	15	1	12
18	11	8	6	10	2	14	19	12
11	15	4
4	2	15	0	14
1	2	7
9	5	15	14	10	3	8	16	1
12	19	8
2	7	8
8	3	16	19	14
6	19	18	5	0
12	7	16	14	1	3	8	2
16	3
3	8	16	2	18	0	11	10	5
6	17	9	3	8	16	14
8	11	16	3	7	6
17	12
7	8	5	18
3	8	16	13	1	10	11	9
14	9	1
7	13	14	12	10	1
17	10	2
1	10	3	8	16	17
19	15	9	7
10	2	18
7	10	8	11	18	13	0
6	2	10	12
14	1	18	3	8	16	7	5	17
14
18	1	3	8	16	7	9	15	5
6	13	0	10	8	12
0	6	15	10
17	12	2	8	9	4	14	7	15	3
15	1	9	0	12	8	3	16	11
13	11	0	14	10
19	0	18	11	4	7	5	3
12	13	11	0	14	17	5	9	10
18	19	11	17	13	0	6	16	10	2
19	18	9	4	12	0	8	7	17
10	7	16	14
11	19	1
10	3	8	16	12	1	14
2	16	0	15
19	16	0	18	12
4	0	17	6	10	1	2	9
18	5	1	15
16	18	19	17	10	7	9
15	18
13	19	4	5	8	12	3
14	8	15	11	13	2	6	4	17	9
14	11	9	12	6	13	15
17	0	12	16	11	7	6	2	15	3
0	17	5	13	1
18	0	11	7	5	10	15	9	13
14	2	7	12	16	10
11	7
19	1	18	11	7	8
16	19	9	2	6	15	8
0	13	17	8	3
11	2
17	6	12	1	16	15
4	18	15	16	14	19	13	2
3	8	16	13	12	7
6
10	1	19	15	3	8	16	13	5
14	10	13	1
19	10	3	8	16	5	12	9
12	16
7	10
5	12
9	0	5
18	13
18	8	6	11	16	17	0
9	8	4	18	17
6	4	8	17	18	10
5	6	19	0	10	11	13	15	18	7
4	6	7	0	14	11	12	8
5	17	11	4
6	8	2	13	0	17	18	15
7	1	13	4	17	2	5	15	12	6
3	8	16	13	0	11	19
0	11	13	19	3	8	16	15	5
0	15	16	5	11
19	16	2	12	5	0	15	17	8
0
18	13	0	6	14	17	15
0	7	15
1	8	15	16	5	9	12
15	2	3	8	16	1	12
18	8	17	14	10	15	19	9	3
19
5	11	1	12	13	9	7	2	3	8	16	0
18	4	3	8	16	9
4	9	10
7	14	6	16	3	8	0
10	8	11	5	1	3	16	9	15
19	6	2	15	7	16	13	8	10
5	1	7
9	14	11	17	18	5	4	12
8	4	1	3
4
7	17
11	3	8	16	1
1	5	10	15
2	12
15	13
19	2	8	14	7	5	18	4	10
14	4	3	8	16	5	18	1	10	13
14	10	6	7
5	16	10	9	18	3
17	9	10	4	8	14
12
15	14	1	16
4	15	2	19	1	12	3
16	5	18	17	8	19	11	15
1
12	16	0	15
4	14	19	10	16	1	11	9
14
11	9	7
19
13	3	8	16	1
5	16	19	15
8	18	3	16	19	15	1	13	6
18	8	1
18	11	3	8	16	14	9	2	7	1
6	11	17	13	0	16	10	2
6	10	17	2	0	9
14	3	8	16	2	15
0	18	8	11	5	7	9
3	8	16	7
17	19	3
3	8	16	11	10	18	7
5	11	2	19	15	16	4
3	8	16
10	19	12	11	3	8	16	13
2	9	0	14	18	5
13	10	3	8	16	2	11	18
18	7
18	19	2
10	2	8	15
8	1	2	14	19	18
17	1	7
5	0	13	4	10	1	2	3	8	16	9
9	12	14	10	4
9	18	5	3	8	16	12
10	11	7	9
18	3	8	16	12	19	13	2	14
2
11
11	0	17
16	18	0	15	8	19	17
2	0	10	13
6	8
17	12	18	7	9	5	19	1
10	8	11	9
10	12	4
15	8	1	10	17	11	16	19
0	13	17	10
13	2	3	8	16	1
2
17	11	3	8	16	10	0	6
1	19	5	6
5	1
9
3	8	16	10	18	1	15	7
7	19
19	18	0	10	1
5	0	8	19	2	18	15	1	14
13	16	1	6	18	10	15	17
0	12
13	15	5	6	1	14	19	8	12
13	17	3	8	16	10
14	8
18	9	8	19	7	11	15	16
3	8	16	11	14	1	5	7	13	4
13	8	3	16	4	12
8	9	10	11	14	7	3	16	4
14	15	6	18	9	7	0	4	3	8	16	12
10
15	1	6	11	9	7	3
10	6	15	1	8	2
2	4	5	12	8	6	9	18
5	0	18	1
0	7	13	14	11	15
14	1	17	10	16	11	0
5	2	18	13	12	17
5	2	17	12	19	7	6	3	8	16	11
19	18	9	5	14	12
2	12	13	0	18	17
8	3	16	17
14	1	18	2	9	16
19	18	1	6	3	8	16	17	15
1	0	2	8	15
16	17	7	13	4
19	1	18	3	8	16
19	17	1	11	4	3	8	16	15
9	1	15
16	17	19	0	12	13
9	8
18	4	14	13	5	10	2	9
9	18	3	8	16	5
4
5	12	7	17
4	10	14	11	1
14	10	2	18	6	1
17	16	14	9	8
13	8	6	2	18	0	19	10
19	16	8	12	18
7	19	14	0	8
18	2
1	4	6
9	13	8	1	6	4	5
2	0	1
3
7	13	3	8	16	11	14	15	1
11	19	18
4
7	4	11	1	9	18	10	13
15	0	13
2	16	3
6	11	15	8
1	9	3
7	12	11	13	10	19	14	5	0	3
9	7	18
11
14	7
3	8	16	9	6
16	12	10	19	6	2	3	8	0
5	11	19	6
9	2	17	5	16	8	12	14
13	0	19	11	18	7	16
14	0	13	7	9	16	2	3	8	10
3	8	16	14	6	17	0	11
4	14	6
4	15	0	12
11
19	3	8	16	17	9	1
12	14	4	1	3	8	16	6
8	17	10	3	16	4	14	6
1	18	11	12	3	8	16	10
9	11	0	19	17	14	15	1	16
8	13	9	1	3	16	7
2	10	17	1	7	6
11	17	5	4	18	7	15	12
17	5
11	0	10	15
10
18	6	4	9	11	8	10	19
7	9	19	16	0	13	18	10	6	14
0	14	13
9	11	8	19	1	6	13
10	9	1	0	8	2
6	18	19
7	18	9	3	8	16	0	15
13	9	17	14	15	18	3
6	11	0	14
14	12	17	11	15	10	13	16
9
9	6	4	0	2	13	12	14	7
14	5	13	11	4	3	8	16	15
1	6	9
8	4	11	14	15	7	13	0	2
17	0	2	18	16	14	15	10
15	17
2	7	9	11
14	0
13	1	5	8
0	15	11	10
15	11	0
0	6	14	8	19
16	12	2	11	7	4
8	16	10	2	1	13	19	12
11	15	4	10	6
18	1	3	8	16	0	15
19	3	8	16	9	14	13	6	17
2	15	12	3	8	16	13	17
8	11	13	5	1	2	10	16	3
15	13	5	4	18	0	8	14	1	12
10	12	2	1	6	15	0
7	17
8	13	15	11
2	11	19	14
13	10	1
18	6	11	3	8	16
19	4	13	15	14	2	7	5
6	9	0	17	10	19	18
17	3	8	16	2	0	11
3	8	16	15	4	6
1	15	18	5	13	3	8	16	12
17	16	19	6	14	3	8	2
0	15
7	10	13	14	16	12	1	6	5
4	9	15	3
13	7	0	19	1
14	0	7	1	12	13
17	3	8	16	13	19	11	5
18	8	10	12	4	14	3	16	13
7	6	1	4	18	11	5
16	8	7	11	19	6	17	13	1	12
19	4	17	1	8	2	16	0
18	5	19	4	14
19	9	14	15	3
11	17	14
11	19	10	17
18	4	12	6
8	17	4	7	13	2	11	9	14	3
11	13	12	18	10	19
13
9	14	13	18	5
18	11	12	3
9	8	5	11	0	6	1	18	17
2	18	3	8	16	6	9	5
3	8	16	18
17
11	6	10	13	0	4	3
5	18
5	14	7	4	16	17	15	2	6	8
19	11	9	18	10	15	12	16	2
12	16	17	13	10	5	11	1	15	8
5	18
19	4	16	6	2	18	8
6	8
8	19	7	9	0	5	2	6
17	11	7	5	6	4	14	9	16	1
5	16	0	17	15	10
9	5	6	8	15	3	16	17
7
2	13	0	14	9	8
8	10	0	19	17	7
4	17	5	19	12
12	2	3	8	16	11
17	13	0	4	3	8	16	10	1	12
4	19	1	9	3	8	16	12
7
10	0	15
15	17	14	13"""

def generate(fileName, maxLine, maxItemNum):
	start = timer()
	f = open(fileName, 'w')
	if maxLine == -1 and maxItemNum == -1:
		f.write(originalInput)
		end = timer()
		f.close()
		return end - start
	txnPool = list(range(-int(maxItemNum/4), int(maxItemNum/4)*3))
	print("txnPool : %d" % len(txnPool))
	for i in range(1, maxLine + 1):
		txnSize = random.randint(1, maxItemNum/2)
		random.shuffle(txnPool)
		txn = txnPool[:txnSize]
		toWrite = ""
		for item in txn[:-1]:
			toWrite += str(item) + "\t"
		toWrite += str(txn[-1]) + "\n"
		f.write(toWrite)
	end = timer()
	return end - start
if __name__ == '__main__':
	print("Test Generator will create 'testN.txt'")
	selected = []
	if len(sys.argv) > 1 and (sys.argv[1] == "--all" or sys.argv[1] == "-A"):
		selected = [1,2,3,4]
	else:
		inp = 0
		while inp != -1:
			print("\nChoose Type of Test Case to generate (-1 to exit)\n")
			print("1. Original Input File")
			print("2. Small Test  (maxLine: 1000   Item Number: -5  ~ 15)")
			print("3. Medium Test (maxLine: 10000  Item Number: -8  ~ 32)")
			print("4. Large Test  (maxLine: 100000 Item Number: -8  ~ 32)")
			inp = int(input("Input: "))
			if 0 <= inp and inp <= 4:
				selected.append(inp)
			elif inp != -1:
				print("Please provide valid input range(1 ~ 4)")
		selected = sorted(set(selected))

	for i in selected:
		outFile = "test" + str(i) + ".txt"
		print("Generating original input file as '%s'" % outFile)
		if i == 1:
			print("Generation took %.2f secs" % generate(outFile, -1, -1))
		elif i == 2:
			print("Generation took %.2f secs" % generate(outFile, 1000, 20))
		elif i == 3:
			print("Generation took %.2f secs" % generate(outFile, 10000, 40))
		elif i == 4:
			print("Generation took %.2f secs" % generate(outFile, 100000, 40))
	print("Terminating Test Generator")
