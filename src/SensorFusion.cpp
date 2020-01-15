// SensorFusion.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main()
{
	ifstream myFile;
	myFile.open("Data.csv");

	while (myFile.good()) {
		string line;
		getline(myFile, line);
		cout << line << endl;
	}
	cout << "Parsing done" << endl;
    return 0;
}

