from emergency.emergency_mediator import IEmergencyMediator
from monitoring.alert_event import AlertEvent
from monitoring.alert_observer import IAlertObserver

class EmergencyBridgeObserver(IAlertObserver):
    def __init__(self, mediator: IEmergencyMediator) -> None:
        if mediator is None:
            raise ValueError("IEmergencyMediator không được là None.")
        self._mediator: IEmergencyMediator = mediator

    def update(self, alert_event: AlertEvent) -> None:
        if alert_event.severity == "CRITICAL":
            print(
                f"[EMERGENCY BRIDGE] Phát hiện mức độ CRITICAL ({alert_event.value:.1f}{alert_event.unit}) "
                f"tại '{alert_event.sensor_name}'. Chuyển tiếp sự kiện FIRE_DETECTED đến EmergencyMediator..."
            )
            self._mediator.notify(self, "FIRE_DETECTED")
        else:
            print(
                f"[EMERGENCY BRIDGE] Cảnh báo '{alert_event.sensor_name}' đạt mức {alert_event.severity}. "
                f"Chưa đạt ngưỡng kích hoạt quy trình ứng phó khẩn cấp."
            )