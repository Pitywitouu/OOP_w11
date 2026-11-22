class Alarm:
    def __init__(self) -> None:
        self._is_active: bool = False

    @property
    def is_active(self) -> bool:
        return self._is_active

    def activate(self) -> None:
        self._is_active = True
        print("[ALARM] Còi báo động hú và đèn cảnh báo chớp ĐÃ KÍCH HOẠT!")

    def deactivate(self) -> None:
        self._is_active = False
        print("[ALARM] Còi báo động và đèn cảnh báo đã TẮT.")