#include <cstdlib>
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cmath>
using namespace std;

// local includes
#include "kwaymergesort.h"

// a basic struct for a single entry.

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
//		else{
//			return false;
//		}

    }
    
    // overload the << operator for writing a single struct
    friend ostream& operator<<(ostream &os, const single &b)
    {
	    os.write((char*)(&b.s), sizeof(single_));
        return os;
    }
    // overload the >> operator for reading into a single struct
    friend istream& operator>>(istream &is, single &b)
    {
		is.read((char *) (&b), sizeof(b));
        return is;
    }    
};


// comparison function for sorting by chromosome, then by start.
bool bySize(single const &a, single const &b) {
	if      (a.s.time < b.s.time)  return true;
	else if (a.s.time > b.s.time)  return false;
//	else {return false;}
}


int main(int argc, char* argv[]) {

    string inFile       = argv[1];
    int  bufferSize     = 100000000;      // allow the sorter to use 100Kb (base 10) of memory for sorting.
                                       // once full, it will dump to a temp file and grab another chunk.     
    bool compressOutput = false;       // not yet supported
    string tempPath     = "./";        // allows you to write the intermediate files anywhere you want.

	std::string outputName = inFile.substr(0, inFile.find('.')) + "_sorted" + inFile.substr(inFile.find('.'), inFile.size());

	ofstream myfile (outputName);

    // sort a single file by chrom then start
    auto *bed_sorter_custom = new KwayMergeSort<single> (inFile,
                                                                          &myfile,
                                                                          bySize,
                                                                          bufferSize,
                                                                          compressOutput,
                                                                          tempPath);
	bed_sorter_custom->SetComparison(bySize);
    bed_sorter_custom->Sort();
	myfile.close();
}