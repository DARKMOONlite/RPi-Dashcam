import time, os, sys
import numpy as np
from numpy import array
import cv2 as cv
from dashcam.src.camera_intrinsics import intrinsic_matrix



class calibration:
    def __init__(self, destination:str=None):
        self.destination = destination
        self.camera_intrinsics = None
        self.camera_calibration()
        pass
    

#! TODO finish this function once other stuff is working corectly
    
    def camera_calibration(self):
        print("to complete camera callibration, please follow the guide in the readme file \n press enter to continue, or anything else to exit")
        confirmation = input()
        print("confirmation received: '{0}'".format(confirmation))
        if(confirmation != ""): 
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

        objp = np.zeros((chessboard_size[0]*chessboard_size[1], 3), np.float32)
        objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)  # x,y coordinates
        
        image_points = []

        while(callibration_count > 0):
            print("press enter to take a picture")
            confirmation = input()
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
