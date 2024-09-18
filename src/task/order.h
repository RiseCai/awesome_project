#ifndef ORDER_H
#define ORDER_H

#include "task.h"

typedef struct Order {
    int id;
    char* name;
    Task* tasks;  // 指向任务链表的头部
    int task_count;
} Order;

Order* Order_Create(int id, const char* name);
void Order_AddTask(Order* order, Task* task);
void Order_Destroy(Order* order);

#endif // ORDER_H
