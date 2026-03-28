from dataclasses import dataclass, field

from app.domain.production import ProductionCounter
from app.domain.states import State


@dataclass(slots=True)
class MachineRuntime:
    machine_id: str
    state: State = State.IDLE
    counter: ProductionCounter = field(default_factory=ProductionCounter)
