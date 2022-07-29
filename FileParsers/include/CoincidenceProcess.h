
#ifndef PETSYSPARSERS_COINCIDENCEPROCESS_H
#define PETSYSPARSERS_COINCIDENCEPROCESS_H

#include <iostream>
#include <vector>
#include <string>
#include "kwaymergesort.h"
#include "DataStructures.h"



std::vector<SinglesWGroup> parseEvents(const std::string &inputPath, long long windowSize, int numHitsCoincidence, const std::vector<int>& includedChannels);
int writeEvents(const std::vector<SinglesWGroup>& events, FileType type, const std::string& name);



#endif //PETSYSPARSERS_COINCIDENCEPROCESS_H
