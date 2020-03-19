// sensorFusion.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include<fstream>
#include<string>
#include<vector>
#include<map>
#include<iostream>

using namespace std;

map<int, vector<double>> readCSV(ifstream& fin) {
	// Check if it is not opened successfully
	if (!fin) {
		cout << "Error, could not open the file";
	}

	map<int, vector<double>> accelerationValues;
	string line;
	size_t pos;
	int rowCounter = 0;
	while (!fin.eof()) {
		vector<double> valuesVector;
		getline(fin, line);
		line += ",";
		while ((pos = line.find(",")) != string::npos) {
			string token = line.substr(0, pos);
			valuesVector.push_back(stod(token));
			line.erase(0, pos + 1);
		}
		accelerationValues.insert(pair<int, vector<double>>(rowCounter, valuesVector));
		rowCounter++;
	}
	return accelerationValues;
}

int main()
{
	// Open the inertial sensor measurement file
	ifstream fin;
	fin.open("data.txt");
	map<int, vector<double>> accelerationData = readCSV(fin);
    return 0;
}

