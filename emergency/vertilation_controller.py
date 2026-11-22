class VentilationController:
    def __init__(self) -> None:
        self._is_running: bool = False

    @property
    def is_running(self) -> bool:
        return self._is_running

    def start(self) -> None:
        self._is_running = True
        print("[VENTILATION CONTROLLER] Quạt hút khói khẩn cấp đã KHỞI ĐỘNG công suất tối đa!")

    def stop(self) -> None:
        self._is_running = False
        print("[VENTILATION CONTROLLER] Quạt thông gió / hút khói đã DỪNG.")