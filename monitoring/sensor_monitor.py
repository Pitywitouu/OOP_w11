from datetime import datetime
from typing import List, Optional

from monitoring.alert_event import AlertEvent
from monitoring.alert_observer import IAlertObserver
from sensors.isensor import ISensor

class SensorMonitor:
    def __init__(self) -> None:
        self._observers: List[IAlertObserver] = []

    def attach(self, observer: IAlertObserver) -> None:
        if observer is None:
            raise ValueError("Observer không được là None.")
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: IAlertObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def check_sensor(self, sensor_name: str, sensor: ISensor) -> None:
        value: float = sensor.read_value()

        severity: Optional[str] = None
        if value >= 70.0:
            severity = "CRITICAL"
        elif value >= 50.0:
            severity = "WARNING"

        if severity is None:
            return

        alert_event = AlertEvent(
            sensor_name=sensor_name,
            value=value,
            unit=sensor.get_unit(),
            severity=severity,
            occurred_at=datetime.now()
        )

        self._notify(alert_event)

    def _notify(self, alert_event: AlertEvent) -> None:
        for observer in list(self._observers):
            try:
                observer.update(alert_event)
            except Exception as ex:
                print(f"[ERROR] Observer '{observer.__class__.__name__}' gặp lỗi khi xử lý cảnh báo: {ex}")