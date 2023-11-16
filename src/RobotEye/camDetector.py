
#!/usr/bin/python
# -----------------------------------------------------------------------------
# Name:        camDetector.py
#
# Purpose:     This module will open the camera to capture the video (pic) the 
#              use openCV to detect different items (such as face, qr code). All
#              the detector class are inheritted from the parent class <camDetector>   
#
# Author:      Yuancheng Liu
#
# Version:     v_0.1
# Created:     2023/11/15
# Copyright:   Copyright (c) 2023 LiuYuancheng
# License:     MIT License
# -----------------------------------------------------------------------------

import cv2
import time
from statistics import mean 

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class camDetector(object):
    """ Parent detector class open the camera and capture the picture."""

    def __init__(self, camIdx=0, showUI=False, imgInt=0.01, imgSize=(640, 480)) -> None:
        """ Init example: detector = camDetector(camIdx=1, imgInt=0.1)
            Args:
                camIdx (int, optional): Camera index. Defaults to 0.
                showUI (bool, optional): Whether show the cv2's result window. Defaults to False.
                imgInt (_type_, optional): Camera image capture interval. Defaults to 0.01
                imgSize (tuple, optional): Image resolution. Defaults to (640, 480).
        """
        self.camIdx = camIdx
        self.showUI = showUI
        self.imgInt = imgInt
        self.imgSize = imgSize
        self.windowName = 'Cam:%s' % str(self.camIdx)
        try:
            print("Start to open the device camera...")
            self.cap = cv2.VideoCapture(camIdx, cv2.CAP_DSHOW)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.imgSize[0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.imgSize[1])
        except Exception as err:
            print("Error to open the camera. error info: %s" % str(err))
            return None
        print("- Camera ready.")
        self.cvDetector = None
        self._initCvDetector()
        self.terminate = False
        print("Detector init finished.")

    # -----------------------------------------------------------------------------
    def _initCvDetector(self):
        """ Init different item detector here, this function will be over overwritten
            by sub-classes.  
        """
        return None

    def _processImg(self, img):
        """ function to process the input cv.img. Return the processed cv.img."""
        return img

    # -----------------------------------------------------------------------------
    def run(self):
        """ Main loop to capture and 
        """
        while not self.terminate:
            success, img = self.cap.read()
            if success:
                img = self._processImg(img)
                if self.showUI: cv2.imshow(self.windowName, img)
            else:
                print("Error: capture image from camera failed.")
            if cv2.waitKey(10) & 0xFF == ord('q'): self.stop()
            time.sleep(self.imgInt)

    # -----------------------------------------------------------------------------
    def setDisplayInfo(self, displayFlg, windowName):
        """ Set whether show the cv result window and the window name.
            Args:
                displayFlg (bool): flag to identify whether show the cv2 window. set to 
                    None will not change the orignal setting.
                windowName (str): Window title name. Set to Noe will not change the 
                    orignal setting.
        """
        if not displayFlg is None: self.showUI = displayFlg
        if not windowName is None : self.windowName = str(windowName) 

    # -----------------------------------------------------------------------------
    def setCapInterval(self, interval):
        self.imgInt = float(interval)

    # -----------------------------------------------------------------------------
    def stop(self):
        self.terminate = True
        cv2.destroyWindow(self.windowName)

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class faceDetector(camDetector):
    """ Detect multiple faces with/without eyes. """

    def __init__(self, camIdx=0, showUI=False, imgInt=0.01, imgSize=(640, 480), detectEye=False) -> None:
        """ Args:
                camIdx, showUI, imgInt, imgSize : refer to parent class <camDetector>
                detectEye (bool, optional): flag to identify whehter detect 
                    human's eyes. Defaults to False.
        """
        self.detectEye = detectEye
        self.faceDetResult = [False]*10 # last 10 frame detection result record.
        self.lastFcPosList = None   # last faces detected position.
        super().__init__(camIdx, showUI, imgInt, imgSize)
        
    # -----------------------------------------------------------------------------
    def _initCvDetector(self):
        """ Init the face and the eyes detectors."""
        # import cascade file for facial recognition
        self.faceCascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        # import cascade file for eyes recognition
        if self.detectEye:
            self.eyeCascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml")

    # -----------------------------------------------------------------------------
    def _archiveDetectRst(self, rst):
        if rst is None: return
        self.faceDetResult.pop(0)
        self.faceDetResult.append(int(len(rst))>0)
        self.lastFcPosList = rst

    # -----------------------------------------------------------------------------
    def _processImg(self, img):
        # Getting corners around the face
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 1.3 = scale factor, 5 = minimum neighbor
        faces = self.faceCascade.detectMultiScale(imgGray, 1.3, 5)
        # drawing bounding box around face
        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        self._archiveDetectRst(faces)
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

    # -----------------------------------------------------------------------------
    def getLastDectPos(self):
        return self.lastFcPosList

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class qrcdDetector(camDetector):
    """Detect multiple QR code in thte camerea. """
    def __init__(self, camIdx=0, showUI=False, imgInt=0.01, imgSize=(1200, 800), decodeFlg=False) -> None:
        """ Args:
                camIdx, showUI, imgInt, imgSize : refer to parent class <camDetector>
                imgSize (tuple, optional): _description_. Defaults to (1200, 800).
                decodeFlg (bool, optional): flag to identify whether decode qr code information. Defaults to False.
        """
        self.decodeFlg = decodeFlg
        self.detectResult = [False]*10
        self.decodeInfo = None
        self.lastCDPos = None   # last QR code detected position.
        self.lastQRCentPos = None
        super().__init__(camIdx, showUI, imgInt, imgSize)

    def _initCvDetector(self):
        self.qcd = cv2.QRCodeDetector()

    def _archiveDetectRst(self, rst):
        if rst is None: return
        self.detectResult.pop(0)
        self.detectResult.append(int(len(rst))>0)

    # -----------------------------------------------------------------------------
    def _processImg(self, img):
        # Getting corners around the face
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.line(img, (self.imgSize[0]//2-10, self.imgSize[1]//2), 
                       (self.imgSize[0]//2+10, self.imgSize[1]//2), (255, 0, 0), 3) 
        img = cv2.line(img, (self.imgSize[0]//2, self.imgSize[1]//2-10), 
                       (self.imgSize[0]//2, self.imgSize[1]//2+10), (255, 0, 0), 3) 
        if self.decodeFlg:
            ret_qr, decoded_info, points, _ = self.qcd.detectAndDecodeMulti(imgGray)
            if ret_qr:
                for s, p in zip(decoded_info, points):
                    color = (0, 255, 0) if s else (0, 0, 255)
                    self.lastCDPos = [p.astype(int)]
                    self.decodeInfo = s
                    xAvg, yAvg = self.getQRcodeCentPo()
                    img = cv2.line(img, (5, yAvg), (self.imgSize[0]-5, yAvg), color, 2) 
                    img = cv2.line(img, (xAvg, 5), (xAvg, self.imgSize[1]-5), color, 2)
                    img = cv2.polylines(img, self.lastCDPos, True, color, 3)
            self._archiveDetectRst(points)
            return img
        else:
            ret_qr, points = self.qcd.detectMulti(imgGray)
            if ret_qr:
                #print(points)
                color = (0, 0, 255)
                if not points is None:
                    for point in points:
                        self.lastCDPos = [point.astype(int)]
                        xAvg, yAvg = self.getQRcodeCentPo()
                        img = cv2.putText(img, str(
                            (xAvg, yAvg)), (xAvg, yAvg), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
                        img = cv2.line(img, (5, yAvg), (self.imgSize[0]-5, yAvg), color, 2) 
                        img = cv2.line(img, (xAvg, 5), (xAvg, self.imgSize[1]-5), color, 2)
                        img = cv2.polylines(img, self.lastCDPos, True, color, 3)
            self._archiveDetectRst(points)
            return img

    # -----------------------------------------------------------------------------
    def getDetectionResult(self, threshold=7):
        count = self.detectResult.count(True)
        return count > threshold

    def getQRcodeData(self):
        return self.decodeInfo

    def getQRCodePos(self):
        return self.lastCDPos
    
    def getQRcodeCentPo(self):
        xAvg = int(mean([int(pt[0]) for pt in self.lastCDPos[0]]))
        yAvg = int(mean([int(pt[1]) for pt in self.lastCDPos[0]]))
        return(xAvg, yAvg)

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
        detector = qrcdDetector(imgInt=1, showUI=True)
        detector.run()

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main(3)
