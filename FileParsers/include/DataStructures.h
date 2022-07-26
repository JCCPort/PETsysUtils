#ifndef PETSYSPARSERS_DATASTRUCTURES_H
#define PETSYSPARSERS_DATASTRUCTURES_H

#include <vector>

struct Singles{
	long long time;
	float energy;
	int channel;
};

struct SinglesWGroup{
	long long time;
	float energy;
	int channel;
	int group;
};

struct Event{
	unsigned int eventNumber;
	std::vector<Singles> hits;
};

#endif //PETSYSPARSERS_DATASTRUCTURES_H
