PREFIX ?= $(shell echo $$PREFIX)
lua.hpp = $(shell dirname $$(find $(PREFIX)/include -name "lua.hpp" 2>/dev/null | head -n 1))

clean:
	@echo "cleaning old heavy.so:"
	-rm heavy.so
	@echo "\n"

heavy.so: clean heavy.cpp
	@echo "compiling heavy.cpp:"
	clang++ -shared -fPIC -x c++ -Wl,--no-as-needed -I$(lua.hpp) heavy.cpp -L$(PREFIX)/lib -llua5.4 -Wl,--export-dynamic -Wl,-u,luaopen_heavy -O0  -o heavy.so
	@echo "\n"

run: heavy.so main.lua
	@echo "running:\n"
	@lua main.lua
