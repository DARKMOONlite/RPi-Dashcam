
from picamera2 import Picamera2, Preview
# from picamera2.array import PiRGBArray
import time, os
import numpy as np
from numpy import array
import cv2 as cv
import msvcrt
class intrinsic_matrix:
    def __init__(self,fx,fy,cx,cy) -> None:
        self.focal_length = [fx,fy]
        self.principal_point = [cx,cy]
        self.matrix = array([[fx,0,cx],[0,fy,cy],[0,0,1]])
        pass


class app:
    

    def __init__(self, debug:bool=False, destination:str=None, camera_intrinsics:intrinsic_matrix=None):
        self.debug = debug
        self.destination = destination
        self.module_list=[]
        self.camera_intrinsics = camera_intrinsics




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


    def camera_calibration(self):
        print("to complete camera callibration, please follow the guide in the readme file \n press enter to continue, or anything else to exit")
        confirmation = msvcrt.getch().decode("utf-8")
        if(confirmation != "\r"): 
            return
        print("please enter the size of the chessboard square in mm")
        while True:
            try:
                size = float(input())
                break
            except ValueError:
                print("Invalid input. Please enter a number.")

        print("please enter the number of images to use for callibration (recommended 10)")
        while True:
            try:
                callibration_count = int(input())
                if(callibration_count < 1):
                    raise ValueError
                break
            except ValueError:
                print("Invalid input. Please enter an integer.")
        print("please enter the size of the chess board, number of squares, please enter two integer values separated by a space ")
        while True:
            try:
                chessboard_size = input().split()
                if(len(chessboard_size) != 2):
                    raise ValueError
                chessboard_size = (int(chessboard_size[0]),int(chessboard_size[1]))
                break
            except ValueError:
                print("Invalid input. Please enter two integers.")   

        objp = np.zeros((chessboard_size[1]*chessboard_size[2], 3), np.float32)
        objp[:, :2] = np.mgrid[0:chessboard_size[1], 0:chessboard_size[2]].T.reshape(-1, 2)  # x,y coordinates
        
        image_points = []

        while(callibration_count > 0):
            print("press enter to take a picture")
            confirmation = msvcrt.getch().decode("utf-8")
            if(confirmation == "\r"): 
                
                image = self.take_simple_photo()
                gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
                result, corner = cv.findChessboardCorners(gray, chessboard_size, None)
                if(result==True):
                    callibration_count -= 1
                    image_points.append(corner)
                    print("picture resolved, {0} remaining".format(callibration_count))
                else:
                    print("no chessboard found, please try again")
        
        ret, camera_matrix, dist, rvecs, tvecs = cv.calibrateCamera(objp, image_points, gray.shape[::-1], None, None)
        

        newcamera_matrix, roi = cv.getOptimalNewCameraMatrix(camera_matrix, dist, gray.shape[::-1], 1, gray.shape[::-1])
        dst = cv.undistort(gray, camera_matrix, dist, None, newcamera_matrix)


        # calculate re-projection error

        mean_error = 0
        for i in range(len(objp)):
            imgpoints2, _ = cv.projectPoints(objp[i], rvecs[i], tvecs[i], camera_matrix, dist)
            error = cv.norm(image_points[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
            mean_error += error
        print("total error: {}".format(mean_error / len(objp)))


    def take_simple_photo(self):
        with Picamera2() as camera:
            capture_array=camera.capture_array()
            return(capture_array)