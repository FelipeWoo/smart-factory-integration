from enum import Enum


class MachineEvent(str, Enum):

    START_REQUESTED = "machine_start_requested"
    STARTED = "machine_started"

    STARVATION_DETECTED = "machine_starvation_detected"

    BLOCKAGE_DETECTED = "machine_blockage_detected"

    STOP_REQUESTED = "machine_stop_requested"

    FAULT_DETECTED = "machine_fault_detected"
    FAULT_CLEARED = "machine_fault_cleared"

    EMERGENCY_STOP_PRESSED = "machine_e_stop_pressed"
    EMERGENCY_STOP_CLEARED = "machine_e_stop_cleared"

    RESET_REQUESTED = "machine_reset_requested"
    RESET_COMPLETED = "machine_reset_completed"

    HEARTBEAT = "heartbeat"


class ProductionEvent(str, Enum):
    UNIT_DETECTED = "unit_detected"
    UNIT_CLASSIFIED = "unit_classified"

    PACKAGE_STARTED = "package_started"
    PACKAGE_COMPLETED = "package_completed"

    PRODUCTION_TARGET_REACHED = "production_target_reached"
    SCRAP_THRESHOLD_EXCEEDED = " scrap_threshold_exceeded"
