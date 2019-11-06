import cv2


class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')
        # self.eye_cascade = cv2.CascadeClassifier('../haarcascade_eye.xml')


    def detect(self, img0, filename):
        gray0 = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)

        faces0 = self.face_cascade.detectMultiScale(gray0, 1.3, 5)

        roi_color0 = None
        for (x0, y0, w0, h0) in faces0:
            roi_color0 = img0[y0 - 25:y0 + h0 + 25, x0 - 25:x0 + w0 + 25]

        if roi_color0 is not None:
            img_name = "../data/faces/{}".format(filename)
            cv2.imwrite(img_name, roi_color0)

