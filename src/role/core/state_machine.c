#include "state_machine.h"
#include <stdio.h>

void StateMachine_Init(StateMachine *sm)
{
    sm->current_state = STATE_UNINITIALIZED;
}

void StateMachine_Transition(StateMachine *sm, State new_state)
{
    printf("Transitioning from %d to %d\n", sm->current_state, new_state);
    sm->current_state = new_state;
}
