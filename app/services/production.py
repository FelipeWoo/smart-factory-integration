from app.domain.events import ProductionEvent
from app.domain.production import ProductionCounter


def apply_production_rules(counter: ProductionCounter, payload: dict) -> list[ProductionEvent]:
    emitted_events: list[ProductionEvent] = []

    result = payload.get("result")

    if result == "ok":
        was_empty = counter.current_package_units == 0
        package_completed = counter.register_good_unit()

        if was_empty:
            emitted_events.append(ProductionEvent.PACKAGE_STARTED)

        if package_completed:
            emitted_events.append(ProductionEvent.PACKAGE_COMPLETED)

    elif result == "reject":
        counter.register_rejected_unit()

    if counter.should_emit_target_reached():
        emitted_events.append(ProductionEvent.PRODUCTION_TARGET_REACHED)

    if counter.should_emit_scrap_threshold_exceeded():
        emitted_events.append(ProductionEvent.SCRAP_THRESHOLD_EXCEEDED)

    return emitted_events
