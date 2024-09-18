#ifndef TASK_H
#define TASK_H

#include <stdbool.h>
#include <stdio.h>

#define DEBUG_PRINT(fmt, ...) \
    do { fprintf(stderr, "%s:%d:%s(): " fmt, __FILE__, \
                __LINE__, __func__, __VA_ARGS__); } while (0)

#include <time.h>
#include "../role/role_types.h"  // 包含 RoleType 定义
#include "../core/state_machine.h"

typedef enum {
    PHASE_REQUIREMENTS,
    PHASE_DESIGN,
    PHASE_IMPLEMENTATION,
    PHASE_VERIFICATION,
    PHASE_MAINTENANCE
} VModelPhase;

typedef enum {
    TASK_REQUIREMENTS,
    TASK_DESIGN,
    TASK_IMPLEMENTATION,
    TASK_VERIFICATION,
    TASK_MAINTENANCE
} TaskType;

typedef struct {
    time_t start_time;
    time_t end_time;
    time_t total_interrupt_time;
} TaskTiming;

typedef struct Task {
    int id;
    char description[100];  // 改为数组而不是指针
    RoleType assigned_role;
    VModelPhase phase;
    TaskType type;
    int priority;
    TaskTiming timing;
    struct Task** dependencies;
    int dependency_count;
    struct Task* next;  // For linked list implementation
    bool is_completed;
    bool managed_by_graph;  // 新增字段
    StateMachine state_machine;
} Task;

const char* GetTaskTypeName(TaskType type);
void InitializeTask(Task* task, int id, TaskType type, const char* description, RoleType role, VModelPhase phase);
void ExecuteTask(Task* task);
void DestroyTask(Task* task);

void Task_Initialize(Task* task);
void Task_Run(Task* task);
void Task_Pause(Task* task);
void Task_Resume(Task* task);
void Task_Sleep(Task* task);
void Task_Wake(Task* task);
void Task_Reset(Task* task);

#endif // TASK_H