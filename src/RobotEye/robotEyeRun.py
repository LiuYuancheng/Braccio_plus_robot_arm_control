#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        robotEyeRun.py
#
# Purpose:     This module will init a detector to detect face / Qr-code, then 
#              start a UDP server for other module to connect and fetch the 
#              detection result.
#
# Author:      Yuancheng Liu
#
# Version:     v_0.1
# Created:     2023/09/21
# Copyright:   Copyright (c) 2023 LiuYuancheng
# License:     MIT License  
#-----------------------------------------------------------------------------

import json
import threading

import robotEyeGlobal as gv
import camDetector

import udpCom

FACE_DET_KEY = 'FD' # face detection request/respond key
QRCD_DET_KEY = 'QD' # QR ccode detection request/respond key.

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class connectionHandler(threading.Thread):
    """ UDP server to handle the other module's connection / data fetch request.
    """
    def __init__(self, parent) -> None:
        threading.Thread.__init__(self)
        self.parent = parent
        self.server = udpCom.udpServer(None, gv.UDP_PORT)
        #self.server.setBufferSize(bufferSize=gv.BUF_SZ)

    #-----------------------------------------------------------------------------
    def run(self):
        print("Start the robot eye service host..")
        print("Start the UDP echo server listening port [%s]" % str(gv.UDP_PORT))
        self.server.serverStart(handler=self.cmdHandler)
    
    #-----------------------------------------------------------------------------
    def parseIncomeMsg(self, msg):
        """ Split the trojan connection's control cmd to:
            - reqKey: request key which idenfiy the action category.
            - reqType: request type which detail action type.
            - reqData: request data which will be used in the action.
        """
        reqKey = reqType = reqData = None
        try:
            if isinstance(msg, bytes): msg = msg.decode('utf-8')
            reqKey, reqType, reqData = msg.split(';', 2)
            return (reqKey.strip(), reqType.strip(), reqData)
        except Exception as err:
            print('The incoming message format is incorrect, ignore it. Error')
            print(err)
            return (reqKey, reqType, reqData)
        
    #-----------------------------------------------------------------------------
    def cmdHandler(self, msg):
        """ The detection request handler."""
        if isinstance(msg, bytes): msg = msg.decode('utf-8')
        print("Incoming message: %s" %str(msg))
        if msg == '': return None
        resp = None
        reqKey, reqType, data = self.parseIncomeMsg(msg)
        if reqKey == FACE_DET_KEY:
            resp =  self._handleFaceDetect(reqType, data)
        elif reqKey == QRCD_DET_KEY:
            resp = self._handleQrcdDetect(reqType, data)
        return resp

    #-----------------------------------------------------------------------------
    def _handleFaceDetect(self, reqType, data):
        """ Handle the face detection request."""
        resp = FACE_DET_KEY+';err;0'
        if gv.iDetector and str(reqType).lower() == 'rst':
            result = {
                'rst': gv.iDetector.getDetectionResult(),
                'pos': gv.iDetector.getLastDectPos()
            }
            resp = ';'.join((FACE_DET_KEY, 'rst', json.dumps(result)))
        return resp

    #-----------------------------------------------------------------------------
    def _handleQrcdDetect(self, reqType, data):
        """ Handle the QR-code detection quest."""
        resp = QRCD_DET_KEY+';err;0'
        if gv.iDetector and str(reqType).lower() == 'rst':
            result = {
                'rst': gv.iDetector.getDetectionResult(),
                'pos': gv.iDetector.getDetectedQRCent()
            }
            resp = ';'.join((QRCD_DET_KEY, 'rst', json.dumps(result)))
        return resp

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class robotEye(object):

    def __init__(self, mode=0) -> None:
        self.detector = None
        if mode == 0:
            print("Init the face detector...")
            self.detector = camDetector.faceDetector(
                showUI=True, imgInt=0.1, detectEye=False)
            self.detector.setDisplayInfo(True, "Face Detection")
            print("Start the communication handler.")
        else:
            self.detector = camDetector.qrcdDetector(imgInt=0.1, showUI=True)
            self.detector.setDisplayInfo(True, "QR-Code Detection")
        gv.iDetector = self.detector
        connHandler = connectionHandler(self)
        connHandler.start()

    def run(self):
        self.detector.run()

    def getDetectionResult(self):
        return self.detector.getDetectionResult()

    def getQRcodePos(self):
        return self.detector.getQRcodeCentPo()

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def main(mode):
    gv.iMainFrame = robotEye(mode=mode)
    gv.iMainFrame.run()

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main(1)
