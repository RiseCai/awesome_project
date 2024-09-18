#include "cli_interface.h"
#include "../../../../task/task_manager.h"
#include <stdio.h>
#include <string.h>

#define MAX_COMMAND_LENGTH 100

void print_menu() {
    printf("\n--- Task Management System ---\n");
    printf("1. Create new task\n");
    printf("2. List all tasks\n");
    printf("3. Execute all tasks\n");
    printf("4. Show task dependencies\n");
    printf("5. Initialize system\n");
    printf("6. Pause system\n");
    printf("7. Resume system\n");
    printf("8. Sleep system\n");
    printf("9. Wake system\n");
    printf("10. Reset system\n");
    printf("11. Manage individual task\n");
    printf("12. Replace task\n");
    printf("13. Help\n");
    printf("14. Exit\n");
    printf("Enter your choice: ");
}

// ... 保留现有函数 ...

void initialize_system(TaskGraph* graph) {
    TaskGraph_Initialize(graph);
    printf("System initialized.\n");
}

void pause_system(TaskGraph* graph) {
    TaskGraph_Pause(graph);
    printf("System paused.\n");
}

void resume_system(TaskGraph* graph) {
    TaskGraph_Resume(graph);
    printf("System resumed.\n");
}

void sleep_system(TaskGraph* graph) {
    TaskGraph_Sleep(graph);
    printf("System sleeping.\n");
}

void wake_system(TaskGraph* graph) {
    TaskGraph_Wake(graph);
    printf("System woken up.\n");
}

void reset_system(TaskGraph* graph) {
    TaskGraph_Reset(graph);
    printf("System reset.\n");
}

void manage_individual_task(TaskGraph* graph) {
    int task_id;
    printf("Enter task ID: ");
    scanf("%d", &task_id);
    
    Task* task = TaskGraph_GetTaskById(graph, task_id);
    if (task == NULL) {
        printf("Task not found.\n");
        return;
    }
    
    int choice;
    printf("1. Initialize\n2. Run\n3. Pause\n4. Resume\n5. Sleep\n6. Wake\n7. Reset\n");
    printf("Enter choice: ");
    scanf("%d", &choice);
    
    switch (choice) {
        case 1: Task_Initialize(task); break;
        case 2: Task_Run(task); break;
        case 3: Task_Pause(task); break;
        case 4: Task_Resume(task); break;
        case 5: Task_Sleep(task); break;
        case 6: Task_Wake(task); break;
        case 7: Task_Reset(task); break;
        default: printf("Invalid choice.\n");
    }
}

void replace_task(TaskGraph* graph) {
    int old_task_id, new_task_id;
    printf("Enter ID of task to replace: ");
    scanf("%d", &old_task_id);
    printf("Enter ID of new task: ");
    scanf("%d", &new_task_id);
    
    if (TaskGraph_ReplaceTask(graph, old_task_id, new_task_id)) {
        printf("Task replaced successfully.\n");
    } else {
        printf("Failed to replace task.\n");
    }
}

void run_cli(TaskGraph* graph) {
    char command[MAX_COMMAND_LENGTH];
    int choice;

    while (1) {
        print_menu();
        fgets(command, MAX_COMMAND_LENGTH, stdin);
        sscanf(command, "%d", &choice);

        switch (choice) {
            case 1: create_task(graph); break;
            case 2: list_tasks(graph); break;
            case 3: execute_tasks(graph); break;
            case 4: show_dependencies(graph); break;
            case 5: initialize_system(graph); break;
            case 6: pause_system(graph); break;
            case 7: resume_system(graph); break;
            case 8: sleep_system(graph); break;
            case 9: wake_system(graph); break;
            case 10: reset_system(graph); break;
            case 11: manage_individual_task(graph); break;
            case 12: replace_task(graph); break;
            case 13: show_help(); break;
            case 14: printf("Exiting...\n"); return;
            default: printf("Invalid choice. Please try again.\n");
        }
    }
}