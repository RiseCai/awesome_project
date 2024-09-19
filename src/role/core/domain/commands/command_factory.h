#ifndef COMMAND_FACTORY_H
#define COMMAND_FACTORY_H

#include "command.h"

Command *CreateCommand(const char *commandName, void *commandData);

#endif // COMMAND_FACTORY_H
