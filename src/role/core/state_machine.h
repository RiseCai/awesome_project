#ifndef STATE_MACHINE_H
#define STATE_MACHINE_H

typedef enum {
    STATE_UNINITIALIZED,
    STATE_INITIALIZED,
    STATE_RUNNING,
    STATE_PAUSED,
    STATE_SLEEPING,
    STATE_COMPLETED,
    STATE_ERROR
} State;

typedef struct {
    State current_state;
    void (*initialize)(void* context);
    void (*run)(void* context);
    void (*pause)(void* context);
    void (*resume)(void* context);
    void (*sleep)(void* context);
    void (*wake)(void* context);
    void (*reset)(void* context);
} StateMachine;

void StateMachine_Init(StateMachine* sm);
void StateMachine_Transition(StateMachine* sm, State new_state);

#endif // STATE_MACHINE_H
