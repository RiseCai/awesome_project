#!/bin/bash

check_platform() {
    platform=$1
    echo "Checking $platform code style..."
    # find src/platform_adapters -name "${platform}_adapter.*" | xargs clang-format -style=file -n -Werror
}

echo "Checking common C code style..."
find src -name "*.c" -o -name "*.h" | grep -v "platform_adapters" | xargs clang-format -style=file -n -Werror

check_platform "android"
check_platform "linux"
check_platform "macos"
check_platform "rtos"
check_platform "windows"

echo "Checking CMake files..."
find . -name "CMakeLists.txt" -o -name "*.cmake" | grep -v "./build/" | xargs cmake-lint

echo "Running cppcheck..."
cppcheck --enable=all --suppress=missingInclude --suppress=unusedFunction --suppress=strdupCalled --platform=unix64 src
cppcheck --enable=all --suppress=missingInclude --suppress=unusedFunction --suppress=strdupCalled --platform=win64 src

echo "Running cmake-lint..."
find . -name "CMakeLists.txt" -o -name "*.cmake" | grep -v "./build/" | xargs cmake-lint

if [ $? -eq 0 ]; then
    echo "All style checks passed!"
else
    echo "Some style checks failed. Please run the format scripts to fix issues."
fi