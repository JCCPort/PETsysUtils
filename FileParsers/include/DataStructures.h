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
	long group;
};

struct Event{
	unsigned int eventNumber;
	std::vector<Singles> hits;
};


struct single_{
	long long time;
	float energy;
	int channel;
};

struct single {
	single_ s;

	inline bool operator < (const single &b) const{
		return s.time < b.s.time;
	};

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


inline bool bySize(single const &a, single const &b) {
	return a.s.time < b.s.time;
//	if      (a.s.time < b.s.time)  return true;
//	else if (a.s.time > b.s.time)  return false;
//	else {return false;}
}

enum FileType{
	Binary = 0,
	Ascii = 1,
	rEWt = 2
};

#endif //PETSYSPARSERS_DATASTRUCTURES_H
