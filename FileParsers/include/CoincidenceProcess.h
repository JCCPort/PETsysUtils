
#ifndef PETSYSPARSERS_COINCIDENCEPROCESS_H
#define PETSYSPARSERS_COINCIDENCEPROCESS_H

#include <iostream>
#include <vector>
#include <string>
#include "kwaymergesort.h"
#include "DataStructures.h"

enum FileType{
	Binary = 0,
	Ascii = 1,
	rEWt = 2
};


std::vector<SinglesWGroup> parseEvents(const std::string &inputPath, long long windowSize, int numHitsCoincidence);
int writeEvents(const std::vector<SinglesWGroup>& events, FileType type, const std::string& name);


struct single_{
	long long time;
	float energy;
	int channel;
};

struct single {
	single_ s;

	bool operator < (const single &b) const;


	// overload the << operator for writing a single struct
	friend std::ostream& operator<<(std::ostream &os, const single &b)
	{
		os.write((char*)(&b.s), sizeof(single_));
		return os;
	}
	// overload the >> operator for reading into a single struct
	friend std::istream& operator>>(std::istream &is, single &b)
	{
		is.read((char *) (&b), sizeof(b));
		return is;
	}
};

bool bySize(single const &a, single const &b);

#endif //PETSYSPARSERS_COINCIDENCEPROCESS_H
