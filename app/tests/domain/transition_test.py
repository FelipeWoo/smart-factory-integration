import pytest

from app.domain.events import MachineEvent
from app.domain.states import State
from app.domain.transitions import TRANSITIONS, resolve_next_state
from app.utils.boot import boot
from app.utils.logger import logger

boot_config = boot("test_transition_rules")


def test_logger():
    logger.info("Testing domain transitions rules.")


@pytest.mark.parametrize(
    "current_state,transition_event,expected_state",
    [
        pytest.param(state, event, next_state,
                     id=f"{state} + {event} -> {next_state}")
        for state, transitions in TRANSITIONS.items()
        for event, next_state in transitions.items()
    ],
)
def test_all_defined_transitions(current_state, transition_event, expected_state):
    assert resolve_next_state(
        current_state, transition_event
    ) == expected_state


def test_all_next_states_are_valid():
    for state, transitions in TRANSITIONS.items():
        for event, next_state in transitions.items():
            assert next_state in State, f"Invalid next state {next_state} for event {event} from state {state}"


def test_all_states_have_transitions_defined():
    for state in State:
        assert state in TRANSITIONS, f"{state} missing in TRANSITIONS"


def test_each_event_used_somewhere():
    used_events = {
        event
        for transitions in TRANSITIONS.values()
        for event in transitions
    }

    for event in MachineEvent:
        assert event in used_events, f"{event} unused"


def test_all_invalid_transitions():
    for state in State:
        for event in MachineEvent:
            if event not in TRANSITIONS.get(state, {}):
                with pytest.raises(ValueError):
                    resolve_next_state(state, event)
