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

import os
import json
import threading

import robotEyeGlobal as gv
import camDetector

import udpCom
import ConfigLoader

CFG_FILE = 'robotEyeConfig.txt'
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
        self.server = udpCom.udpServer(None, gv.gUdpPort)
        #self.server.setBufferSize(bufferSize=gv.BUF_SZ)
        self.terminate = False

    #-----------------------------------------------------------------------------
    def run(self):
        print("Start the robot eye service host..")
        print("Start the UDP echo server listening port [%s]" % str(gv.gUdpPort))
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

    #-----------------------------------------------------------------------------
    def stop(self):
        """ Stop the thread."""
        self.terminate = True
        if self.server: self.server.serverStop()
        endClient = udpCom.udpClient(('127.0.0.1', gv.gUdpPort))
        endClient.disconnect()
        endClient = None


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class robotEye(object):

    def __init__(self, mode=0) -> None:
        print("Start init the robot eye:")
        cfgFilePath = os.path.join(gv.dirpath, CFG_FILE)
        self.cfgLoader = ConfigLoader.ConfigLoader(cfgFilePath, mode='r')
        cfg_dict = self.cfgLoader .getJson()
        # init the detector paramters
        mode = cfg_dict['DET_TYPE'] if 'DET_TYPE' in cfg_dict.keys() else None 
        if 'UDP_PORT' in cfg_dict.keys(): gv.gUdpPort = int(cfg_dict['UDP_PORT'])
        camIdxParm = int(cfg_dict['CAM_IDX']) if 'CAM_IDX' in cfg_dict.keys() else 0
        showUIParm = cfg_dict['SHOW_UI'] if 'SHOW_UI' in cfg_dict.keys() else True
        imgIntParm = float(cfg_dict['FPS_INT']) if 'FPS_INT' in cfg_dict.keys() else 0.1

        if mode == FACE_DET_KEY:
            print("Init the face detector ...")
            detectEyeFlg = cfg_dict['DET_EYE'] if 'DET_EYE' in cfg_dict.keys() else False 
            gv.iDetector = camDetector.faceDetector(camIdx=camIdxParm,
                showUI=showUIParm, imgInt=imgIntParm, detectEye=detectEyeFlg)
            gv.iDetector.setDisplayInfo(True, "Face Detection")
            print("Start the communication handler.")
        elif mode == QRCD_DET_KEY:
            print("Init the Qr-code detector ...")
            decodeInfoFlg = cfg_dict['QR_DECODE'] if 'QR_DECODE' in cfg_dict.keys() else False 
            gv.iDetector = camDetector.qrcdDetector(
                camIdx=camIdxParm, showUI=showUIParm, imgInt=imgIntParm, decodeFlg=decodeInfoFlg)
            gv.iDetector.setDisplayInfo(True, "QR-Code Detection")
        else:
            print("The detector mode [%s] is not valid, exit..." %str(mode))
            return None 
        
        print("Start the communication handling thread.")
        gv.iConnHandler = connectionHandler(self)
        gv.iConnHandler.start()
        print("Robot Eye init finished.")

    # -----------------------------------------------------------------------------
    def run(self):
        print("Start the robot eye.")
        gv.iDetector.run()

    # -----------------------------------------------------------------------------
    def stop(self):
        if gv.iConnHandler: gv.iConnHandler.stop()
        if gv.iDetector: gv.iDetector.stop()

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def main(mode):
    gv.iMainFrame = robotEye(mode=mode)
    gv.iMainFrame.run()

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main(1)
