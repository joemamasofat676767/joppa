#include <iostream>
#include <fstream>

int ReadKnowledge(lua_state* L){
	std::ifstream configs_file("config.txt");
	// 0 knowledge file
	std::string configs[1];
	int configs_i = 0;
	std::string line;
	while(std::getline(configs_file, line)){
		if(line.at(0) == '#'){
			continue;
		}
		configs[configs_i] = line;
		configs_i++;
	}
	configs_file.close();
	std::ifstream knowledge_file(configs[0]);


	return 1;
}
