#ifndef TASK_MANAGER_H
#define TASK_MANAGER_H

#include "../core/state_machine.h"
#include "order.h"
#include "task.h"

typedef struct TaskGraph {
    Task **tasks;
    int task_count;
    int capacity;
    int **dependencies; // 依赖关系矩阵
    StateMachine state_machine;
} TaskGraph;

// 创建任务图
TaskGraph *TaskGraph_Create(void);

// 向任务图中添加任务
void TaskGraph_AddTask(TaskGraph *graph, Task *task);

// 在任务之间添加依赖关系
void TaskGraph_AddDependency(TaskGraph *graph, int taskIndex,
                             int dependencyIndex);

// 将订单拆分为任务
TaskGraph *SplitOrderIntoTasks(Order *order);

// 销毁任务图
void TaskGraph_Destroy(TaskGraph *graph);

// 其他可能需要的函数声明...

// 新增：获取任务图中的任务数量
int TaskGraph_GetTaskCount(const TaskGraph *graph);

// 新增：执行任务图中的任务
void TaskGraph_ExecuteTasks(TaskGraph *graph);

// 新增：状态机相关函数
void TaskGraph_Initialize(TaskGraph *graph);
void TaskGraph_Run(TaskGraph *graph);
void TaskGraph_Pause(TaskGraph *graph);
void TaskGraph_Resume(TaskGraph *graph);
void TaskGraph_Sleep(TaskGraph *graph);
void TaskGraph_Wake(TaskGraph *graph);
void TaskGraph_Reset(TaskGraph *graph);

#endif // TASK_MANAGER_H
