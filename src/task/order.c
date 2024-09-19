#define _POSIX_C_SOURCE 200809L

#include "order.h"
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
#define _strdup strdup
#else
#define _POSIX_C_SOURCE 200809L
#endif

Order *Order_Create(int id, const char *name)
{
    Order *order = (Order *)malloc(sizeof(Order));
    if (order) {
        order->id = id;
        order->name = malloc(strlen(name) + 1);
        if (order->name) {
            strcpy(order->name, name);
        } else {
            free(order);
            return NULL;
        }
        order->tasks = NULL;
        order->task_count = 0;
    }
    return order;
}

void Order_AddTask(Order *order, Task *task)
{
    if (order && task) {
        task->next = order->tasks;
        order->tasks = task;
        order->task_count++;
    }
}

void Order_Destroy(Order *order)
{
    DEBUG_PRINT("Destroying Order %p\n", (void *)order);
    if (order) {
        Task *current = order->tasks;
        while (current) {
            Task *next = current->next;
            DEBUG_PRINT("Checking Task %p in Order\n", (void *)current);
            if (!current->managed_by_graph) {
                DEBUG_PRINT("Destroying unmanaged Task %p in Order\n",
                            (void *)current);
                DestroyTask(current);
                free(current);
            } else {
                DEBUG_PRINT("Skipping managed Task %p in Order\n",
                            (void *)current);
            }
            current = next;
        }
        DEBUG_PRINT("Freeing Order name %p\n", (void *)order->name);
        free(order->name);
        order->name = NULL;
        order->tasks = NULL;
    }
}