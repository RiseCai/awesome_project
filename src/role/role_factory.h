// role_factory.h
#ifndef ROLE_FACTORY_H
#define ROLE_FACTORY_H

#include "role.h"
#include "task.h"  // 这里包含了 RoleType 的定义

Role* CreateRole(RoleType type);

#endif // ROLE_FACTORY_H