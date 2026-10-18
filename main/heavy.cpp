#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <array>

std::array<std::vector<std::vector<int>>, 2>* ReadKnowledge(){
	std::ifstream configs_file("config.txt");
	// 0 knowledge file, 1 knowledge buckets
	int configs_i = 0;
	std::vector<int> knowledge_buckets;
	std::string line;
	while(std::getline(configs_file, line)){
		if(line.at(0) == '#' || line.empty()){
			continue;
		}
		switch(configs_i){
			case 0:
				std::ifstream knowledge_file(line, std::ios::binary);
				break;
			case 1:
				std::stringstream line_stream(line);
				uint16_t temp;
				while(line_stream >> temp){
					knowledge_buckets.push_back(temp);
				}
				break;
		}
		configs_i++;
	}
	configs_file.close();

	// 0 bucket size, 1 how many
	int knowledge_buckets_buf[2];
	if(knowledge_buckets.size() < 2){
		return nullptr;
	}
	for(int i = 0; i < knowledge_buckets_buf[1]; i++){
		if(std::getline(knowledge_file, line)){
			
		}
		else{
			break;
		}
	}

	return 1;
}
