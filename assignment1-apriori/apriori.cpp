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
void apriori();
void association();
int calcSupport(const set<int>& txn1, const set<int>& txn2);
string setToString(const set<int>& tmpSet);
void printItemset();

int main(int argc, char *argv[])
{
	parseArgv(argc, argv);
	parseTransaction();
	apriori();
	association();
	int cnt = 0;
	for (auto& it : transaction) {
		if(it.find(0) != it.end() && it.find(1) != it.end()) {
			cout << setToString(it) << "\n";
			cnt++;
		}
	}

	return 0;
}

void parseArgv(int argc, char *argv[])
{
	if (argc < 4) {
		minSupport = 5;
		inpFile.open("input.txt");
		outFile.open("output.txt");
		return;

		cout << "3 arguments are required to proceed" << endl;
		cout << argv[0] << " [Minimum Support] [Input File Name] [Output File Name]" << endl;
		exit(EXIT_FAILURE);
	}

	minSupport = strtod(argv[1], NULL);
	inpFile.open(argv[2]);
	outFile.open(argv[3]);

	/* error on argv*/
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

void apriori()
{
	int txnNum = 0;
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
	while (itr != itemset.end()) {
		if ((itr->second.size()/totalTxn)*100 < minSupport)
			itr = itemset.erase(itr);
		else
			itr++;
	}

	int setSize = 1;
	while(true) {
		bool inserted = false;
		set<set<int> > checked;
		for (auto it = itemset.begin(); next(it) != itemset.end(); it++) {
			if (it->first.size() != setSize)
				continue;
			for (auto nextItr = next(it); nextItr != itemset.end(); nextItr++) {
				if (nextItr->first.size() != setSize)
					continue;
				set<int> newItemset;
				set_union(it->first.begin(), it->first.end(),
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

void association()
{
	outFile.setf(ios_base:: fixed, ios_base:: floatfield);
	for (auto it = itemset.begin(); it != itemset.end(); it++) {
		for (auto comp = itemset.begin(); comp != itemset.end(); comp++) {
			if (it == comp)
				continue;
			double support;
			double confidence;
			support = calcSupport(it->second, comp->second);
			confidence = static_cast<double>(support)/it->second.size() * 100;
			support = support/totalTxn * 100;
			// if (support < minSupport)
			// 	continue;
			outFile << setprecision(2)
							<< setToString(it->first) << "\t" << setToString(comp->first)<< "\t"
							<< support << "\t" << confidence << "\n";
		}
	}
}

int calcSupport(const set<int>& txn1, const set<int>& txn2)
{
	auto first1 = txn1.begin(), first2 = txn2.begin();
	auto last1 = txn1.end(), last2 = txn2.end();
	int size = 0;
	while (true)
		{
			if (first1 == last1 || first2 == last2)
				break;

			if (*first1 < *first2) ++first1;
			else if (*first2 < *first1)  ++first2;
			else { ++size; ++first1; ++first2; }
		}

	return size;
}

string setToString(const set<int>& tmpSet)
{
	string ret = "{";
	for (auto& it : tmpSet)
		ret += to_string(it) + ",";
	ret = ret.substr(0, ret.size()-1);
	ret += "}";
	return ret;
}

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
