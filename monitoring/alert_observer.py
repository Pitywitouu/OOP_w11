from abc import ABC, abstractmethod
from monitoring.alert_event import AlertEvent

class IAlertObserver(ABC):
    @abstractmethod
    def update(self, alert_event: AlertEvent) -> None:
        pass