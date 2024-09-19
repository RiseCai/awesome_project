#!/bin/bash

echo "Formatting C code..."
find src -name "*.c" -o -name "*.h" | xargs clang-format -style=file -i

echo "Formatting CMake files..."
find . -name "CMakeLists.txt" -o -name "*.cmake" | xargs cmake-format -i

echo "Code formatting complete."