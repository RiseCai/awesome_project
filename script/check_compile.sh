#!/bin/bash

check_compile() {
    platform=$1
    compiler=$2
    flags=$3
    echo "Checking compilation for $platform..."
    $compiler $flags -c src/platform_adapters/${platform}_adapter.c -o /dev/null
}

check_compile "linux" "gcc" "-Wall -Wextra"
check_compile "macos" "clang" "-Wall -Wextra"
check_compile "windows" "x86_64-w64-mingw32-gcc" "-Wall -Wextra"
# 对于 Android 和 RTOS，您可能需要使用特定的交叉编译器或模拟器

echo "Compilation checks complete."