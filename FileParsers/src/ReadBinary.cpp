#include "../include/ReadBinary.h"

#include <string>
#include <fstream>
#include <iostream>
#include "../include/DataStructures.h"

std::vector<SinglesWGroup> parseEvents(const std::string &path, long long windowSize, int numHitsCoincidence) {
	// TODO(josh): Group by channels or by hits
	std::string line;
	std::ifstream dataFile(path);

	std::vector<SinglesWGroup> events;
	Singles single_{};
	if (dataFile.is_open()) {
		long long prevTime = 0;
		int evNum = 0;
		std::vector<long long> timesInWindow;
		std::vector<Singles> hitsInWindow;

		SinglesWGroup event_{};
		while (dataFile.read((char *) (&single_), sizeof(single_))) {
			timesInWindow.push_back(single_.time); // Keep updating with the newest time
			hitsInWindow.push_back(single_);

			if ((single_.time - timesInWindow[0]) >
			    windowSize) {  // Check if the distance between the first and the latest entry is greater than the window size
				timesInWindow.erase(timesInWindow.begin());
				hitsInWindow.erase(hitsInWindow.begin());
			}

			if (timesInWindow.size() >= numHitsCoincidence) {
				if ((single_.time - timesInWindow[0]) > windowSize) {  // Keep looking to add hits until you get to the window length
					for(auto & k : hitsInWindow) {
						event_.time = k.time;
						event_.energy = k.energy;
						event_.channel = k.channel;
						event_.group = evNum;
						events.push_back(event_);
					}

					// Empty these vectors now that a group is going to be written
					timesInWindow.clear();
					hitsInWindow.clear();

					evNum++;
				}
			}


			if ((prevTime > single_.time)) {
				std::cout << prevTime << "\t" << single_.time << std::endl;
				std::cout << "OH GOD NO THE TIMES AREN'T SORTED\n" << std::endl;
			}
			prevTime = single_.time;
		}
		dataFile.close();
	} else {
		std::cout << "Unable to open file";
	}

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

int main(int argc, char* argv[]) {
	std::string fileName = argv[1];
	long long windowSize = (long long)(std::stoi(argv[2]));
	int majority = std::stoi(argv[3]);

	std::string outputName = fileName.substr(0, fileName.find_last_of('.')) + "_grouped" + fileName.substr(fileName.find_last_of('.'), fileName.size());
	auto events = parseEvents(fileName, windowSize, majority);
	writeEvents(events, Binary, outputName);
}