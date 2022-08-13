#include <string>
#include <fstream>
#include "include/kwaymergesort.h"
#include "include/DataStructures.h"


int main(int argc, char* argv[]) {

	std::string fileName = argv[1];
	std::ifstream dataFile(fileName);
	if (!dataFile.is_open()) {
		std::cout << "Unable to open file";
	}
	std::string outputName = fileName.substr(0, fileName.find_last_of('.')) + "_sorted" + fileName.substr(fileName.find_last_of('.'), fileName.size());
	std::ofstream outFile(outputName);
	// sort a single file by chrom then start

	long  bufferSize     = 100000000;
	bool compressOutput = false;
	std::string tempPath     = "./";
	auto *bed_sorter_custom = new KwayMergeSort<single> (fileName,
	                                                     &outFile,
	                                                     bySize,
	                                                     bufferSize,
	                                                     compressOutput,
	                                                     tempPath);
	bed_sorter_custom->SetComparison(bySize);
	bed_sorter_custom->Sort();
	outFile.close();

	std::cout << "Sorted file. Output at:\t" << outputName << std::endl;
}