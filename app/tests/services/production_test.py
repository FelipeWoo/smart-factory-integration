
from app.domain.events import ProductionEvent
from app.domain.production import ProductionCounter
from app.services.production import apply_production_rules
from app.utils.boot import boot
from app.utils.logger import logger

boot_config = boot("test_production_service_rules")


def test_logger():
    logger.info("Testing domain production rules.")


def test_one_good_unit_emits_package_started():
    counter = ProductionCounter()
    emitted_events = apply_production_rules(
        counter, {"result": "ok"})

    assert emitted_events == [ProductionEvent.PACKAGE_STARTED]
    assert counter.good_units == 1
    assert counter.completed_packages == 0
    assert counter.current_package_units == 1


def test_three_good_units_emits_package_completed():
    counter = ProductionCounter()
    emitted_events = []

    for _ in range(3):
        emitted_events.extend(apply_production_rules(
            counter, {"result": "ok"}))

    assert emitted_events == [
        ProductionEvent.PACKAGE_STARTED, ProductionEvent.PACKAGE_COMPLETED]
    assert counter.good_units == 3
    assert counter.completed_packages == 1
    assert counter.current_package_units == 0


def test_rejected_units_increase_rejected_count():
    counter = ProductionCounter()
    emitted_events = apply_production_rules(
        counter, {"result": "reject"})

    assert emitted_events == []
    assert counter.rejected_units == 1


def test_production_target_reached_emits_event():
    counter = ProductionCounter(production_target_packages=2)
    emitted_events = []

    for _ in range(6):  # 6 good units = 2 completed packages
        emitted_events.extend(apply_production_rules(
            counter, {"result": "ok"}))

    assert ProductionEvent.PRODUCTION_TARGET_REACHED in emitted_events
    assert counter.completed_packages == 2


def test_scrap_threshold_exceeded_emits_event():
    counter = ProductionCounter(scrap_threshold=2)
    emitted_events = []

    for _ in range(2):  # 2 rejected units
        emitted_events.extend(apply_production_rules(
            counter, {"result": "reject"}))

    assert ProductionEvent.SCRAP_THRESHOLD_EXCEEDED in emitted_events
    assert counter.rejected_units == 2
