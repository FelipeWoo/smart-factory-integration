
from app.domain.production import ProductionCounter
from app.utils.boot import boot
from app.utils.logger import logger

boot_config = boot("test_production_rules")


def test_logger():
    logger.info("Testing domain production rules.")


def test_three_good_units_complete_one_package():
    counter = ProductionCounter()

    assert counter.register_good_unit() is False
    assert counter.register_good_unit() is False
    assert counter.register_good_unit() is True

    assert counter.good_units == 3
    assert counter.completed_packages == 1
    assert counter.current_package_units == 0


def test_rejected_unit_does_not_advance_package():
    counter = ProductionCounter()

    counter.register_good_unit()
    counter.register_rejected_unit()

    assert counter.good_units == 1
    assert counter.rejected_units == 1
    assert counter.completed_packages == 0
    assert counter.current_package_units == 1


def test_partial_package_progress_is_preserved():
    counter = ProductionCounter()

    counter.register_good_unit()
    counter.register_good_unit()

    assert counter.current_package_units == 2
    assert counter.completed_packages == 0


def test_multiple_packages():
    counter = ProductionCounter()

    for _ in range(7):
        counter.register_good_unit()

    assert counter.good_units == 7
    assert counter.completed_packages == 2
    assert counter.current_package_units == 1
