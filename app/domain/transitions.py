from app.domain.events import Event
from app.domain.states import State

TRANSITIONS: dict[State, dict[Event, State]] = {

    State.IDLE: {
        Event.MACHINE_START_REQUESTED: State.STARTING,
        Event.MACHINE_FAULT_DETECTED: State.FAULTED,
        Event.MACHINE_STOP_REQUESTED: State.STOPPED,
        Event.MACHINE_E_STOP_PRESSED: State.E_STOP,
    },

    State.STARTING: {
        Event.MACHINE_STARTED: State.RUNNING,
        Event.MACHINE_FAULT_DETECTED: State.FAULTED,
        Event.MACHINE_STOP_REQUESTED: State.STOPPED,
        Event.MACHINE_E_STOP_PRESSED: State.E_STOP,
    },

    State.RUNNING: {
        Event.HEARTBEAT: State.RUNNING,
        Event.UNIT_DETECTED: State.RUNNING,
        Event.UNIT_CLASSIFIED: State.RUNNING,
        Event.PACKAGE_STARTED: State.RUNNING,
        Event.PACKAGE_COMPLETED: State.RUNNING,
        Event.MACHINE_STARVATION_DETECTED: State.STARVED,
        Event.MACHINE_BLOCKAGE_DETECTED: State.BLOCKED,
        Event.MACHINE_FAULT_DETECTED: State.FAULTED,
        Event.MACHINE_STOP_REQUESTED: State.STOPPED,
        Event.MACHINE_E_STOP_PRESSED: State.E_STOP,
    },

    State.STARVED: {
        Event.MACHINE_RESET_REQUESTED: State.RESETTING,
        Event.MACHINE_FAULT_DETECTED: State.FAULTED,
        Event.MACHINE_STOP_REQUESTED: State.STOPPED,
        Event.MACHINE_E_STOP_PRESSED: State.E_STOP,
    },

    State.BLOCKED: {
        Event.MACHINE_RESET_REQUESTED: State.RESETTING,
        Event.MACHINE_FAULT_DETECTED: State.FAULTED,
        Event.MACHINE_STOP_REQUESTED: State.STOPPED,
        Event.MACHINE_E_STOP_PRESSED: State.E_STOP,
    },

    State.STOPPED: {
        Event.MACHINE_START_REQUESTED: State.STARTING,
        Event.MACHINE_FAULT_DETECTED: State.FAULTED,
        Event.MACHINE_E_STOP_PRESSED: State.E_STOP,
    },

    State.FAULTED: {
        Event.MACHINE_FAULT_CLEARED: State.IDLE,
        Event.MACHINE_RESET_REQUESTED: State.RESETTING,
        Event.MACHINE_E_STOP_PRESSED: State.E_STOP,
    },

    State.E_STOP: {
        Event.MACHINE_E_STOP_CLEARED: State.STOPPED,
    },

    State.RESETTING: {
        Event.MACHINE_RESET_COMPLETED: State.IDLE,
        Event.MACHINE_FAULT_DETECTED: State.FAULTED,
        Event.MACHINE_STOP_REQUESTED: State.STOPPED,
        Event.MACHINE_E_STOP_PRESSED: State.E_STOP,
    },

}


def resolve_next_state(current: State, event: Event) -> State:
    try:
        return TRANSITIONS[current][event]
    except KeyError:
        raise ValueError(
            f"Invalid transition: {current.value} + {event.value}"
        )
