from picamera2 import PiCamera
from numpy import array
import cv2 as cv
from dataclasses import dataclass
import time

@dataclass
class CameraSettings:
    camera_intrinsics:array
    frame_rate:int
    resolution:tuple


# https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf
class app:
    
    def __init__(self,debug:bool=False, destination:str=None, 
                camera_intrinsics:array=None,frame_rate:int=5, resolution:tuple=(640,480)
                ):
        self.debug = debug
        self.destination = destination
        self.camera_settings:CameraSettings = CameraSettings(camera_intrinsics,frame_rate,resolution)


    def run(self):
        with PiCamera() as camera:
            camera.resolution = self.camera_settings.resolution
            camera.framerate = self.camera_settings.frame_rate
            camera.start_preview()
            time.sleep(2)
            camera.capture('foo.jpg')
            camera.stop_preview()
            pass