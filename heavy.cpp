#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <array>

std::vector<std::vector<uint16_t>>* ReadKnowledge(){
	std::ifstream configs_file("config.txt");
	// 0 knowledge file, 1 knowledge buckets
	int configs_i = 0;
	// bucket size & how many
	std::vector<int> knowledge_buckets;
	std::ifstream knowledge_file;
	std::string line;
	while(std::getline(configs_file, line)){
		std::cout << "line: " << line << "\n";
		if(line.at(0) == '#' || line.empty()){
			continue;
		}
		switch(configs_i){
			case 0:
				knowledge_file.open(line, std::ios::binary);
				break;
			case 1:
				std::stringstream line_stream(line);
				uint16_t temp;
				while(line_stream >> temp){
				std::cout << "temp: " << temp << " ";
					knowledge_buckets.push_back(temp);
				}
				std::cout << "\n";
				break;
		}
		configs_i++;
	}
	configs_file.close();

	if(knowledge_buckets.size() < 2){
		return nullptr;
	}
	int knowledge_buckets_i = 0;
	std::vector<std::vector<uint16_t>> knowledge_keys;
	std::vector<std::vector<uint16_t>> knowledge_values;
	std::vector<uint16_t> knowledge_buf;
	for(int i = 0; i < knowledge_buckets[knowledge_buckets_i+1]; i++){
		if(std::getline(knowledge_file, line)){
			int read_i = 0;
			std::cout << "line: " << line << "\n";
			std::stringstream line_stream(line);
			uint16_t temp;
			while(read_i < knowledge_buckets[knowledge_buckets_i] && line_stream >> temp){
				std::cout << "key buf: " << temp << "\n";
				knowledge_buf.push_back(temp);
				read_i++;
			}
			knowledge_keys.push_back(knowledge_buf);
			knowledge_buf.clear();
			while(line_stream >> temp){
				std::cout << "value buf: " << temp << "\n";
				knowledge_buf.push_back(temp);
			}
			knowledge_values.push_back(knowledge_buf);
			knowledge_buf.clear();
		}
		else{
			std::cout << "break";
			break;
		}
	}
	knowledge_buckets_i += 2;

	knowledge_file.close();

	std::vector<std::vector<uint16_t>>* knowledge = new std::vector<std::vector<uint16_t>>[2]{knowledge_keys, knowledge_values};

	return knowledge;
}

int main(){
	auto* knowledge = ReadKnowledge();
	std::cout << "knowledge:\n";
	for(const auto& item1 : knowledge[0]){
		for(const auto& item2 : item1){
			std::cout << item2 << " ";
		}
		std::cout << ", ";
	}
	std::cout << "\b\b \n";
	for(const auto& item1 : knowledge[1]){
		for(const auto& item2 : item1){
			std::cout << item2 << " ";
		}
		std::cout << ", ";
	}
	std::cout << "\b\b";

	delete[] knowledge;

	return 0;
}
