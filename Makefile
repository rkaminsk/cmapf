BUILD_TYPE:=debug
CLINGO_DIR:=${HOME}/.local/opt/potassco/$(BUILD_TYPE)/lib/cmake/Clingo
CXXFLAGS=-Wall -Wextra -Wpedantic

.PHONY: all configure compdb

all: configure
	@TERM=dumb MAKEFLAGS= MFLAGS= cmake --build "build/$(BUILD_TYPE)" --target all

test: all
	@cmake --build "build/$(BUILD_TYPE)" --target "test"

%: configure
	@cmake --build "build/$(BUILD_TYPE)" --target "$@"

# compdb can be installed with pip
compdb: configure
	compdb -p "build/$(BUILD_TYPE)" list -1 > compile_commands.json

configure: build/$(BUILD_TYPE)/build.ninja

build/$(BUILD_TYPE)/build.ninja:
	cmake -G Ninja -H. -B"build/$(BUILD_TYPE)" -DCMAKE_INSTALL_PREFIX=${HOME}/.local/opt/potassco/$(BUILD_TYPE) -DCMAKE_CXX_FLAGS="$(CXXFLAGS)" -DCMAKE_BUILD_TYPE="$(BUILD_TYPE)" -DClingo_DIR="$(CLINGO_DIR)" -DCMAPF_BUILD_TESTS=On -DCMAKE_EXPORT_COMPILE_COMMANDS=On

Makefile:
	:
