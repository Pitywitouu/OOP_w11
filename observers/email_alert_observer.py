from monitoring.alert_event import AlertEvent
from monitoring.alert_observer import IAlertObserver

class EmailAlertObserver(IAlertObserver):
    def __init__(self, recipient: str = "safety-team@campus.edu") -> None:
        self._recipient: str = recipient

    def update(self, alert_event: AlertEvent) -> None:
        time_str = alert_event.occurred_at.strftime("%H:%M:%S")
        print(
            f"[EMAIL] Đã gửi thông báo tới {self._recipient}: "
            f"Cảm biến '{alert_event.sensor_name}' phát hiện mức {alert_event.severity} "
            f"({alert_event.value:.1f}{alert_event.unit}) vào lúc {time_str}."
        )