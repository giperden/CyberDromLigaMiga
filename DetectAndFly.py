from pioneer_sdk import Pioneer
from pioneer_sdk import Camera
import time
import numpy as np
import cv2
import cv2.aruco as aruco
from collections import defaultdict

# Порты для управления и видео
control_port = 8001
video_port = 18001

# Инициализация дрона с дополнительными параметрами для отладки
razvetBVS = Pioneer(
    ip="127.0.0.1",
    mavlink_port=control_port,
    logger=True,  # Включаем логирование
    start_message_handler_from_init=True,  # Автоматический старт обработчика сообщений
    checking_components=False  # Отключаем проверку компонентов для симулятора
)
razvetCamera = Camera(ip='127.0.0.1', port=18001, timeout=3)

def get_aruco_coordionates(drone: Pioneer, camera: Camera) -> dict[int: set[list[int, int]]]:
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
    params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(aruco_dict, params)
    coordinates = defaultdict(set)
    try:
        frame = camera.get_cv_frame()
        height, width, _ = frame.shape
        size = (width, height)
        corners, ids, _ = detector.detectMarkers(frame)
        for index, id in enumerate(ids):
            if id not in [0, 1]:
                continue
            x_center = int(
                (
                    corners[index][0][0][0]
                    + corners[index][0][1][0]
                    + corners[index][0][2][0]
                    + corners[index][0][3][0]
                )
            ) // 4
            y_center = int(
                (
                    corners[index][0][0][1]
                    + corners[index][0][1][1]
                    + corners[index][0][2][1]
                    + corners[index][0][3][1]
                )
            ) // 4
        
        coefficient = 0.2 / (((corners[index][0][0][0] - corners[index][0][1][0]) ** 2 + (corners[index][0][0][1] - corners[index][0][1][1]) ** 2) ** 0.5)
        local_coordinates = (
                 (x_center - size[0] // 2) * coefficient,
                 (y_center - size[1] // 2) * coefficient
            )
        while (drone_coordinates := drone.get_local_position_lps()) is None:
            continue
        global_coordinates = (
            drone_coordinates[0] + local_coordinates[0],
            drone_coordinates[1] + local_coordinates[1]
        )
        coordinates[id].add(global_coordinates)
    except cv2.error:
        pass
    return coordinates