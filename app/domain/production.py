from dataclasses import dataclass


@dataclass(slots=True)
class ProductionCounter:
    units_per_package: int = 3
    production_target_packages: int = 10
    scrap_threshold: int = 5
    current_package_units: int = 0
    completed_packages: int = 0
    good_units: int = 0
    rejected_units: int = 0
    target_reached_emitted: bool = False
    scrap_threshold_emitted: bool = False

    def register_good_unit(self) -> bool:
        self.good_units += 1
        self.current_package_units += 1

        if self.current_package_units == self.units_per_package:
            self.completed_packages += 1
            self.current_package_units = 0
            return True

        return False

    def register_rejected_unit(self) -> None:
        self.rejected_units += 1

    def should_emit_target_reached(self) -> bool:
        # Ensure the event is emitted only once when the target is reached
        if not self.target_reached_emitted and self.completed_packages >= self.production_target_packages:
            self.target_reached_emitted = True
            return True
        return False

    def should_emit_scrap_threshold_exceeded(self) -> bool:
        # Ensure the event is emitted only once when the scrap threshold is exceeded
        if not self.scrap_threshold_emitted and self.rejected_units >= self.scrap_threshold:
            self.scrap_threshold_emitted = True
            return True
        return False
