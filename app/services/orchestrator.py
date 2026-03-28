from unittest import result

from app.domain.runtime import MachineRuntime
from app.domain.orchestrator_result import OrchestratorResult
from app.domain.event_record import EventRecord
from app.domain.events import MachineEvent, ProductionEvent


from app.utils.utils import timestamp_ms

plc = MachineRuntime(machine_id="PLC_1")
previous_state=plc.state
# Simulate some events and state changes
current_state=plc.state
result = OrchestratorResult(previous_state, current_state)