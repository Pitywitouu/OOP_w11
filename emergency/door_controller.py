class DoorController:
    def __init__(self) -> None:
        self._is_unlocked: bool = False

    @property
    def is_unlocked(self) -> bool:
        return self._is_unlocked

    def unlock(self) -> None:
        self._is_unlocked = True
        print("[DOOR CONTROLLER] Tất cả các cửa thoát hiểm đã MỞ KHÓA tự động để sơ tán!")

    def lock(self) -> None:
        self._is_unlocked = False
        print("[DOOR CONTROLLER] Các cửa phòng máy đã được KHÓA lại.")