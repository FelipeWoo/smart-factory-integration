from dataclasses import dataclass, field

from app.domain.events import MachineEvent, ProductionEvent
from app.domain.states import State


@dataclass(slots=True)
class OrchestratorResult:
    previous_state: State
    current_state: State
    emitted_events: list[MachineEvent |
                         ProductionEvent] = field(default_factory=list)
