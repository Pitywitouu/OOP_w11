from monitoring.alert_event import AlertEvent
from monitoring.alert_observer import IAlertObserver

class AuditLogObserver(IAlertObserver):
    def update(self, alert_event: AlertEvent) -> None:
        timestamp = alert_event.occurred_at.strftime("%Y-%m-%d %H:%M:%S")
        print(
            f"[AUDIT LOG] [{timestamp}] SENSOR={alert_event.sensor_name} | "
            f"VALUE={alert_event.value:.1f}{alert_event.unit} | "
            f"SEVERITY={alert_event.severity}"
        )