#ifndef LINUX_ADAPTER_H
#define LINUX_ADAPTER_H

#include "../../core/domain/commands/command.h"

void LinuxAdapter_ParseCommand(const char* rawCommand, Command** outCommand);
void LinuxAdapter_ExecuteCommand(Command* command);

#endif // LINUX_ADAPTER_H
