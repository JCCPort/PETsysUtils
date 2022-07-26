#include "../include/ReadBinary.h"

#include <string>
#include <fstream>
#include <iostream>
#include "../include/DataStructures.h"

std::vector<Event> parseEvents(const std::string& path, long long windowSize, int numHitsCoincidence){
	// TODO(josh): Group by channels or by hits
	std::string line;
	std::ifstream dataFile(path);

	std::vector<Event> events;
	Singles single_{};
	if (dataFile.is_open())
	{
		long long prevTime = 0;
		unsigned int evNum = 0;
		std::vector<long long> timesInWindow;
		std::vector<Singles> hitsInWindow;

		Event event_;
		while (dataFile.read((char *) (&single_), sizeof(single_)))
		{
			timesInWindow.push_back(single_.time); // Keep updating with the newest time
			hitsInWindow.push_back(single_);

			if((single_.time - timesInWindow[0]) > windowSize){  // Check if the distance between the first and the latest entry is greater than the window size
				timesInWindow.erase(timesInWindow.begin());
				hitsInWindow.erase(hitsInWindow.begin());
			}

			if(timesInWindow.size() >= numHitsCoincidence){
				if((single_.time - timesInWindow[0]) > windowSize){  // Keep looking to add hits until you get to the window length
					event_.eventNumber = evNum;
					event_.hits = hitsInWindow;

					// Empty these vectors now that a group is going to be written
					timesInWindow.clear();
					hitsInWindow.clear();

					events.push_back(event_);

					evNum++;
				}
			}


			if((prevTime > single_.time)){
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

int main(){
	parseEvents("/home/josh/PETsysUtils/run5_LED_qdc_single.ldatsorted", 100000, 2);
}