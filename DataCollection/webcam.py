import numpy as np
import cv2
import time
import datetime
from datetime import datetime, timedelta
from gazepoint import GazePoint

import multiprocessing
import os

class Webcam:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        # self.csv_filename = 'screenshot_list.csv'
        self.cap0 = cv2.VideoCapture(0)
        self.cap1 = cv2.VideoCapture(1)
        self.gaze_point_process = None
        self.face_cascade = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')
        self.face_dir0 = os.path.join(self.base_dir, 'face0')
        self.face_dir1 = os.path.join(self.base_dir, 'face1')

        if not os.path.exists(self.face_dir0):
            os.makedirs(self.face_dir0)

        if not os.path.exists(self.face_dir1):
            os.makedirs(self.face_dir1)

    def __del__(self):
        self.cap0.release()
        self.cap1.release()

    def detect(self, img, filename):
        faces = self.face_cascade.detectMultiScale(img, 1.3, 5)

        roi_color = None
        for (x, y, w, h) in faces:
            roi_color = img[y - 25:y + h + 25, x - 25:x + w + 25]

        if roi_color is not None:
            cv2.imwrite(filename, roi_color)
        else:
            print("no face founded!")

    def take_screenshot(self, total_time):
        # total_time= 60 * 4
        t_end = datetime.now() + timedelta(seconds=total_time)

        while datetime.now() < t_end:
            img_counter1 = time.time()
            ret1, img1 = self.cap1.read()
            
            img_counter0 = time.time()
            ret0, img0 = self.cap0.read()
            
            face_img1_path = self.face_dir1 + "/cam1_{}.png".format(img_counter1)
            face_img0_path = self.face_dir0 + "/cam0_{}.png".format(img_counter0)

            if img1 is not None:
                self.detect(img1, face_img1_path)

            if img0 is not None:
                self.detect(img0, face_img0_path)

            
    @staticmethod
    def run_gaze():
        HOST = '127.0.0.1'
        PORT = 4242
        base_dir = os.getcwd()

        eyegaze = GazePoint(HOST, PORT, base_dir)
        eyegaze.run_gazepoint()


if __name__ == '__main__':
    filepath = os.getcwd()
    webcam = Webcam(filepath)
    webcam.eyegaze_process = multiprocessing.Process(target=Webcam.run_gaze, args=())
    webcam.eyegaze_process.start()
    print(webcam.eyegaze_process.pid)

    total_time= 60 * 4
    webcam.take_screenshot(total_time)
     