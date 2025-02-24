import time
import numpy as np
import cv2
import cv2.aruco as aruco
from pioneer_sdk import Pioneer  # SDK для работы с БВС

# Исходные данные
start_positions = {
    "scout_bvs": (-3.92, -2.14),
    "transport_bvs": (-3.92, -3.20),
}

hospitals = [(-0.88, -3.10), (0.56, 3.15)]
warehouses = [(1.8, 3.15), (3.50, -0.24)]
medicine = [(-0.88, -3.10), (0.56, 3.15)]

# Создание объектов с указанием хоста
scout_bvs = Pioneer(ip='127.0.0.1', mavlink_port=8003)
transport_bvs = Pioneer(ip='127.0.0.1', mavlink_port=8000)

# Функция для полёта дрона
def fly_to(drone, x, y, z=2, yaw=0):
    print(f"[{drone.__class__.__name__}] Летим в ({x}, {y}, {z})")
    while not scout_bvs.point_reached():
        drone.go_to_local_point(x=x, y=y, z=z, yaw=0)
        time.sleep(0.5)  # Ожидание для достижения точки

# Функция взлёта дрона
def takeoff(drone):
    print(f"[{drone.__class__.__name__}] Взлёт...")
    drone.arm()
    drone.takeoff()
    time.sleep(5)  # Ожидание завершения взлёта

# Функция посадки дрона
def land(drone):
    print(f"[{drone.__class__.__name__}] Посадка...")
    drone.land()
    drone.disarm()
    time.sleep(5)  # Ожидание завершения посадки

# Функция распознавания QR-кодов
# def recognize_qr_code(image):
#     detector = cv2.QRCodeDetector()
#     data, _, _ = detector.detectAndDecode(image)
#     return data if data else None

# Функция распознавания ArUco-маркеров
# def recognize_aruco_markers(image):
#     aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
#     parameters = aruco.DetectorParameters()
#     detector = aruco.ArucoDetector(aruco_dict, parameters)
#     corners, ids, _ = detector.detectMarkers(image)
#     return ids if ids is not None else []

# Разведывательный БВС ищет объекты
def scout_mission():
    print("[Разведывательный БВС] Поиск объектов...")
    detected_objects = []
    
    x0 = start_positions["scout_bvs"][0]
    y0 = start_positions["scout_bvs"][1]
   
    for y in np.linspace(-5, 5, 5):
        for x in np.linspace(-5, 5, 5):
                fly_to(scout_bvs, x, y, z=3)
                # image = np.zeros((200, 200, 3), dtype=np.uint8)  # Заглушка
                # qr_data = recognize_qr_code(image)
                # aruco_data = recognize_aruco_markers(image)
                # if qr_data:
                #     print(f"[Разведывательный БВС] QR-код: {qr_data}")
                #     detected_objects.append((x, y, qr_data))
                # if aruco_data:
                #     print(f"[Разведывательный БВС] ArUco-маркер: {aruco_data}")               
    fly_to(scout_bvs, x0, y0, z=3)
    land(scout_bvs)

    return detected_objects 

# Транспортный БВС выполняет доставку
def transport_mission(detected_objects):
    for obj in detected_objects:
        x, y, qr_code = obj
        print(f"[Транспортный БВС] Забираем {qr_code} в ({x}, {y})")
        fly_to(transport_bvs, x, y, z=1)
        destination = hospitals[0] if "медикаменты" in qr_code else hospitals[1]
        print(f"[Транспортный БВС] Доставка {qr_code} в {destination}")
        fly_to(transport_bvs, destination[0], destination[1], z=1)

# Запуск миссий
print("🚀 Начало миссии")

# Взлёт разведывательного дрона
takeoff(scout_bvs)
scout_results = scout_mission()

# Взлёт транспортного дрона
takeoff(transport_bvs)
transport_mission(scout_results)
land(transport_bvs)

print("✅ Миссия завершена!")