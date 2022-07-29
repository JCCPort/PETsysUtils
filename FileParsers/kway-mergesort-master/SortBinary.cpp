#include <iostream>
#include <vector>
#include <string>
#include "kwaymergesort.h"
#include "SortBinary.h"

//bool bySize(single const &a, single const &b) {
//	if      (a.s.time < b.s.time)  return true;
//	else if (a.s.time > b.s.time)  return false;
//	else {return false;}
//}

//int main(int argc, char* argv[]) {
//
//	std::string inFile       = argv[1];
//    int  bufferSize     = 100000000;      // allow the sorter to use 100Kb (base 10) of memory for sorting.
//                                       // once full, it will dump to a temp file and grab another chunk.
//    bool compressOutput = false;       // not yet supported
//	std::string tempPath     = "./";        // allows you to write the intermediate files anywhere you want.
//
//	std::string outputName = inFile.substr(0, inFile.find_last_of('.')) + "_sorted" + inFile.substr(inFile.find_last_of('.'), inFile.size());
//
//	std::ofstream outFile(outputName);
//
//    // sort a single file by chrom then start
//    auto *bed_sorter_custom = new KwayMergeSort<single> (inFile,
//                                                                          &outFile,
//                                                                          bySize,
//                                                                          bufferSize,
//                                                                          compressOutput,
//                                                                          tempPath);
//	bed_sorter_custom->SetComparison(bySize);
//    bed_sorter_custom->Sort();
//	outFile.close();
//
//	std::cout << "Sorted file. Output at:\t" << outputName << std::endl;
//}