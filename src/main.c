#include "order_context.h"
#include "task_manager.h"
#include <stdio.h>

int main()
{
    OrderContext *context = OrderContext_Create();

    Order *order = Order_Create(1, "Project Alpha");
    OrderContext_AddOrder(context, order);

    TaskGraph *graph = SplitOrderIntoTasks(order);

    printf("Created order with %d tasks\n", graph->task_count);

    TaskGraph_ExecuteTasks(graph);

    // 清理资源
    DEBUG_PRINT("Destroying TaskGraph\n", "");
    TaskGraph_Destroy(graph);

    DEBUG_PRINT("Destroying OrderContext\n", "");
    OrderContext_Destroy(context);

    DEBUG_PRINT("Main function completed\n", "");
    return 0;
}
