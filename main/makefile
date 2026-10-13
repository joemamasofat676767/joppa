PREFIX ?= $(shell echo $$PREFIX)
lua.hpp = $(shell dirname $$(find $(PREFIX)/include -name "lua.hpp" 2>/dev/null | head -n 1))
.PHONY: clean c C heavy h H main m M run r R

clean c C:
	@echo "cleaning old heavy.so:"
	-rm heavy.so
	@echo ""

heavy h H: clean heavy.cpp
	@echo "compiling heavy.cpp:"
	clang++ -shared -fPIC -x c++ -Wl,--no-as-needed -I$(lua.hpp) heavy.cpp -L$(PREFIX)/lib -llua5.4 -Wl,--export-dynamic -Wl,-u,luaopen_heavy -O0  -o heavy.so
	@echo ""

main m M: main.lua
	lua main.lua

run r R: heavy main.lua
	@echo "running:"
	make main
