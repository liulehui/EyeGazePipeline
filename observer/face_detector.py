import cv2


class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')
        # self.eye_cascade = cv2.CascadeClassifier('../haarcascade_eye.xml')

    def detect(self, img, filename):
        # gray0 = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("face", img0)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        face_flag = False
        faces = self.face_cascade.detectMultiScale(img, 1.3, 5)

        roi_color0 = None
        for (x0, y0, w0, h0) in faces:
            roi_color0 = img[y0 - 25:y0 + h0 + 25, x0 - 25:x0 + w0 + 25]

        if roi_color0 is not None:
            # img_name = "../data/faces/{}".format(filename)
            cv2.imwrite(filename, roi_color0)
            face_flag = True
        else:
            print("no face found.")

        return face_flag

