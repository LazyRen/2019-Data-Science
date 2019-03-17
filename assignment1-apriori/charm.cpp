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
map<set<int>, set<int> > itemset;

void parseArgv(int argc, char *argv[]);
void parseTransaction();
void charm();
void printToOutputFile();
int calcSupport(const set<int>& txn1, const set<int>& txn2);
string setToString(const set<int>& tmpSet);
void printItemset();

int main(int argc, char *argv[])
{
	parseArgv(argc, argv);
	parseTransaction();
	charm();
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
 * that is, get all frequent patterns using CHARM algorithm.
 */
void charm()
{
	int txnNum = 0;

	/* get 1-itemset */
	for (auto& trx : transaction) {
		for (auto& item : trx) {
			set<int> tmpSet;
			tmpSet.insert(item);
			auto it = itemset.find(tmpSet);
			if (it != itemset.end()) {
				it->second.insert(txnNum);
			} else { /* item not yet inserted */
				set<int> txnSet;
				txnSet.insert(txnNum);
				itemset.insert({tmpSet, txnSet});
			}
		}
		txnNum += 1;
	}
	auto itr = itemset.begin();
	while (itr != itemset.end()) {/* remove all 1-itemsets that has support < minSupport */
		if ((itr->second.size()/totalTxn)*100 < minSupport)
			itr = itemset.erase(itr);
		else
			itr++;
	}

	int setSize = 1;/* size of itemset */
	while(true) {
		bool inserted = false;
		set<set<int> > checked;
		for (auto itr = itemset.begin(); next(itr) != itemset.end(); itr++) {
			if (itr->first.size() != setSize)
				continue;
			for (auto nextItr = next(itr); nextItr != itemset.end(); nextItr++) {
				if (nextItr->first.size() != setSize)
					continue;
				set<int> newItemset;
				set_union(itr->first.begin(), itr->first.end(),
							nextItr->first.begin(), nextItr->first.end(),
							inserter(newItemset, newItemset.begin()));
				if (newItemset.size() != setSize + 1)
					continue;
				if (checked.find(newItemset) != checked.end())
					continue;
				checked.insert(newItemset);
				txnNum = 0;
				set<int> newTxnset;
				for (auto& txn : transaction) {
					if (includes(txn.begin(), txn.end(), newItemset.begin(), newItemset.end()))
						newTxnset.insert(txnNum);
					txnNum += 1;
				}
				if ((newTxnset.size()/totalTxn)*100 < minSupport)
					continue;
				itemset.insert({newItemset, newTxnset});
				if (!inserted)
					inserted = true;
			}
		}
		if (!inserted)
			break;
		setSize += 1;
	}
	printItemset();
}

void printToOutputFile()
{
	outFile.setf(ios_base:: fixed, ios_base:: floatfield);
	for (auto itr = itemset.begin(); itr != itemset.end(); itr++) {
		for (auto comp = itemset.begin(); comp != itemset.end(); comp++) {
			if (itr == comp)
				continue;
			double support = static_cast<double>(calcSupport(itr->second, comp->second));
			double confidence = static_cast<double>(support)/itr->second.size() * 100;
			support = support/totalTxn * 100;
			if (support < minSupport)
				continue;
			outFile << setprecision(2)
							<< setToString(itr->first) << "\t" << setToString(comp->first)<< "\t"
							<< support << "\t" << confidence << "\n";
		}
	}
}

/*
 * return number of transactions that contain [item_set] ∪ [associative_item_set]
 * slight modification of c++ STL set_intersection from <algorithm> header.
 */
int calcSupport(const set<int>& txn1, const set<int>& txn2)
{
	auto first1 = txn1.begin(), first2 = txn2.begin();
	auto last1 = txn1.end(), last2 = txn2.end();
	int size = 0;
	while (first1 != last1 && first2 != last2)
	{
		if (*first1 < *first2) {
			++first1;
		} else if (*first2 < *first1) {
			++first2;
		} else {
			++size; ++first1; ++first2;
		}
	}

	return size;
}

/*
 * helper function that transform set to string format.
 * e.g.) {1,2,3,4}
 */
string setToString(const set<int>& tmpSet)
{
	string ret = "{";
	for (auto& it : tmpSet)
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
		cout.width(4);
		cout << cnt << " ";
		cout << setToString(it.first);
		cout << " - " << it.second.size() << endl;
		cnt++;
	}
}
