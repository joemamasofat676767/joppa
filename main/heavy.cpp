#include <iostream>
#include <tuple>
#include <vector>
#include <iterator>
#include <lua.hpp>

template <typename T>
class GoodMap{
	private:
		std::vector<int> BucketLens;
		std::vector<std::vector<std::vector<uint16_t>>> keys;
		std::vector<std::vector<T>> values;
	public:
		void insert(std::vector<uint16_t>&& key, T&& value){
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
				index = 0;
				while(index < BucketLens.size() && TargetLen > BucketLens[index]){
					index++;
				}
				BucketLens.insert(BucketLens.begin() + index, TargetLen);
				keys.insert(keys.begin() + index, std::vector<std::vector<uint16_t>>());
				values.insert(values.begin() + index, std::vector<T>());
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
					std::cout << item2 << ",";
				}
			}
			std::cout << "\n";
		}

		void remove(std::vector<uint16_t>& key){
			int TargetLen = key.size();
			if(TargetLen == 0){
				return;
			}
			
			auto it = std::lower_bound(BucketLens.begin(), BucketLens.end(), TargetLen);
			if(it == BucketLens.end() || *it != TargetLen){
				return;
			}
			int index = std::distance(BucketLens.begin(), it);

			auto& InsideKeys = keys[index];
			auto& InsideValues = values[index];

			it = std::find(InsideKeys.begin(), InsideKeys.end(), key);
			if(it == keys[index].end()){
				return;
			}
			int index2 = std::distance(InsideKeys.begin(), it);
			
			InsideKeys.erase(InsideKeys.begin() + index2);
			InsideValue.erase(InsideValue.begin() + index2);

		}

		T get(const std::vector<uint16_t>& key){
			int TargetLen = key.size();
			if(TargetLen == 0){
				return;
			}
			
			auto it = std::lower_bound(BucketLens.begin(), BucketLens.end(), TargetLen);
			if(it == BucketLens.end() || *it != TargetLen){
				return;
			}
			int index = std::distance(BucketLens.begin(), it);

			
			auto& InsideKeys = keys[index];
			auto& InsideValues = values[index];

			it = std::find(InsideKeys.begin(), InsideKeys.end(), key);
			if(it == keys[index].end()){
				return;
			}
			int index2 = std::distance(InsideKeys.begin(), it);
			
			return InsideValue[index2];

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

	int GoodMap_new(){
		GoodMap** UsrData = (GoodMap**)lua_newuserdata(L, sizeof(GoodMap*));
		*UsrData = new GoodMap();

		luaL_getmetatable(L, "GoodMap_m");
		lua_setmetatable(L, -2)

		return 1;
	}

	int GoodMap_gc(){
		GoodMap** UsrData = 

		return 0;
	}

	int temp(lua_State* L){
		GoodMap<std::string> map{};
		map.insert({1, 2, 3}, "obama");

		return 0;
	}

	int luaopen_heavy(lua_State* L){
		const luaL_Reg functions[] = {
			{"temp", temp},
			{NULL, NULL}
		};
		luaL_newlib(L, functions);

		return 1;
	}
}
