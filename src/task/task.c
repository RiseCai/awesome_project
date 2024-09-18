#include "task.h"
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>  // 添加这行以解决 sleep 函数的隐式声明警告

void InitializeTask(Task* task, int id, TaskType type, const char* description, RoleType role, VModelPhase phase) {
    task->id = id;
    task->type = type;
    strncpy(task->description, description, sizeof(task->description) - 1);
    task->description[sizeof(task->description) - 1] = '\0';
    task->assigned_role = role;
    task->phase = phase;
    task->priority = 0;
    task->timing.start_time = 0;
    task->timing.end_time = 0;
    task->timing.total_interrupt_time = 0;
    task->dependencies = NULL;
    task->dependency_count = 0;
    task->next = NULL;
    task->is_completed = false;
    task->managed_by_graph = false;
}

void ExecuteTask(Task* task) {
    printf("Executing task: %s - %s\n", GetTaskTypeName(task->type), task->description);
    task->timing.start_time = time(NULL);
    
    // 模拟任务执行
    switch(task->type) {
        case TASK_REQUIREMENTS:
            printf("Gathering and analyzing requirements...\n");
            break;
        case TASK_DESIGN:
            printf("Creating system design...\n");
            break;
        case TASK_IMPLEMENTATION:
            printf("Implementing the designed system...\n");
            break;
        case TASK_VERIFICATION:
            printf("Verifying the implemented system...\n");
            break;
        case TASK_MAINTENANCE:
            printf("Performing system maintenance...\n");
            break;
    }
    
    // 模拟任务执行时间
    sleep(2);
    
    task->timing.end_time = time(NULL);
    task->is_completed = true;
    printf("Task completed: %s - %s\n", GetTaskTypeName(task->type), task->description);
}

const char* GetTaskTypeName(TaskType type) {
    switch(type) {
        case TASK_REQUIREMENTS: return "Requirements";
        case TASK_DESIGN: return "Design";
        case TASK_IMPLEMENTATION: return "Implementation";
        case TASK_VERIFICATION: return "Verification";
        case TASK_MAINTENANCE: return "Maintenance";
        default: return "Unknown";
    }
}

void DestroyTask(Task* task) {
    DEBUG_PRINT("Destroying Task %p\n", (void*)task);
    if (task) {
        if (task->dependencies) {
            DEBUG_PRINT("Freeing dependencies for Task %p\n", (void*)task);
            free(task->dependencies);
            task->dependencies = NULL;
        }
        task->dependency_count = 0;
    }
}