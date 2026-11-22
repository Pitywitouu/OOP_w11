from monitoring.alert_event import AlertEvent
from monitoring.alert_observer import IAlertObserver

class DashboardObserver(IAlertObserver):
    def update(self, alert_event: AlertEvent) -> None:
        print(
            f"[DASHBOARD] {alert_event.sensor_name}: "
            f"{alert_event.value:.1f}{alert_event.unit} "
            f"[{alert_event.severity}]"
        )