from abc import ABC, abstractmethod
from typing import Any, Optional

from emergency.alarm import Alarm
from emergency.door_controller import DoorController
from emergency.vertilation_controller import VentilationController
from monitoring.alert_event import AlertEvent

class IEmergencyMediator(ABC):
    @abstractmethod
    def notify(self, sender: Any, event: str) -> None:
        pass

    @abstractmethod
    def handle_alert(self, alert_event: AlertEvent) -> None:
        pass

class EmergencyMediator(IEmergencyMediator):
    def __init__(
        self,
        alarm: Optional[Alarm] = None,
        door_controller: Optional[DoorController] = None,
        ventilation_controller: Optional[VentilationController] = None
    ) -> None:
        self._alarm: Alarm = alarm if alarm is not None else Alarm()
        self._door_controller: DoorController = door_controller if door_controller is not None else DoorController()
        self._ventilation_controller: VentilationController = (
            ventilation_controller if ventilation_controller is not None else VentilationController()
        )

    @property
    def alarm(self) -> Alarm:
        return self._alarm

    @property
    def door_controller(self) -> DoorController:
        return self._door_controller

    @property
    def ventilation_controller(self) -> VentilationController:
        return self._ventilation_controller

    def notify(self, sender: Any, event: str) -> None:
        sender_name = sender.__class__.__name__ if sender else "Unknown"
        print(f"[EMERGENCY MEDIATOR] Nhận sự kiện '{event}' từ {sender_name}.")

        if event == "FIRE_DETECTED":
            print("[EMERGENCY MEDIATOR] ĐANG ĐIỀU PHỐI CÁC THIẾT BỊ ỨNG PHÓ KHẨN CẤP")
            self._alarm.activate()
            self._door_controller.unlock()
            self._ventilation_controller.start()
            print("[EMERGENCY MEDIATOR] ĐÃ HOÀN TẤT ĐIỀU PHỐI ỨNG PHÓ")
        elif event == "ALL_CLEAR":
            print("[EMERGENCY MEDIATOR] KHÔI PHỤC HỆ THỐNG VỀ TRẠNG THÁI AN TOÀN")
            self._alarm.deactivate()
            self._door_controller.lock()
            self._ventilation_controller.stop()
            print("[EMERGENCY MEDIATOR] ĐÃ KHÔI PHỤC HOÀN TẤT")
        else:
            print(f"[EMERGENCY MEDIATOR] Không có hành động cấu hình cho sự kiện: {event}")

    def handle_alert(self, alert_event: AlertEvent) -> None:
        if alert_event.severity == "CRITICAL":
            self.notify(self, "FIRE_DETECTED")