// role_factory.c
#include "role_factory.h"
#include "product_manager.h"
// 包含其他角色的头文件

Role* CreateRole(RoleType type) {
    switch (type) {
        case ROLE_PRODUCT_MANAGER:
            return CreateProductManager();
        // 为其他角色添加 case
        default:
            return NULL;
    }
}