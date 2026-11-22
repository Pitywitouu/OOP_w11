"""
MSSV: 202418985
Họ tên: Nguyễn Phú Thái
"""

from emergency.alarm import Alarm
from emergency.door_controller import DoorController
from emergency.emergency_mediator import EmergencyMediator
from emergency.vertilation_controller import VentilationController
from monitoring.alert_observer import IAlertObserver
from monitoring.alert_event import AlertEvent
from monitoring.sensor_monitor import SensorMonitor
from observers.audit_log_observer import AuditLogObserver
from observers.dashboard_observer import DashboardObserver
from observers.email_alert_observer import EmailAlertObserver
from observers.emergency_bridge_observer import EmergencyBridgeObserver
from sensors.isensor import ISensor
from sensors.legacy_smoke_detector import LegacySmokeDetector
from sensors.smoke_sensor_adapter import SmokeSensorAdapter

def print_separator(title: str = "") -> None:
    print("\n")
    if title:
        print(f" {title.upper()} ")

def main() -> None:
    print_separator("        KHỞI TẠO HỆ THỐNG CAMPUS SAFETY HUB")

    # 1. Khởi tạo thiết bị cũ và Adapter (Adapter Pattern)
    legacy_detector = LegacySmokeDetector(smoke_level=0)
    adapted_smoke_sensor: ISensor = SmokeSensorAdapter(legacy_detector)

    print(f"Khởi tạo thiết bị: {legacy_detector.get_description()}")
    print(f"Đơn vị đo chuẩn hóa: {adapted_smoke_sensor.get_unit()}")

    # 2. Khởi tạo hệ thống thiết bị khẩn cấp và Mediator (Mediator Pattern)
    alarm = Alarm()
    door_controller = DoorController()
    ventilation = VentilationController()
    mediator = EmergencyMediator(alarm, door_controller, ventilation)

    # 3. Khởi tạo SensorMonitor và các Observers (Observer Pattern)
    monitor = SensorMonitor()

    dashboard_obs = DashboardObserver()
    email_obs = EmailAlertObserver("admin-server-room@campus.edu")
    audit_obs = AuditLogObserver()
    bridge_obs = EmergencyBridgeObserver(mediator)

    monitor.attach(dashboard_obs)
    monitor.attach(email_obs)
    monitor.attach(audit_obs)
    monitor.attach(bridge_obs)

    # 4. Kịch bản 1: Mức khói bình thường (< 50%)
    # Giả sử thiết bị cũ đọc mức 350 -> tương đương 35.0%
    print_separator("KỊCH BẢN 1: MỨC KHÓI DƯỚI 50% (BÌNH THƯỜNG)")
    legacy_detector.set_smoke_level(350)
    print(f"Cảm biến đo mức cũ: {legacy_detector.get_smoke_level()} -> Chuyển đổi: {adapted_smoke_sensor.read_value()}{adapted_smoke_sensor.get_unit()}")
    print("Kiểm tra cảm biến qua SensorMonitor...")
    monitor.check_sensor("Cảm biến Khói Phòng Máy A", adapted_smoke_sensor)
    print("=> Kết quả: Không có cảnh báo nào được phát ra (Hệ thống an toàn).")

    # 5. Kịch bản 2: Mức khói ở mức cảnh báo WARNING (50% <= khói < 70%)
    # Giả sử thiết bị cũ đọc mức 620 -> tương đương 62.0%
    print_separator("KỊCH BẢN 2: MỨC KHÓI TỪ 50% ĐẾN DƯỚI 70% (WARNING)")
    legacy_detector.set_smoke_level(620)
    print(f"Cảm biến đo mức cũ: {legacy_detector.get_smoke_level()} -> Chuyển đổi: {adapted_smoke_sensor.read_value()}{adapted_smoke_sensor.get_unit()}")
    print("Kiểm tra cảm biến qua SensorMonitor...")
    monitor.check_sensor("Cảm biến Khói Phòng Máy A", adapted_smoke_sensor)

    # 6. Kịch bản 3: Mức khói ở mức nguy hiểm CRITICAL (>= 70%) - Kích hoạt phản ứng khẩn cấp
    # Thử nghiệm với giá trị 735 như trong tài liệu hướng dẫn (735 -> 73.5%)
    print_separator("KỊCH BẢN 3: MỨC KHÓI TỪ 70% TRỞ LÊN (CRITICAL)")
    legacy_detector.set_smoke_level(735)
    print(f"Cảm biến đo mức cũ: {legacy_detector.get_smoke_level()} -> Chuyển đổi: {adapted_smoke_sensor.read_value()}{adapted_smoke_sensor.get_unit()}")
    print("Kiểm tra cảm biến qua SensorMonitor...")
    monitor.check_sensor("Cảm biến Khói Phòng Máy A", adapted_smoke_sensor)

    # 7. Thử nghiệm tính năng quản lý Observer linh hoạt (Detach observer)
    print_separator("THỬ NGHIỆM: HỦY ĐĂNG KÝ (DETACH) EMAIL OBSERVER")
    print("Hủy đăng ký EmailAlertObserver để không nhận email nữa...")
    monitor.detach(email_obs)

    # Đặt mức 850 (85.0% - CRITICAL) và kiểm tra lại
    legacy_detector.set_smoke_level(850)
    print(f"Cảm biến đo mức cũ: {legacy_detector.get_smoke_level()} -> Chuyển đổi: {adapted_smoke_sensor.read_value()}{adapted_smoke_sensor.get_unit()}")
    monitor.check_sensor("Cảm biến Khói Phòng Máy A", adapted_smoke_sensor)

    # 8. Thử nghiệm khả năng chống lỗi (Fault Tolerance) của Observer
    print_separator("THỬ NGHIỆM: KHẢ NĂNG CÔ LẬP LỖI CỦA OBSERVER")

    class FaultyObserver(IAlertObserver):
        def update(self, alert_event: AlertEvent) -> None:
            raise RuntimeError("Lỗi mạng khi kết nối hệ thống SMS bên ngoài!")

    faulty_obs = FaultyObserver()
    monitor.attach(faulty_obs)
    print("Đã gắn thêm một Observer lỗi (FaultyObserver). Kiểm tra phát cảnh báo:")
    legacy_detector.set_smoke_level(750)
    monitor.check_sensor("Cảm biến Khói Phòng Máy A", adapted_smoke_sensor)
    print("=> Dù FaultyObserver gặp lỗi, các Observer khác vẫn nhận cảnh báo bình thường.")

    # 9. Thử nghiệm All Clear từ Mediator
    print_separator("KHÔI PHỤC: SỰ KIỆN ALL_CLEAR TỪ MEDIATOR")
    mediator.notify(None, "ALL_CLEAR")

    print_separator("HOÀN THÀNH MÔ PHỎNG")

if __name__ == "__main__":
    main()
