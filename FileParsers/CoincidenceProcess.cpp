#include "kway-mergesort-master/SortBinary.h"
#include "kway-mergesort-master/kwaymergesort.h"
#include "include/ReadBinary.h"

int main(int argc, char* argv[]) {

	std::string fileName = argv[1];
	long long windowSize = (long long)(std::stoi(argv[2]));
	int majority = std::stoi(argv[3]);

	int  bufferSize     = 100000000;
	bool compressOutput = false;
	std::string tempPath     = "./";


	std::string outputName = fileName.substr(0, fileName.find_last_of('.')) + "_grouped" + fileName.substr(fileName.find_last_of('.'), fileName.size());
	std::ofstream outFile(outputName);

	// sort a single file by chrom then start
	auto *bed_sorter_custom = new KwayMergeSort<single> (fileName,
	                                                     &outFile,
	                                                     bySize,
	                                                     bufferSize,
	                                                     compressOutput,
	                                                     tempPath);
	bed_sorter_custom->SetComparison(bySize);
	bed_sorter_custom->Sort();
	outFile.close();

	auto events = parseEvents(outputName, windowSize, majority);
	writeEvents(events, Binary, outputName);

	std::cout << "Found coincidences. Output at:\t" << outputName << std::endl;
}