#ifndef COMMAND_H
#define COMMAND_H

#include <stddef.h>

typedef struct CommandStatus {
    int statusCode;
    const char* message;
} CommandStatus;

typedef struct Command {
    const char* name;
    void* data;
    void (*execute)(struct Command* self);
    CommandStatus status;
} Command;

void UpdateCommandStatus(Command* command, int statusCode, const char* message);

#endif // COMMAND_H
