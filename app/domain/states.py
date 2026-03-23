from enum import Enum


class State(str, Enum):
    IDLE = "idle"
    STARTING = "starting"
    RUNNING = "running"
    STARVED = "starved"
    BLOCKED = "blocked"
    STOPPED = "stopped"
    FAULTED = "faulted"
    E_STOP = "e_stop"
    RESETTING = "resetting"
