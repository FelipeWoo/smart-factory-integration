from enum import Enum


class Event(str, Enum):

    MACHINE_START_REQUESTED = "machine_start_requested"
    MACHINE_STARTED = "machine_started"

    MACHINE_STARVATION_DETECTED = "machine_starvation_detected"

    MACHINE_BLOCKAGE_DETECTED = "machine_blockage_detected"

    MACHINE_STOP_REQUESTED = "machine_stop_requested"

    MACHINE_FAULT_DETECTED = "machine_fault_detected"
    MACHINE_FAULT_CLEARED = "machine_fault_cleared"

    MACHINE_E_STOP_PRESSED = "machine_e_stop_pressed"
    MACHINE_E_STOP_CLEARED = "machine_e_stop_cleared"

    MACHINE_RESET_REQUESTED = "machine_reset_requested"
    MACHINE_RESET_COMPLETED = "machine_reset_completed"

    UNIT_DETECTED = "unit_detected"
    UNIT_CLASSIFIED = "unit_classified"

    PACKAGE_STARTED = "package_started"
    PACKAGE_COMPLETED = "package_completed"

    HEARTBEAT = "heartbeat"
