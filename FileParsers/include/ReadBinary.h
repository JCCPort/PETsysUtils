#ifndef PETSYSPARSERS_READBINARY_H
#define PETSYSPARSERS_READBINARY_H

#include <vector>
#include <string>
#include "DataStructures.h"

enum FileType{
	Binary = 0,
	Ascii = 1,
	rEWt = 2
};

std::vector<SinglesWGroup> parseEvents(const std::string& path, long long windowSize, int numHitsCoincidence);
int writeEvents(const std::vector<SinglesWGroup>& events, FileType type, const std::string& name);

#endif //PETSYSPARSERS_READBINARY_H