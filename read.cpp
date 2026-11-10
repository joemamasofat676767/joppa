#include <fstream>
#include <sstream>
#include <vector>
#include <lua.hpp>
#include <iostream>

int ReadKnowledge(lua_State* L){
	std::ifstream configs_file("config.txt");
	// 0 knowledge file, 1 knowledge buckets
	int configs_i = 0;
	// bucket size & how many
	std::vector<int> knowledge_buckets;
	std::ifstream knowledge_file;
	std::string line;
	while(std::getline(configs_file, line)){
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
					knowledge_buckets.push_back(temp);
				}
				break;
		}
		configs_i++;
	}
	configs_file.close();

	if(knowledge_buckets.size() < 2){
		return 0;
	}
	int knowledge_buckets_i = 0;
	std::vector<std::vector<uint16_t>> knowledge_keys;
	std::vector<std::vector<uint16_t>> knowledge_values;
	std::vector<uint16_t> knowledge_buf;
	while(knowledge_buckets_i < knowledge_buckets.size()){
		for(int i = 0; i < knowledge_buckets[knowledge_buckets_i+1]; i++){
			int read_i = 0;
			std::stringstream line_stream(line);
			uint16_t temp;
			while(read_i < knowledge_buckets[knowledge_buckets_i] && knowledge_file.read((char*)(&temp), 2)){
				knowledge_buf.push_back(temp);
				read_i++;
			}
			knowledge_keys.push_back(knowledge_buf);
			knowledge_buf.clear();
			while(knowledge_file.read((char*)(&temp), 2)){
			if(temp == 0){ break; }
				knowledge_buf.push_back(temp);
			}
			knowledge_values.push_back(knowledge_buf);
			knowledge_buf.clear();
		}
		knowledge_buckets_i += 2;
	}
	knowledge_file.close();

	std::vector<std::vector<uint16_t>>* knowledge = new std::vector<std::vector<uint16_t>>[2]{knowledge_keys, knowledge_values};
	std::vector<std::vector<uint16_t>>** data = (std::vector<std::vector<uint16_t>>**)lua_newuserdata(L, sizeof(std::vector<std::vector<uint16_t>>*));
	*data = knowledge;

	luaL_getmetatable(L, "knowledge");
	lua_setmetatable(L, -2);

	return 1;
}

int CleanKnowledge(lua_State* L){
	std::vector<std::vector<uint16_t>>** data = (std::vector<std::vector<uint16_t>>**)lua_touserdata(L, 1);
	delete[] *data;
	*data = nullptr;

	return 0;
}

int OutKnowledge(lua_State* L){
	std::vector<std::vector<uint16_t>>** data = (std::vector<std::vector<uint16_t>>**)lua_touserdata(L, 1);
	std::cout << "keys: ";
	for(const auto& item : **data){
		std::cout << "{";
		for(const auto& item2 : item){
			std::cout << item2 << ", ";
		}
		std::cout << "\b\b}, ";
	}
	std::cout << "\nvalues: ";
	for(const auto& item : *(*data+1)){
		std::cout << "{";
		for(const auto& item2 : item){
			std::cout << item2 << ", ";
		}
		std::cout << "\b\b}, ";
	}
	std::cout << "\b\b \n";

	return 0;
}

extern "C" __attribute__((visibility("default"))){
	int luaopen_heavy(lua_State* L){
		const luaL_Reg heavy_stuff[]{
			{"ReadKnowledge", ReadKnowledge},
			{"OutKnowledge", OutKnowledge},
			{NULL, NULL}
		};
		luaL_newmetatable(L, "knowledge");
		lua_pushcfunction(L, CleanKnowledge);
		lua_setfield(L, -2, "__gc");
		lua_pop(L, 1);
		luaL_newlib(L, heavy_stuff);

		return 1;
	}
}
