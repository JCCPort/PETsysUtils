
#include "include/CoincidenceProcess.h"
#include "include/argparse.h"

std::vector<SinglesWGroup> parseEvents(const std::string &inputPath, long long windowSize, int numHitsCoincidence, const std::vector<int>& includedChannels) {
	// TODO(josh): Group by channels or by hits
	std::ifstream dataFile(inputPath);
	if (!dataFile.is_open()) {
		throw std::runtime_error("Unable to open data file");
	}

	std::vector<SinglesWGroup> events;
	Singles single_{};

	long long prevTime = 0;
	long evNum = 0;
	std::vector<Singles> hitsInWindow;
	hitsInWindow.reserve(1000);
	events.reserve(10000000);

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

	std::cout << "Found " << events.size() << " clustered hits" << std::endl;

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
	if (!inFile.is_open()) {
		throw std::runtime_error("Unable to open channel file");
	}
	std::vector<int> allowedChannels;
	std::string line;

	while (inFile) {
		inFile >> line;
		allowedChannels.emplace_back(std::stoi(line));
	}
	return allowedChannels;
}

int main(int argc, char* argv[]) {
	argparse::ArgumentParser program("Event Builder Supreme");
	program.add_description("Multi-threaded implementation of the RecoZoR PE finding algorithm.");
	program.add_argument("-i", "--input")
			.required()
			.help("Path to data file.");
	program.add_argument("-o", "--output")
			.help("Path for output grouped file. Defaults to input file name with '_grouped' appended.");
	program.add_argument("--mapping_dir")
			.required()
			.help("Path to file that lists channels to consider events from.");
	program.add_argument("--majority")
			.required()
			.help("Number of hits in time window required for event building.")
			.scan<'i', int>();
	program.add_argument("--window_size")
			.required()
			.help("Size of time window in ns.")
			.scan<'i', long long>();
	program.add_argument("--sort")
			.default_value(true)
			.help("Set to false if file is already sorted.");
	
	program.parse_args(argc, argv);
	
	std::string fileName            = program.get<std::string>("-i");
	long long windowSize            = program.get<long long>("--window_size") * 1000;
	int majority                    = program.get<int>("--majority");
	std::string allowedChannelPath  = program.get<std::string>("--mapping_dir");
	bool sort                       = program.get<bool>("--sort");
	
	std::string outputFileName;
	if(program.is_used("-o")){
		outputFileName = program.get<std::string>("-o");
	} else {
		outputFileName = fileName.substr(0, fileName.find_last_of('.')) + "_grouped" + fileName.substr(fileName.find_last_of('.'), fileName.size());;
	}

	long bufferSize      = 10000000000;
	bool compressOutput  = false;
	std::string tempPath = "./";

	std::vector<int> channels = readChannels(allowedChannelPath);

	std::vector<SinglesWGroup> events;
	if(sort){
		std::ofstream outFile(outputFileName);

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
		events = parseEvents(outputFileName, windowSize, majority, channels);
		delete bed_sorter_custom;
	} else{
		events = parseEvents(fileName, windowSize, majority, channels);
	}

	writeEvents(events, Binary, outputFileName);

	std::cout << "Found coincidences. Output at:\t" << outputFileName << std::endl;
}