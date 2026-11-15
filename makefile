MAKEFLAGS += --no-print-directory
PREFIX ?= $(shell echo $$PREFIX)
lua.hpp = $(shell dirname $$(find $(PREFIX)/include -name "lua.hpp" 2>/dev/null | head -n 1))
.PHONY: clean cl module mo main ma run ru binary bi

clean cl:
	@echo "cleaning old modules.so:"
	-rm modules.so

modules mo: modules.cpp
	@echo "compiling modules.cpp:"
	clang++ -shared -fPIC -x c++ -Wl,--no-as-needed -I$(lua.hpp) modules.cpp -L$(PREFIX)/lib -llua5.4 -Wl,--export-dynamic -Wl,-u,luaopen_modules -O0  -o modules.so -ferror-limit=0

main ma: main.lua
	lua main.lua

run ru:
	@make modules
	@echo "\nrunning:"	
	@make main

binary bi: dev_tools/to_binary.py
	@echo "turning knowledge.bin into binary:\n"
	python dev_tools/to_binary.py
