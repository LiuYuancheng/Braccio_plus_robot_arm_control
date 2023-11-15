
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
        self.imgInt = 0 if imgInt is None else imgInt 
        self.imgSize = imgSize
        self.windowName = 'Cam:%s' % str(self.camIdx)
        try:
            print("Start to try to open the device camera.")
            self.cap = cv2.VideoCapture(camIdx)
            self.cap.set(3, self.imgSize[0])
            self.cap.set(4, self.imgSize[1])
        except Exception as err:
            print("Error to open the camera. error info: %s" % str(err))
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
class faceDetector(camDetector):

    def __init__(self, camIdx=0, showUI=False, imgInt=None, imgSize=(640, 480), detectEye=False) -> None:
        self.detectEye = detectEye
        self.faceDetResult = [False]*10
        super().__init__(camIdx, showUI, imgInt, imgSize)
        
    def _initCvDetector(self):
        # import cascade file for facial recognition
        self.faceCascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        if self.detectEye:
            self.eyeCascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml")

    def _archiveDetectRst(self, rst):
        self.faceDetResult.pop(0)
        self.faceDetResult.append(int(rst)>0)

    def processImg(self, img):
        # Getting corners around the face
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 1.3 = scale factor, 5 = minimum neighbor
        faces = self.faceCascade.detectMultiScale(imgGray, 1.3, 5)
        # drawing bounding box around face
        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        self._archiveDetectRst(len(faces))
        if self.detectEye:
            # detecting eyes
            eyes = self.eyeCascade.detectMultiScale(imgGray)
            # drawing bounding box for eyes
            for (ex, ey, ew, eh) in eyes:
                img = cv2.rectangle(img, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)
        return img

    # -----------------------------------------------------------------------------
    def getDetectionResult(self, threshold=7):
        count = self.faceDetResult.count(True)
        return count > threshold


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class qrcdDetector(camDetector):
    
    def __init__(self, camIdx=0, showUI=False, imgInt=None, imgSize=(1600, 900), decodeFlg=False) -> None:
        self.decodeFlg = decodeFlg
        self.detectResult = [False]*10
        self.decodeInfo = None
        super().__init__(camIdx, showUI, imgInt, imgSize)

    def _initCvDetector(self):
        self.qcd = cv2.QRCodeDetector()

    def processImg(self, img):
        # Getting corners around the face
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if self.decodeFlg:
            ret_qr, decoded_info, points, _ = self.qcd.detectAndDecodeMulti(imgGray)
            if ret_qr:
                for s, p in zip(decoded_info, points):
                    if s:
                        print(s)
                        color = (0, 255, 0)
                    else:
                        color = (0, 0, 255)
                    img = cv2.polylines(img, [p.astype(int)], True, color, 8)
            return img
        else:
            ret_qr, points = self.qcd.detectMulti(imgGray)
            if ret_qr:
                print(points)
                color = (0, 0, 255)
                if not points is None:
                    for point in points:
                        img = cv2.polylines(img, [point.astype(int)], True, color, 8)
            return img


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main(mode):
    if mode == 0:
        detector = camDetector(imgInt=0.1)
        detector.setDisplayInfo(True, "Camera")
        detector.run()
    elif mode == 1:
        detector = faceDetector(showUI=True, detectEye=True)
        detector.run()
    else:
        detector = qrcdDetector(showUI=True)
        detector.run()


#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main(2)
