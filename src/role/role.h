#ifndef ROLE_H
#define ROLE_H

#include "role_types.h"

struct Task;

typedef struct Role {
    void (*HandleTask)(struct Role *self, struct Task *task);
    void (*InterruptTask)(struct Role *self, struct Task *task);
    void (*ResumeTask)(struct Role *self, struct Task *task);
} Role;

typedef Role *(*RoleFactory)();

Role *CreateRole(RoleType type);

#endif // ROLE_H
