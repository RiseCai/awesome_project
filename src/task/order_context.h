#ifndef ORDER_CONTEXT_H
#define ORDER_CONTEXT_H

#include "order.h"

typedef struct OrderContext {
    Order **orders;
    int order_count;
    int capacity;
} OrderContext;

OrderContext *OrderContext_Create();
void OrderContext_AddOrder(OrderContext *context, Order *order);
Order *OrderContext_GetOrderById(OrderContext *context, int id);
void OrderContext_Destroy(OrderContext *context);

#endif // ORDER_CONTEXT_H
