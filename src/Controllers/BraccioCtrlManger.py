#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        scadaDataMgr.py
#
# Purpose:     Data manager module used to control all the other data processing 
#              modules and store the interprocess /result data.
#
# Author:      Yuancheng Liu
#
# Created:     2023/06/13
# Version:     v0.1.2
# Copyright:   Copyright (c) 2023 Singapore National Cybersecurity R&D Lab LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

import time
from queue import Queue
import serialCom
import BraccioCtrlGlobal as gv

MAX_QSZ = 20

POS_TAG = 'POS'
MMV_TAG = 'MOV'
RST_TAG = 'RST'

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class CtrlManager(object):
    """ The data manager is a module running parallel with the main thread to 
        connect to PLCs to do the data communication with modbus TCP.
    """
    def __init__(self, parent, comInfo) -> None:
        self.connector = serialCom.serialCom(None, serialPort='COM3',baudRate=9600)
        self.taskQueue = Queue(maxsize=MAX_QSZ)
        self.connected = self.connector.connected
        self.motorAngles = [None]*6
        if self.connected:
            print("Linked to the Braccio robot successfully")
        else:
            print("Error: serical port under usage.")

    #-----------------------------------------------------------------------------
    def _sendCommCmd(self, cmdStr):
        if not self.connected: return False
        try:
            cmd = cmdStr.encode(gv.STR_DECODE) if isinstance(cmdStr, str) else cmdStr
            self.connector.write(cmd)
            return True
        except Exception as err:
            print("Err: [ send cmd ] connection lose.")
            if gv.DEBUG: print("Error detail: %s" %str(err))
            self.connected = False
            self.motorAngles = [None]*6
            return False

    #-----------------------------------------------------------------------------
    def _readCommData(self):
        if not self.connected: return False
        try:
            data = self.connector.readline()
            return data.decode(gv.STR_DECODE)
        except Exception as err:
            print("Err: [ read cmd ] connection lose.")
            if gv.DEBUG: print("Error detail: %s" %str(err))
            self.connected = False
            self.motorAngles = [None]*6
            return None

    #-----------------------------------------------------------------------------
    def fetchMotorPos(self):
        cmdStr = POS_TAG
        if self._sendCommCmd(cmdStr):
            data = self._readCommData()
            if data == '' or data is None:return None
            if POS_TAG in data:
                data = data.split(':')[1]
                self.motorAngles = [int(float(val)) for val in data.split(';')[:6]]
        else:
            self.motorAngles = [None]*6
       
    def getModtorPos(self):
        return self.motorAngles 
    
    #-----------------------------------------------------------------------------
    def movMotor(self, motorKey, motoVal):
        cmd = MMV_TAG+str(motorKey)+str(motoVal)
        self._sendCommCmd(cmd)

    #-----------------------------------------------------------------------------
    def resetPos(self):
        cmd = RST_TAG
        self._sendCommCmd(cmd)

    #-----------------------------------------------------------------------------
    def stop(self):
        if self.connector: self.connector.close()

    #-----------------------------------------------------------------------------
    def hasQueuedTask(self):
        return not self.taskQueue.empty()

    #-----------------------------------------------------------------------------
    def runQueuedTask(self):
        if self.taskQueue.empty(): return False
        cmd = self.taskQueue.get()
        print("Run task: %s" %str(cmd))
        return self._sendCommCmd(cmd)

    #-----------------------------------------------------------------------------
    def addTasks(self, tasklist):
        for cmd in tasklist:
            if self.taskQueue.full():
                print("Task queue full, can not add cmd: %s" %str(cmd))
                continue
            self.taskQueue.put(cmd)
    
    def addMotorMovTask(self, motorKey, motoVal):
        self.addTasks((MMV_TAG+str(motorKey)+str(motoVal),))
    
    def addRestTask(self):
        self.addTasks((RST_TAG,))