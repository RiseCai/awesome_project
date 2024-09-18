#include "task_manager.h"
#include <stdlib.h>
#include <string.h>

TaskGraph* TaskGraph_Create(void) {
    TaskGraph* graph = (TaskGraph*)malloc(sizeof(TaskGraph));
    if (graph) {
        graph->tasks = NULL;
        graph->task_count = 0;
        graph->capacity = 0;
        graph->dependencies = NULL;
    }
    return graph;
}

void TaskGraph_AddTask(TaskGraph* graph, Task* task) {
    if (graph->task_count == graph->capacity) {
        int new_capacity = graph->capacity == 0 ? 1 : graph->capacity * 2;
        graph->tasks = (Task**)realloc(graph->tasks, new_capacity * sizeof(Task*));
        graph->capacity = new_capacity;

        // 重新分配依赖关系矩阵
        graph->dependencies = (int**)realloc(graph->dependencies, new_capacity * sizeof(int*));
        for (int i = 0; i < new_capacity; i++) {
            if (i >= graph->task_count) {
                graph->dependencies[i] = (int*)calloc(new_capacity, sizeof(int));
            } else {
                graph->dependencies[i] = (int*)realloc(graph->dependencies[i], new_capacity * sizeof(int));
                for (int j = graph->task_count; j < new_capacity; j++) {
                    graph->dependencies[i][j] = 0;
                }
            }
        }
    }
    graph->tasks[graph->task_count++] = task;
    task->managed_by_graph = true;
}

void TaskGraph_AddDependency(TaskGraph* graph, int taskIndex, int dependencyIndex) {
    if (taskIndex < graph->task_count && dependencyIndex < graph->task_count) {
        graph->dependencies[taskIndex][dependencyIndex] = 1;
    }
}

void TaskGraph_Destroy(TaskGraph* graph) {
    DEBUG_PRINT("Destroying TaskGraph %p\n", (void*)graph);
    if (graph) {
        for (int i = 0; i < graph->task_count; i++) {
            if (graph->tasks[i]) {
                DEBUG_PRINT("Destroying Task %d (%p)\n", i, (void*)graph->tasks[i]);
                if (graph->tasks[i]->managed_by_graph) {
                    DestroyTask(graph->tasks[i]);
                    free(graph->tasks[i]);
                } else {
                    DEBUG_PRINT("Task %d not managed by graph\n", i);
                }
                graph->tasks[i] = NULL;
            }
            if (graph->dependencies[i]) {
                free(graph->dependencies[i]);
                graph->dependencies[i] = NULL;
            }
        }
        free(graph->tasks);
        free(graph->dependencies);
        free(graph);
    }
}

TaskGraph* SplitOrderIntoTasks(Order* order) {
    TaskGraph* graph = TaskGraph_Create();
    
    // 创建任务
    for (VModelPhase phase = PHASE_REQUIREMENTS; phase <= PHASE_MAINTENANCE; phase++) {
        Task* task = (Task*)malloc(sizeof(Task));
        InitializeTask(task, 
                       order->task_count + graph->task_count, 
                       (TaskType)phase,
                       "Placeholder task",
                       ROLE_PRODUCT_MANAGER,
                       phase);
        task->managed_by_graph = true;  // 确保设置这个标志
        TaskGraph_AddTask(graph, task);
    }
    
    // 添加依赖关系
    for (int i = 1; i < graph->task_count; i++) {
        TaskGraph_AddDependency(graph, i, i-1);
    }
    
    return graph;
}

void TaskGraph_ExecuteTasks(TaskGraph* graph) {
    int* executed = (int*)calloc(graph->task_count, sizeof(int));
    int executed_count = 0;

    while (executed_count < graph->task_count) {
        for (int i = 0; i < graph->task_count; i++) {
            if (!executed[i]) {
                int can_execute = 1;
                for (int j = 0; j < graph->task_count; j++) {
                    if (graph->dependencies[i][j] && !executed[j]) {
                        can_execute = 0;
                        break;
                    }
                }
                if (can_execute) {
                    ExecuteTask(graph->tasks[i]);
                    executed[i] = 1;
                    executed_count++;
                }
            }
        }
    }

    free(executed);
}

int TaskGraph_GetTaskCount(const TaskGraph* graph) {
    return graph ? graph->task_count : 0;
}