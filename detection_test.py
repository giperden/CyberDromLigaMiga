import cv2
import numpy as np
from pioneer_sdk import Pioneer, Camera
from collections import defaultdict


def get_aruco_coordionates(drone: Pioneer, camera: Camera) -> dict[int: set[list[int, int]]]:
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
    params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(aruco_dict, params)
    coordinates = defaultdict(set)
    try:
        frame = camera.get_cv_frame()
        height, width, _ = frame.shape
        size = (width, height)
        bnw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = detector.detectMarkers(bnw)
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


def get_qr_coordionates(drone: Pioneer, camera: Camera) -> dict[int: set[list[int, int]]]:
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
    params = cv2.aruco.DetectorParameters()
    qcd = cv2.QRCodeDetector()
    coordinates = defaultdict(set)
    try:
        frame = camera.get_cv_frame()
        height, width, _ = frame.shape
        size = (width, height)
        bnw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        retval, decoded_info, points, _ = qcd.detectAndDecodeMulti(bnw)
        for index, info in enumerate(decoded_info):
            info = ''
            if not (info.startswith('Box') or info.startswith('Wood') or info.startswith('Stone')):
                continue
            x_center = int(
                (
                    points[index][0][0][0]
                    + points[index][0][1][0]
                    + points[index][0][2][0]
                    + points[index][0][3][0]
                )
            ) // 4
            y_center = int(
                (
                    points[index][0][0][1]
                    + points[index][0][1][1]
                    + points[index][0][2][1]
                    + points[index][0][3][1]
                )
            ) // 4
        
        coefficient = 0.2 / (((points[index][0][0][0] - points[index][0][1][0]) ** 2 + (points[index][0][0][1] - points[index][0][1][1]) ** 2) ** 0.5)
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