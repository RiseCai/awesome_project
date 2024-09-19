cmake_minimum_required(VERSION 3.10)
set(CMAKE_BINARY_DIR ${CMAKE_CURRENT_SOURCE_DIR}/build)
project(
  awesome_project
  VERSION 1.0.0
  LANGUAGES C)

# 设置 C 标准
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# 递归查找所有的 .c 文件
file(GLOB_RECURSE SOURCES "src/*.c")

# 创建一个库，包含所有源文件
add_library(${PROJECT_NAME}_lib ${SOURCES})

# 递归添加所有包含目录
target_include_directories(
  ${PROJECT_NAME}_lib
  PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src
         ${CMAKE_CURRENT_SOURCE_DIR}/src/role
         ${CMAKE_CURRENT_SOURCE_DIR}/src/role/application
         ${CMAKE_CURRENT_SOURCE_DIR}/src/role/core
         ${CMAKE_CURRENT_SOURCE_DIR}/src/role/infrastructure
         ${CMAKE_CURRENT_SOURCE_DIR}/src/role/interfaces
         ${CMAKE_CURRENT_SOURCE_DIR}/src/role/role_abstruct
         ${CMAKE_CURRENT_SOURCE_DIR}/src/task)

# 创建主可执行文件
add_executable(${PROJECT_NAME} src/main.c)
target_link_libraries(${PROJECT_NAME} PRIVATE ${PROJECT_NAME}_lib)

# 根据不同的平台添加特定的编译选项或链接库
if(APPLE)
  target_compile_definitions(${PROJECT_NAME}_lib PUBLIC PLATFORM_MACOS)
elseif(WIN32)
  target_compile_definitions(${PROJECT_NAME}_lib PUBLIC PLATFORM_WINDOWS)
else()
  target_compile_definitions(${PROJECT_NAME}_lib PUBLIC PLATFORM_RTOS)
endif()

# 可选地添加测试
option(BUILD_TESTS "Build the tests" OFF)
if(BUILD_TESTS)
  enable_testing()
  add_subdirectory(tests)
endif()

# 安装规则
install(TARGETS ${PROJECT_NAME} DESTINATION bin)
