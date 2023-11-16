#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        faceDetector.py
#
# Purpose:     
#
# Author:      Yuancheng Liu
#
# Version:     v_0.1
# Created:     2023/09/21
# Copyright:   Copyright (c) 2023 LiuYuancheng
# License:     MIT License  
#-----------------------------------------------------------------------------

import time
import threading

import robotEyeGlobal as gv
import camDetector

import udpCom

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class connectionHandler(threading.Thread):

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
            print('The incoming message format is incorrect, ignore it.')
            print(err)
            return (reqKey, reqType, reqData)
        
    #-----------------------------------------------------------------------------
    def cmdHandler(self, msg):
        """ The trojan report handler method passed into the UDP server to handle the 
            incoming messages.
        """
        if isinstance(msg, bytes): msg = msg.decode('utf-8')
        print("incoming message: %s" %str(msg))
        if msg == '': return None
        
        # Reply tojan connection accept
        resp = ''
        result = 0
        reqKey, reqType, data = self.parseIncomeMsg(msg)
        if reqKey == 'FD':
            resp = 'FD;result;'
            if self.parent.getDetectionResult(): result = 1
            resp += str(result)
        elif reqKey == 'CD':
            if reqType == 'result':
                resp = 'CD;result;'
                if self.parent.getDetectionResult(): result = 1
                resp += str(result)
            else:
                resp = 'CD;pos;'
                if self.parent.getDetectionResult(): 
                    result = str(self.parent.getQRcodePos())
                resp += str(result)
        return resp

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class robotEye(object):

    def __init__(self, mode=0) -> None:
        self.detector = None
        if mode == 0:
            print("Init the face detector...")
            self.detector = camDetector.faceDetector(
                showUI=True, detectEye=False)
            self.detector.setDisplayInfo(True, "Face Detection")
            print("Start the communication handler.")
        else:
            self.detector = camDetector.qrcdDetector(imgInt=0.1, showUI=True)
            self.detector.setDisplayInfo(True, "QR-Code Detection")

        connHandler = connectionHandler(self)
        connHandler.start()

    def run(self):
        self.detector.run()

    def getDetectionResult(self):
        return self.detector.getDetectionResult()

    def getQRcodePos(self):
        return self.detector.getQRcodeCentPo()

def main(mode):
    gv.iMainFrame = robotEye(mode=mode)
    gv.iMainFrame.run()

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main(1)
