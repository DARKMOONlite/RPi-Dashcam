
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder, Quality
from picamera2.array import PiRGBArray

import time, os, sys
import numpy as np
from numpy import array
import cv2 as cv
from dashcam.src.settings import Settings
from dashcam.src.camera_intrinsics import intrinsic_matrix




class app:
    

    def __init__(self, debug:bool=False, destination:str=None, 
                camera_id:int=0,
                load:bool=False, settings_file:str=None):
        self.debug = debug
        self.destination = destination
        self.module_list=[]
        self.id = camera_id
        
        if(load):
            self.stored_settings = Settings(settings_file)
            self.load(settings_file)

    
    def load(self):
        if(self.stored_settings is None):
            print('No settings file found')
            return
        else:
            self.camera_intrinsics = intrinsic_matrix(
                self.stored_settings.read_setting(f"{self.id}-focal_length-x"),
                self.stored_settings.read_setting(f"{self.id}-focal_length-y"),
                self.stored_settings.read_setting(f"{self.id}-principal_point-x"),
                self.stored_settings.read_setting(f"{self.id}-principal_point-y")
            )
            print('Loaded camera intrinsics from file')
            self.frame_rate = self.stored_settings.read_setting(f"{self.id}-frame_rate")
            self.stored_video = self.stored_settings.read_setting(f"{self.id}-stored_video")
            print("loaded general settings from {0}".format(self.stored_settings.settings_file))
            return
            



    def run(self):
        print('Running app in mode debug={0}, \n\tdesination={1},\n\t modules={2}'.format(
            self.debug, self.destination,self.module_list))
        
        if(self.camera_intrinsics is None):
            print('Camera intrinsics not set, please set them before running the app')
            return
        else:
            print('Camera intrinsics set to {0}'.format(self.camera_intrinsics.matrix))
        
        if(not os.path.exists(self.destination)):
            print('Destination folder does not exist, creating it')
            os.makedirs(self.destination)
        else:
            print('storing video in {0}'.format(self.destination))
        
        

    def set_camera_intrinsics(self, camera_intrinsics : intrinsic_matrix):
        self.camera_intrinsics = camera_intrinsics



    def take_simple_photo(self):
        with Picamera2() as camera:
            capture_array=camera.capture_array()
            return(capture_array)
        
    def take_simple_video(self, duration:int):
        with Picamera2() as camera:
            encoder = H264Encoder(bitrate=10000000)
            camera.start_recording(encoder,desination=self.destination,quality=Quality.Medium)
            time.sleep(duration)
            camera.stop_recording()
            return