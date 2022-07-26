#ifndef PETSYSPARSERS_READBINARY_H
#define PETSYSPARSERS_READBINARY_H

#include <vector>
#include <string>
#include "DataStructures.h"

std::vector<Event> parseEvents(const std::string& path, long long windowSize, int numHitsCoincidence);
#endif //PETSYSPARSERS_READBINARY_H
