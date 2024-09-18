#include "../role.h"
#include "../../task/order.h"
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    Role base;
    // 可以添加产品经理特有的属性
} ProductManager;

static void ProductManager_HandleTask(Role* self, Task* task) {
    printf("Product Manager handling task: %s\n", task->description);
    // 实现任务处理逻辑
}

static void ProductManager_InterruptTask(Role* self, Task* task) {
    printf("Product Manager task interrupted: %s\n", task->description);
    // 实现任务中断逻辑
}

static void ProductManager_ResumeTask(Role* self, Task* task) {
    printf("Product Manager resuming task: %s\n", task->description);
    // 实现任务恢复逻辑
}

Role* CreateProductManager() {
    ProductManager* pm = (ProductManager*)malloc(sizeof(ProductManager));
    pm->base.HandleTask = ProductManager_HandleTask;
    pm->base.InterruptTask = ProductManager_InterruptTask;
    pm->base.ResumeTask = ProductManager_ResumeTask;
    return (Role*)pm;
}