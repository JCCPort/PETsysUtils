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
    
    // sort a single file by chrom then start
//    KwayMergeSort<single> *bed_sorter = new KwayMergeSort<single> (inFile,
//                                                                   &cout,
//                                                                   bufferSize,
//                                                                   compressOutput,
//                                                                   tempPath);
//
////    cout << "First sort by chrom, then start using the overloaded \"<\" operator\n";
////    bed_sorter->Sort();
//    cout << "Now, sort by size using a custom function (bySize)\n";
//    bed_sorter->SetComparison(bySize);
//    bed_sorter->Sort();

	ofstream myfile (inFile + "sorted");

    // sort a single file by chrom then start
    auto *bed_sorter_custom = new KwayMergeSort<single> (inFile,
                                                                          &myfile,
                                                                          bySize,
                                                                          bufferSize,
                                                                          compressOutput,
                                                                          tempPath);
	bed_sorter_custom->SetComparison(bySize);
    cout << "Now create a new class with bySize() as the custom sort function\n";
    bed_sorter_custom->Sort();
	myfile.close();
}