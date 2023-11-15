
#!/usr/bin/python
# -----------------------------------------------------------------------------
# Name:        camDetector.py
#
# Purpose:
#
# Author:      Yuancheng Liu
#
# Version:     v_0.1
# Created:     2023/09/21
# Copyright:   Copyright (c) 2023 LiuYuancheng
# License:     MIT License
# -----------------------------------------------------------------------------

import cv2
import time

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class camDetector(object):

    def __init__(self, camIdx=0, showUI=False, imgInt=None, imgSize=(640, 480)) -> None:
        self.camIdx = camIdx
        self.showUI = showUI
        self.imgInt = imgInt
        self.imgSize = imgSize
        self.windowName = 'Cam:%s' % str(self.camIdx)
        try:
            self.cap = cv2.VideoCapture(camIdx)
            self.cap.set(3, self.imgSize[0])
            self.cap.set(4, self.imgSize[1])
        except Exception as err:
            print("Error to open the camera. error info: %s" %str(err))
            return None
        self.cvDetector = None 
        self._initCvDetector()
        self.terminate = False

    def _initCvDetector(self):
        return None

    def setDisplayInfo(self, displayFlg, windowName):
        self.showUI = displayFlg
        self.windowName = windowName

    def setDisplayInterval(self, interval):
        self.imgInt = interval

    def run(self):
        while not self.terminate:
            success, img = self.cap.read()
            if success:
                img = self.processImg(img)
                if self.showUI:
                    cv2.imshow(self.windowName, img)
            else:
                print("Error: capture image from camera failed.")
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            time.sleep(self.imgInt)

    def processImg(self, img):
        return img

    def stop(self):
        self.terminate = True


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class faceDetector(object):

    def __init__(self, parent, frameInterval=None,  detectEye=False, imageSize=(640, 480)) -> None:
        self.parent = parent
        self.detectEye = detectEye
        self.framInterval = frameInterval
        print("Start to try to open the device camera.")
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, imageSize[0])
        self.cap.set(4, imageSize[1])
        self.faceDetResult = [0]*10
        # import cascade file for facial recognition
        self.faceCascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        if self.detectEye:
            # if you want to detect any object for example eyes, use one more layer of classifier as below:
            self.eyeCascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml")
        self.terminate = False

        connHandler = connectionHandler(self)
        connHandler.start()

    # -----------------------------------------------------------------------------
    def run(self):
        while not self.terminate:
            # print("start")
            success, img = self.cap.read()
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Getting corners around the face
            # 1.3 = scale factor, 5 = minimum neighbor
            faces = self.faceCascade.detectMultiScale(imgGray, 1.3, 5)
            # drawing bounding box around face
            self.faceDetResult.pop(0)

            for (x, y, w, h) in faces:
                img = cv2.rectangle(
                    img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if len(faces) > 0:
                self.faceDetResult.append(1)
            else:
                self.faceDetResult.append(0)

            if self.detectEye:
                # detecting eyes
                eyes = self.eyeCascade.detectMultiScale(imgGray)
                # drawing bounding box for eyes
                for (ex, ey, ew, eh) in eyes:
                    img = cv2.rectangle(
                        img, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)

            cv2.imshow('face_detect', img)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            time.sleep(self.framInterval)
            # self.getDetectionResult()

    # -----------------------------------------------------------------------------
    def getDetectionResult(self):
        count = self.faceDetResult.count(1)
        return count > 7


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main(mode):
    if mode == 0:
        detector = camDetector(imgInt=0.1)
        detector. setDisplayInfo(True, "Camera")
        detector.run()

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main(0)