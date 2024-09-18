#include "order_context.h"
#include <stdlib.h>

#define INITIAL_CAPACITY 10

OrderContext* OrderContext_Create() {
    OrderContext* context = (OrderContext*)malloc(sizeof(OrderContext));
    if (context) {
        context->orders = NULL;
        context->order_count = 0;
        context->capacity = 0;
    }
    return context;
}

void OrderContext_AddOrder(OrderContext* context, Order* order) {
    if (context->order_count == context->capacity) {
        int new_capacity = context->capacity == 0 ? 1 : context->capacity * 2;
        context->orders = (Order**)realloc(context->orders, new_capacity * sizeof(Order*));
        context->capacity = new_capacity;
    }
    context->orders[context->order_count++] = order;
}

Order* OrderContext_GetOrderById(OrderContext* context, int id) {
    for (int i = 0; i < context->order_count; i++) {
        if (context->orders[i]->id == id) {
            return context->orders[i];
        }
    }
    return NULL;
}

void OrderContext_Destroy(OrderContext* context) {
    if (context) {
        DEBUG_PRINT("Destroying OrderContext %p with %d orders\n", (void*)context, context->order_count);
        for (int i = 0; i < context->order_count; i++) {
            DEBUG_PRINT("Destroying Order %d (%p) in OrderContext\n", i, (void*)context->orders[i]);
            Order_Destroy(context->orders[i]);
        }
        free(context->orders);
        free(context);
    }
}