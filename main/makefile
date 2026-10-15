PREFIX ?= $(shell echo $$PREFIX)
lua.hpp = $(shell dirname $$(find $(PREFIX)/include -name "lua.hpp" 2>/dev/null | head -n 1))
.PHONY: clean c C GoodMap G g main m M run r R

clean c C:
	@echo "cleaning old Goodmap.so:"
	-rm GoodMap.so
	@echo ""

GoodMap G g: clean GoodMap.cpp
	@echo "compiling GoodMap.cpp:"
	clang++ -shared -fPIC -x c++ -Wl,--no-as-needed -I$(lua.hpp) GoodMap.cpp -L$(PREFIX)/lib -llua5.4 -Wl,--export-dynamic -Wl,-u,luaopen_GoodMap -O0  -o GoodMap.so -ferror-limit=0
	@echo ""

main m M: main.lua
	lua main.lua

run r R: GoodMap main.lua
	@echo "running:"
	make main
