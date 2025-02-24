import cv2
import numpy as np
from pioneer_sdk import Camera
from pioneer_sdk import Pioneer
import asyncio

# Connect to the drone camera

pioner = Pioneer(ip='127.0.0.1', mavlink_port=8001)
camera = Camera(ip='127.0.0.1', port=18001, timeout=3)

def getVid():
    while True:
        raw_frame = camera.get_frame()  # Get raw data
        if raw_frame is not None:
            # Decode data to get image
            frame = cv2.imdecode(
                np.frombuffer(raw_frame, dtype=np.uint8), cv2.IMREAD_COLOR
            )
        cv2.imshow("video", frame)  # Show an image on the screen

        if cv2.waitKey(1) == 27:  # Exit if the ESC key is pressed
            break
    cv2.destroyAllWindows() 

def move():
    print(pioner.connected())
    pioner.arm()
    pioner.takeoff()
    pioner.go_to_local_point(x=0, y=0, z=3, yaw=3)
    pioner.land()
    pioner.disarm()



if __name__ == "__main__":
    pioner.arm()
    getVid()
    print(pioner.connected())

    pioner.takeoff()
    pioner.go_to_local_point(x=0, y=0, z=3, yaw=3)
    pioner.land()
    pioner.disarm()