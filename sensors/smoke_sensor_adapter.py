from sensors.isensor import ISensor
from sensors.legacy_smoke_detector import LegacySmokeDetector

class SmokeSensorAdapter(ISensor):
    def __init__(self, legacy: LegacySmokeDetector) -> None:
        if legacy is None:
            raise ValueError("LegacySmokeDetector không được để trống (None).")
        self._legacy: LegacySmokeDetector = legacy

    def read_value(self) -> float:
        return self._legacy.get_smoke_level() / 10.0

    def get_unit(self) -> str:
        return "% smoke"