#include <iostream>
#include <tuple>
#include <vector>
#include <iterator>
#include <algorithm>
#include <lua.hpp>

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
			std::cout << "bucket lens:\n";
			for(const auto& item : BucketLens){
				std::cout << item << ",";
			}
			std::cout << "\nkeys:\n";
			for(const auto& item : keys){
				for(const auto& item2: item){
					for(const auto& item3 : item2){
						std::cout << item3 << ",";
					}
				}
			}
			std::cout << "\nvalues:\n";
			for(const auto& item : values){
				for(const auto& item2 : item){
					for(const auto& item3 : item2){
						std::cout << item3 << ",";
					}
				}
			}
			std::cout << "\n";
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

	//int GetKnowledge(lua_State* L){
	//	std::tuple<int, std::vector<std::string>, >

	//	return ;
	//}

	//int similarity(lua_State* L){
		
		
	//	return 0;
	//}

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

	int luaopen_GoodMap(lua_State* L){
		const luaL_Reg GoodMap_stuff[] = {
			{"add", GoodMap_add},
			{"remove", GoodMap_remove},
			{NULL, NULL}
		};
		luaL_newmetatable(L, "GoodMap_m");
		lua_pushvalue(L, -1);
		lua_setfield(L, -2, "__index");
		lua_pushcfunction(L, GoodMap_gc);
		lua_setfield(L, -2, "__gc");
		luaL_setfuncs(L, GoodMap_stuff, 0);
		lua_pop(L, 1);
		lua_newtable(L);
		lua_pushcfunction(L, GoodMap_new);
		lua_setfield(L, -2, "GoodMap");

		return 1;
	}
}
