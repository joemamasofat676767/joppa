PREFIX ?= $(shell echo $$PREFIX)
lua.hpp = $(shell dirname $$(find $(PREFIX)/include -name "lua.hpp" 2>/dev/null | head -n 1))
.PHONY: clean c C GoodMap G g main m M run r R heavy h H

clean c C:
	@echo "cleaning old good_map.so:"
	-rm good_map.so
	@echo "cleaning old heavy.so"
	-rm heavy.so
	@echo ""

GoodMap G g: clean good_map.cpp
	@echo "compiling good_map.cpp:"
	clang++ -shared -fPIC -x c++ -Wl,--no-as-needed -I$(lua.hpp) good_map.cpp -L$(PREFIX)/lib -llua5.4 -Wl,--export-dynamic -Wl,-u,luaopen_GoodMap -O0  -o good_map.so -ferror-limit=0
	@echo ""

heavy h H: heavy.cpp
	@echo "compiling heavy.cpp"
	clang++ heavy.cpp -o heavy.so -ferror-limit=0

main m M: main.lua
	lua main.lua

run r R: GoodMap main.lua
	@echo "running:"
	make main
