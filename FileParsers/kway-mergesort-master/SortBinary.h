
#ifndef PETSYSPARSERS_SORTBINARY_H
#define PETSYSPARSERS_SORTBINARY_H

#include "kwaymergesort.h"

struct single_{
	long long time;
	float energy;
	int channel;
};

struct single {
	single_ s;

	bool operator < (const single &b) const
	{
		if (s.time < b.s.time){
			return true;
		}
		else if (s.time > b.s.time) {
			return false ;
		}
		else{
			return false;
		}
	}

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

bool bySize(single const &a, single const &b) {
	if      (a.s.time < b.s.time)  return true;
	else if (a.s.time > b.s.time)  return false;
	else {return false;}
}

#endif //PETSYSPARSERS_SORTBINARY_H
