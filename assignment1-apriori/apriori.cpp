#include <algorithm>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iterator>
#include <iostream>
#include <iomanip>
#include <map>
#include <string>
#include <sstream>
#include <set>
#include <utility>
#include <vector>
using namespace std;

double minSupport;
double totalTxn;
ifstream inpFile;
ofstream outFile;
vector<set<int> > transaction;
vector<set<set<int> > > itemset;

void parseArgv(int argc, char *argv[]);
void parseTransaction();
void apriori();
void generateCandidate(set<set<int> >& candidate, int poolSize);
void pruning(set<set<int> >& candidate, int poolSize);
void printToOutputFile();
bool isFrequent(const set<int>& curItemset);
int calcSupport(const set<int>& fp1, const set<int>& fp2);
string setToString(const set<int>& tempSet);
void printItemset();

int main(int argc, char *argv[])
{
	parseArgv(argc, argv);
	parseTransaction();
	apriori();
	printToOutputFile();

	return 0;
}

/*
 * Parse 3 arguments to set minimum support and open input & output txt files.
 */
void parseArgv(int argc, char *argv[])
{
	if (argc < 4) {
		// minSupport = 5;
		// inpFile.open("input.txt");
		// outFile.open("output.txt");
		// return;

		cout << "3 arguments are required to proceed" << endl;
		cout << argv[0] << " [Minimum Support] [Input File Name] [Output File Name]" << endl;
		exit(EXIT_FAILURE);
	}

	minSupport = strtod(argv[1], NULL);
	inpFile.open(argv[2]);
	outFile.open(argv[3]);

	/* error on argv */
	if (minSupport == 0 || !inpFile.is_open() || !outFile.is_open()) {
		if (minSupport == 0)
			cout << "Failed to parse 'Support Value' or it is set to 0.0" << endl;
		if (!inpFile.is_open())
			cout << "Failed to open input file [" << argv[2] << "]" << endl;
		if (!outFile.is_open())
			cout << "Failed to open output file [" << argv[3] << "]" << endl;
		exit(EXIT_FAILURE);
	}
}

/*
 * get all items from input file and save it to 'vector<set<int> > transaction'
 * transaction[N][M] = (N+1)th transaction's (M+1)th item.
 */
void parseTransaction()
{
	string line;
	while (getline(inpFile, line)) {
		stringstream linestream(line);
		set<int> newTransaction;
		string tmp;
		while (getline(linestream, tmp, '\t')) {
			int cur = atoi(tmp.c_str());
			newTransaction.insert(cur);
		}
		transaction.push_back(newTransaction);
	}
	totalTxn = transaction.size();
}

/*
 * get all k-itemsets that has support > minSupport
 * that is, get all frequent patterns using APRIORI algorithm.
 */
void apriori()
{
	// set<set<int> >* curItemset = &itemset[itemsetSize];
	set<set<int> > emptyItemset;
	itemset.push_back(emptyItemset);/* 0-itemset */
	itemset.push_back(emptyItemset);/* 1-itemset */

	for (auto& txn : transaction) {
		for (auto& item : txn) {
			set<int> tempSet;
			tempSet.insert(item);
			itemset[1].insert(tempSet);
		}
	}
	/* remove all 1-itemsets that has support < minSupport */
	for (auto itr = itemset[1].begin(); itr != itemset[1].end(); ) {
		if (isFrequent(*itr))
			itr++;
		else
			itr = itemset[1].erase(itr);
	}

	int itemsetSize = 1;
	while (true) {
		set<set<int> > candidate;
		generateCandidate(candidate, itemsetSize);
		pruning(candidate, itemsetSize);

		for (auto itr = candidate.begin(); itr != candidate.end(); ) {
			if (isFrequent(*itr))
				itr++;
			else
				itr = candidate.erase(itr);
		}
		if (candidate.empty())
			break;
		else
			itemset.push_back(candidate);
		itemsetSize++;
	}
	printItemset();
}

void generateCandidate(set<set<int> >& candidate, int poolSize)
{
	const set<set<int> >& pool = itemset[poolSize];

	for (auto itr = pool.begin(); next(itr) != pool.end(); itr++) {
		for (auto nextItr = next(itr); nextItr != pool.end(); nextItr++) {
			set<int> newItemset;
			set_union(itr->begin(), itr->end(),
						nextItr->begin(), nextItr->end(),
						inserter(newItemset, newItemset.begin()));
			if (newItemset.size() != poolSize + 1)
				continue;
			candidate.insert(newItemset);
		}
	}
}

