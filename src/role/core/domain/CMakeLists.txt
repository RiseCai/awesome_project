add_library(core_domain commands/command.c commands/command_factory.c)

target_include_directories(core_domain PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
