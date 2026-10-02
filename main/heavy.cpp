#include <iostream>
#include <lua.hpp>

extern "C"{
	int hello(lua_State* L){
		std::cout << "hello\n";
		return 0;
	}
}

extern "C" __attribute__((visibility("default"))) int luaopen_heavy(lua_State* L){
	const luaL_Reg functions[] = {
		{"hello", hello},
		{NULL, NULL}
	};
	luaL_newlib(L, functions);
	return 1;
}