void pruning(set<set<int> >& candidate, int poolSize)
{
	const set<set<int> >& pool = itemset[poolSize];

	for (auto itr = candidate.begin(); itr != candidate.end(); ) {
		bool isPruned = false;
		for (int i = 0; i < itr->size(); i++) {
			set<int> tempSet(*itr);
			auto rm = tempSet.begin();
			advance(rm, i);
			tempSet.erase(rm);
			if (pool.find(tempSet) == pool.end()) {
				isPruned = true;
				break;
			}
		}
		if (isPruned)
			itr = candidate.erase(itr);
		else
			itr++;
	}
}

void printToOutputFile()
{
	/* vector<set<int> > transaction */
	/* vector<set<set<int> > > itemset */
	outFile.setf(ios_base:: fixed, ios_base:: floatfield);

	/* For the convenience of iteration, all itemsets will be inserted into itemset[0]
	 * Note that previous items will be removed from itemset[n](n >= 1) to save some memory.
	 */
	set<set<int> >& frequentPattern = itemset[0];
	for (auto curPool = itemset.begin() + 1; curPool != itemset.end(); curPool++) {
		frequentPattern.insert(curPool->begin(), curPool->end());
		curPool->clear();
	}
	for (auto itr = frequentPattern.begin(); itr != frequentPattern.end(); itr++) {
		for (auto comp = frequentPattern.begin(); comp != frequentPattern.end(); comp++) {
			if (itr == comp)
				continue;
			if (includes(itr->begin(), itr->end(), comp->begin(), comp->end()))
				continue;
			if (includes(comp->begin(), comp->end(), itr->begin(), itr->end()))
				continue;
			double support = static_cast<double>(calcSupport(*itr, *comp));
			if ((support/totalTxn * 100) < minSupport)
				continue;
			set<int> emptySet;
			double confidence = (static_cast<double>(support)/calcSupport(*itr, emptySet)) * 100;
			support = support/totalTxn * 100;

			outFile << setprecision(2)
							<< setToString(*itr) << "\t" << setToString(*comp)<< "\t"
							<< support << "\t" << confidence << "\n";
		}
	}
}

/*
 * lookup DB to check whether provided itemset is frequent or not.
 */
bool isFrequent(const set<int>& curItemset)
{
	int cnt = 0;
	for (auto& txn : transaction) {
		bool found = true;
		for (auto& item : curItemset) {
			auto itr = txn.find(item);
			if (itr == txn.end()) {
				found = false;
				break;
			}
		}
		if (found)
			cnt++;
	}
	// cout << setToString(curItemset) << " " << (cnt/totalTxn)*100 << endl;
	if ((cnt/totalTxn)*100 >= minSupport)
		return true;
	else
		return false;
}

/*
 * return number of transactions that contain [item_set] ∪ [associative_item_set]
 */
int calcSupport(const set<int>& fp1, const set<int>& fp2)
{
	/* vector<set<int> > transaction */
	/* vector<set<set<int> > > itemset */
	set<int> unionPattern;
	int cnt = 0;
	set_union(fp1.begin(), fp1.end(),
				fp2.begin(), fp2.end(),
				inserter(unionPattern, unionPattern.begin()));
	for (auto& txn : transaction) {
		bool isSubset = true;
		for (auto& item : unionPattern) {
			auto itr = txn.find(item);
			if (itr == txn.end()) {
				isSubset = false;
				break;
			}
		}
		if (isSubset)
			cnt++;
		// if (includes(txn.begin(), txn.end(), unionPattern.begin(), unionPattern.end()))
		// 	cnt++;
	}

	return cnt;
}

/*
 * helper function that transform set to string format.
 * e.g.) {1,2,3,4}
 */
string setToString(const set<int>& tempSet)
{
	string ret = "{";
	for (auto& it : tempSet)
		ret += to_string(it) + ",";
	ret = ret.substr(0, ret.size()-1);
	ret += "}";
	return ret;
}

/*
 * helper function that prints all frequent patterns(itemsets) to the terminal.
 */
void printItemset()
{
	int cnt = 1;
	for (auto& it : itemset) {
		for (auto& set : it) {
			cout.width(4);
			cout << cnt << " ";
			cout << setToString(set) << endl;
			cnt++;
		}
	}
}
