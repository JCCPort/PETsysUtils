
#include "include/CoincidenceProcess.h"

std::vector<SinglesWGroup> parseEvents(const std::string &inputPath, long long windowSize, int numHitsCoincidence, const std::vector<int>& includedChannels) {
	// TODO(josh): Group by channels or by hits
	std::ifstream dataFile(inputPath);
	if (!dataFile.is_open()) {
		std::cout << "Unable to open file";
	}

	std::vector<SinglesWGroup> events;
	Singles single_{};

	long long prevTime = 0;
	long evNum = 0;
	std::vector<Singles> hitsInWindow;

	SinglesWGroup event_{};
	while (dataFile.read((char *) (&single_), sizeof(single_))) {
		if (!(std::find(includedChannels.begin(), includedChannels.end(), single_.channel) != includedChannels.end())){
			continue;
		}
		if(!hitsInWindow.empty()){
			if ((single_.time - hitsInWindow[0].time) <= windowSize){ // Check if the distance between the first and the possible entry is greater than the window size
				hitsInWindow.push_back(single_); // Keep updating with the most recent hit
			} else {
				if (hitsInWindow.size() >= numHitsCoincidence){
					for(auto & k : hitsInWindow) {
						event_.time = k.time;
						event_.energy = k.energy;
						event_.channel = k.channel;
						event_.group = evNum;
						events.push_back(event_);
					}

					// Empty these vectors now that a group is going to be written
					hitsInWindow.clear();

					evNum++;
				} else {
					hitsInWindow.erase(hitsInWindow.begin());
					hitsInWindow.push_back(single_);
				}
			}
		} else {
			hitsInWindow.push_back(single_);
		}

		if ((prevTime > single_.time)) {
			std::cout << prevTime << "\t" << single_.time << std::endl;
			std::cout << "OH GOD NO THE TIMES AREN'T SORTED\n" << std::endl;
		}
		prevTime = single_.time;
	}
	dataFile.close();

	return events;
}

int writeEvents(const std::vector<SinglesWGroup>& events, FileType type, const std::string& name){
	std::ofstream outFile (name);
	switch (type) {

		case Binary:
			for (const auto & event : events) {
				outFile.write(reinterpret_cast<const char *>(&event), sizeof(SinglesWGroup));
			}
			outFile.close();
			break;
		case Ascii:
			break;
		case rEWt:
			break;
	}

	return 0;
}


std::vector<int> readChannels(const std::string& path){
	std::ifstream inFile (path);
	std::vector<int> allowedChannels;
	std::string line;

	while (inFile) {
		inFile >> line;
		allowedChannels.emplace_back(std::stoi(line));
	}
	return allowedChannels;
}

int main(int argc, char* argv[]) {

	std::string fileName = argv[1];
	long long windowSize = (long long)(std::stoi(argv[2]));
	int majority = std::stoi(argv[3]);
	std::string allowedChannelPath = argv[4];
	bool sort = bool(std::stoi(argv[5]));

	int  bufferSize     = 100000000;
	bool compressOutput = false;
	std::string tempPath     = "./";

	std::vector<int> channels = readChannels(allowedChannelPath);

	std::string outputName = fileName.substr(0, fileName.find_last_of('.')) + "_grouped" + fileName.substr(fileName.find_last_of('.'), fileName.size());
	std::vector<SinglesWGroup> events;
	if(sort){
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
		events = parseEvents(outputName, windowSize, majority, channels);
	} else{
		events = parseEvents(fileName, windowSize, majority, channels);
	}

	writeEvents(events, Binary, outputName);

	std::cout << "Found coincidences. Output at:\t" << outputName << std::endl;
}
