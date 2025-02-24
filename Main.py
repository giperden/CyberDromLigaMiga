from pion import Pion
import time
import numpy as np
import cv2
import cv2.aruco as aruco

# Порты для управления и видео
control_port = 8001
video_port = 18001

# Инициализация дрона с дополнительными параметрами для отладки
drone = Pion(
    ip="127.0.0.1",
    mavlink_port=control_port,
    logger=True,  # Включаем логирование
    start_message_handler_from_init=True,  # Автоматический старт обработчика сообщений
    checking_components=False  # Отключаем проверку компонентов для симулятора
)