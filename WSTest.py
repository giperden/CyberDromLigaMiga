import cv2
import numpy as np
from pioneer_sdk import Camera
from pioneer_sdk import Pioneer
import asyncio
from multiprocessing.managers import BaseManager
import multiprocessing as mp
import random as rd
import time
# Connect to the drone camera

pioner = Pioneer(ip='127.0.0.1', mavlink_port=8001)
camera = Camera(ip='127.0.0.1', port=18001, timeout=0.5)

def getVid():
    camera.connect()
    while True:
        raw_frame = camera.get_frame()  # Get raw data
        #print('===============', raw_frame)
        try:
            # Decode data to get image
            # print(len(raw_frame))
            frame = cv2.imdecode(
                np.frombuffer(raw_frame, dtype=np.uint8), cv2.IMREAD_COLOR
            )
            cv2.imshow("video", frame)  # Show an image on the screen
        except Exception: print('Error')
        

        if cv2.waitKey(1) == 27:  # Exit if the ESC key is pressed
            break
    cv2.destroyAllWindows() 


def move():
    pioner.arm()
    pioner.takeoff()
    print(pioner.connected())
    while True:
        pioner.go_to_local_point(x=rd.random() * 10 % 2, y=0, z=rd.random() * 10 % 2, yaw=rd.random() * 10 % 2)
        time.sleep(5)
    # pioner.land()
    # pioner.disarm()

async def go():
    await asyncio.gather(getVid, move)

if __name__ == "__main__":
    BaseManager.register('Pioneer', Pioneer)
    manager = BaseManager()
    manager.start()
    video = mp.Process(target=getVid)
    drone_flight = mp.Process(target=move)
    video.start()
    drone_flight.start()


    
    
    
