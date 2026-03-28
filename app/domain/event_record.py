from dataclasses import dataclass, field
from typing import Any

from app.domain.events import MachineEvent, ProductionEvent


@dataclass(slots=True)
class EventRecord:
    event: MachineEvent | ProductionEvent
    timestamp_ms: int
    payload: dict[str, Any] = field(default_factory=dict)
