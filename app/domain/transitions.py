from app.domain.events import MachineEvent
from app.domain.states import State

TRANSITIONS: dict[State, dict[MachineEvent, State]] = {

    State.IDLE: {
        MachineEvent.START_REQUESTED: State.STARTING,
        MachineEvent.FAULT_DETECTED: State.FAULTED,
        MachineEvent.STOP_REQUESTED: State.STOPPED,
        MachineEvent.EMERGENCY_STOP_PRESSED: State.E_STOP,
    },

    State.STARTING: {
        MachineEvent.STARTED: State.RUNNING,
        MachineEvent.FAULT_DETECTED: State.FAULTED,
        MachineEvent.STOP_REQUESTED: State.STOPPED,
        MachineEvent.EMERGENCY_STOP_PRESSED: State.E_STOP,
    },

    State.RUNNING: {
        MachineEvent.HEARTBEAT: State.RUNNING,
        MachineEvent.BLOCKAGE_DETECTED: State.BLOCKED,
        MachineEvent.STARVATION_DETECTED: State.STARVED,
        MachineEvent.FAULT_DETECTED: State.FAULTED,
        MachineEvent.STOP_REQUESTED: State.STOPPED,
        MachineEvent.EMERGENCY_STOP_PRESSED: State.E_STOP,
    },

    State.STARVED: {
        MachineEvent.RESET_REQUESTED: State.RESETTING,
        MachineEvent.FAULT_DETECTED: State.FAULTED,
        MachineEvent.STOP_REQUESTED: State.STOPPED,
        MachineEvent.EMERGENCY_STOP_PRESSED: State.E_STOP,
    },

    State.BLOCKED: {
        MachineEvent.RESET_REQUESTED: State.RESETTING,
        MachineEvent.FAULT_DETECTED: State.FAULTED,
        MachineEvent.STOP_REQUESTED: State.STOPPED,
        MachineEvent.EMERGENCY_STOP_PRESSED: State.E_STOP,
    },

    State.STOPPED: {
        MachineEvent.START_REQUESTED: State.STARTING,
        MachineEvent.FAULT_DETECTED: State.FAULTED,
        MachineEvent.EMERGENCY_STOP_PRESSED: State.E_STOP,
    },

    State.FAULTED: {
        MachineEvent.FAULT_CLEARED: State.IDLE,
        MachineEvent.RESET_REQUESTED: State.RESETTING,
        MachineEvent.EMERGENCY_STOP_PRESSED: State.E_STOP,
    },

    State.E_STOP: {
        MachineEvent.EMERGENCY_STOP_CLEARED: State.STOPPED,
    },

    State.RESETTING: {
        MachineEvent.RESET_COMPLETED: State.IDLE,
        MachineEvent.FAULT_DETECTED: State.FAULTED,
        MachineEvent.STOP_REQUESTED: State.STOPPED,
        MachineEvent.EMERGENCY_STOP_PRESSED: State.E_STOP,
    },

}


def resolve_next_state(current: State, event: MachineEvent) -> State:
    try:
        return TRANSITIONS[current][event]
    except KeyError:
        raise ValueError(
            f"Invalid transition: {current.value} + {event.value}"
        )
