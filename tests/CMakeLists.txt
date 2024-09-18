# 添加测试可执行文件
add_executable(test_suite
    test_main.c
    test_order.c
    test_task_manager.c
)

# 链接到主项目
target_link_libraries(test_suite PRIVATE ${PROJECT_NAME}_lib)

# 添加测试
add_test(NAME AllTests COMMAND test_suite)