#include <vector>
#include <iterator>
#include <algorithm>
#include <lua.hpp>
#include <fstream>
#include <sstream>
#include <iostream>

class GoodMap{
	private:
		std::vector<int> BucketLens;
		std::vector<std::vector<std::vector<uint16_t>>> keys;
		std::vector<std::vector<std::vector<uint16_t>>> values;
	public:
		void add(std::vector<uint16_t>&& key, std::vector<uint16_t>&& value){
			int TargetLen = key.size();
			if(TargetLen == 0){
				return;
			}
			
			auto it = std::lower_bound(BucketLens.begin(), BucketLens.end(), TargetLen);
			int index = std::distance(BucketLens.begin(), it);

			if(it == BucketLens.end() || *it != TargetLen){
				if(BucketLens.empty()){
					BucketLens.push_back(TargetLen);
				}
				else{
					index = 0;
					while(index < BucketLens.size() && TargetLen > BucketLens[index]){
						index++;
					}
					BucketLens.insert(BucketLens.begin() + index, TargetLen);
				}
				keys.insert(keys.begin() + index, std::vector<std::vector<uint16_t>>());
				values.insert(values.begin() + index, std::vector<std::vector<uint16_t>>());
			}

			auto it_key = std::find(keys[index].begin(), keys[index].end(), key);

			if(it_key != keys[index].end()){
				return;
			}

			keys[index].push_back(std::move(key));
			values[index].push_back(std::move(value));
		}

		void remove(std::vector<uint16_t>& key){
			int TargetLen = key.size();
			if(TargetLen == 0){
				return;
			}
			
			auto it_bucket = std::lower_bound(BucketLens.begin(), BucketLens.end(), TargetLen);
			if(it_bucket == BucketLens.end() || *it_bucket != TargetLen){
				return;
			}
			int index = std::distance(BucketLens.begin(), it_bucket);

			auto& InsideKeys = keys[index];
			auto& InsideValues = values[index];

			auto it_keys = std::find(InsideKeys.begin(), InsideKeys.end(), key);
			if(it_keys == keys[index].end()){
				return;
			}
			int index2 = std::distance(InsideKeys.begin(), it_keys);
			
			InsideKeys.erase(InsideKeys.begin() + index2);
			InsideValues.erase(InsideValues.begin() + index2);

		}

		std::vector<uint16_t> get(const std::vector<uint16_t>& key){
			int TargetLen = key.size();
			if(TargetLen == 0){
				return std::vector<uint16_t>();
			}
			
			auto it_bucket = std::lower_bound(BucketLens.begin(), BucketLens.end(), TargetLen);
			if(it_bucket == BucketLens.end() || *it_bucket != TargetLen){
				return std::vector<uint16_t>();
			}
			int index = std::distance(BucketLens.begin(), (std::vector<int>::iterator)it_bucket);
			
			auto& InsideKeys = keys[index];
			auto& InsideValues = values[index];

			auto it_keys = std::find(InsideKeys.begin(), InsideKeys.end(), key);
			if(it_keys == keys[index].end()){
				return std::vector<uint16_t>();
			}
			int index2 = std::distance(InsideKeys.begin(), it_keys);

			return InsideValues[index2];
		}

};

extern "C" __attribute__((visibility("default"))){
	int parse(lua_State* L){
		GoodMap** UsrData = (GoodMap**)lua_newuserdata(L, sizeof(GoodMap*));
		*UsrData = new GoodMap();
	
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
				uint16_t temp;
				std::vector<uint16_t> knowledge_keys_temp;
				std::vector<uint16_t> knowledge_values_temp;
				while(read_i < knowledge_buckets[knowledge_buckets_i] && knowledge_file.read((char*)(&temp), 2)){
					knowledge_keys_temp.push_back(temp);
					read_i++;
				}
				while(knowledge_file.read((char*)(&temp), 2)){
					if(temp == 0){ break; }
					knowledge_values_temp.push_back(temp);
				}
				(*UsrData)->add(std::move(knowledge_keys_temp), std::move(knowledge_values_temp));
			}
			knowledge_buckets_i += 2;
		}
		knowledge_file.close();

		luaL_getmetatable(L, "GoodMap_m");
		lua_setmetatable(L, -2);

		return 1;
	}

	int GoodMap_new(lua_State* L){
		GoodMap** UsrData = (GoodMap**)lua_newuserdata(L, sizeof(GoodMap*));
		*UsrData = new GoodMap();

		luaL_getmetatable(L, "GoodMap_m");
		lua_setmetatable(L, -2);

		return 1;
	}

	int GoodMap_gc(lua_State* L){
		GoodMap** UsrData = (GoodMap**)luaL_checkudata(L, 1, "GoodMap_m");
		if(*UsrData){
			delete *UsrData;
			*UsrData = nullptr;
		}

		return 0;
	}

	int GoodMap_add(lua_State* L){
		GoodMap** UsrData = (GoodMap**)luaL_checkudata(L, 1, "GoodMap_m");
		std::vector<uint16_t> key(lua_rawlen(L, 2));
		for(int i = 0; i < key.size(); lua_pop(L, 1)){
			lua_rawgeti(L, 2, i+1);
			key[i++] = (uint16_t)lua_tointeger(L, -1);
		}

		std::vector<uint16_t> value(lua_rawlen(L, 3));
		for(int i = 0; i < value.size(); lua_pop(L, 1)){
			lua_rawgeti(L, 3, i+1);
			value[i++] = (uint16_t)lua_tointeger(L, -1);
		}

		(*UsrData)->add(std::move(key), std::move(value));

		return 0;
	}

	int GoodMap_remove(lua_State* L){
		GoodMap** UsrData = (GoodMap**)luaL_checkudata(L, 1, "GoodMap_m");
		std::vector<uint16_t> key(lua_rawlen(L, 2));
		for(int i = 0; i < key.size(); lua_pop(L, 1)){
			lua_rawgeti(L, 2, i+1);
			key[i++] = (uint16_t)lua_tointeger(L, -1);
		}

		(*UsrData)->remove(key);

		return 0;
	}

	int GoodMap_get(lua_State* L){
		GoodMap** UsrData = (GoodMap**)luaL_checkudata(L, 1, "GoodMap_m");
		std::vector<uint16_t> key(lua_rawlen(L, 2));
		for(int i = 0; i < key.size(); lua_pop(L, 1)){
			lua_rawgeti(L, 2, i+1);
			key[i++] = (uint16_t)lua_tointeger(L, -1);
		}

		std::vector<uint16_t> value = (*UsrData)->get(key);

		lua_newtable(L);
		for(int i = 0; i < value.size(); i++){
			lua_pushinteger(L, value[i]);
			lua_rawseti(L, -2, i+1);
		}

		return 1;
	}

	int luaopen_modules(lua_State* L){
		const luaL_Reg GoodMap_methods[] = {
			{"GoodMap_add", GoodMap_add},
			{"GoodMap_remove", GoodMap_remove},
			{"GoodMap_get", GoodMap_get},
			{NULL, NULL}
		};
		luaL_newmetatable(L, "GoodMap_m");
		lua_pushvalue(L, -1);
		lua_setfield(L, -2, "__index");
		lua_pushcfunction(L, GoodMap_gc);
		lua_setfield(L, -2, "__gc");
		luaL_setfuncs(L, GoodMap_methods, 0);
		lua_pop(L, 1);
		lua_newtable(L);
		lua_pushcfunction(L, GoodMap_new);
		lua_setfield(L, -2, "GoodMap");
		lua_pushcfunction(L, parse);
		lua_setfield(L, -2, "parse");

		return 1;
	}
}
