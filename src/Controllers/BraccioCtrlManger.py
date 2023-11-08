#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        BraccioCtrlManger.py
#
# Purpose:     This module is the data manager module also used for handling 
#              the serial communication ( send the control request to Arduino and 
#              and fetch the potentiometer data).
#
# Author:      Yuancheng Liu
#
# Version:     v_0.1
# Created:     2023/11/03
# Copyright:   Copyright (c) 2023 LiuYuancheng
# License:     MIT License  
#-----------------------------------------------------------------------------
import os 
import json
from queue import Queue
import threading
import serialCom
import udpCom
import BraccioCtrlGlobal as gv

UDP_PORT = 3005

MAX_QSZ = 50

POS_TAG = 'POS'
MMV_TAG = 'MOV'
RST_TAG = 'RST'

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class CtrlManager(object):
    """ Control manager parent class"""

    def __init__(self, maxQsz=MAX_QSZ) -> None:
        self.connector = None
        self.taskQueue = Queue(maxsize=MAX_QSZ)

    def _enqueueTask(self, taskStr):
        if self.taskQueue.full():
            print("Tasks queue full, can not add cmd: %s" % str(taskStr))
            return
        self.taskQueue.put(taskStr)

    def _dequeuTask(self):
        return None if self.taskQueue.empty() else self.taskQueue.get_nowait()

    def addTasks(self, tasklist):
        """ Add the input tasks string list into the tasks queue."""
        for cmd in tasklist:
            self._enqueueTask(cmd)

    def hasQueuedTask(self):
        return not self.taskQueue.empty()

    def getConnection(self):
        if self.connector: return self.connector.isConnected()
        return False
     
    def stop(self):
        if self.connector: self.connector.close()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class CtrlManagerSerial(CtrlManager):
    """ Control manager used for serial communication. """
    def __init__(self, serialPort, baudRate=9600, maxQsz=MAX_QSZ) -> None:
        super().__init__(maxQsz)
        self.connector = serialCom.serialCom(serialPort=serialPort, baudRate=baudRate)
        self.motorAngles = [None]*6
        if self.connector and self.connector.isConnected():
            print("Connected to the Braccio robot with port %s successfully" %str(self.connector.getPortVal()))
        else:
            print("Error: serical port under usage.")

    #-----------------------------------------------------------------------------
    def addMotorMovTask(self, motorKey, motoVal):
        self.addTasks((MMV_TAG+str(motorKey)+str(motoVal),))

    #-----------------------------------------------------------------------------
    def addRestTask(self):
        self.addTasks((RST_TAG,))

    #-----------------------------------------------------------------------------
    def fetchMotorPos(self):
        if not self.connector.isConnected(): return None
        cmdStr = POS_TAG
        if self.connector.sendStr(cmdStr):
            data = self.connector.receiveStr()
            if data == '' or data is None:return None
            if POS_TAG in data:
                data = data.split(':')[1]
                self.motorAngles = [int(float(val)) for val in data.split(';')[:6]]
        else:
            self.motorAngles = [None]*6

    #-----------------------------------------------------------------------------
    def getModtorPos(self):
        return self.motorAngles 
    
    #-----------------------------------------------------------------------------
    def movMotor(self, motorKey, motoVal):
        """Send the motor move command immediately."""
        cmd = MMV_TAG+str(motorKey)+str(motoVal)
        self.connector.sendStr(cmd)

    #-----------------------------------------------------------------------------
    def resetPos(self):
        """Send the reset command immediately."""
        self.connector.sendStr(RST_TAG)

    #-----------------------------------------------------------------------------
    def stop(self):
        if self.connector: self.connector.close()

    #-----------------------------------------------------------------------------
    def runQueuedTask(self):
        cmd = self._dequeuTask()
        if not cmd is None: 
            print("Run task: %s" %str(cmd))
            return self.connector.sendStr(cmd)

    #-----------------------------------------------------------------------------
    
class connectionHandler(threading.Thread):

    def __init__(self, parent) -> None:
        threading.Thread.__init__(self)
        self.parent = parent
        self.server = udpCom.udpServer(None, gv.gHostPort)
        #self.server.setBufferSize(bufferSize=gv.BUF_SZ)
        self.tasksList = []
        actConfigPath = os.path.join(gv.SCE_FD, 'demo.json')
        if os.path.exists(actConfigPath):
            with open(actConfigPath) as json_file:
                self.tasksList = json.load(json_file)
                print("loaded the demo scenario")

    #-----------------------------------------------------------------------------
    def run(self):
        print("Start the trojanReceiverMgr.")
        print("Start the UDP echo server listening port [%s]" % str(UDP_PORT))
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
        resp = "busy"
        if msg == 'demo' and gv.iCtrlManger :
            if not gv.iCtrlManger.hasQueuedTask():
                if self.tasksList and len(self.tasksList) > 0:
                    print("Execute scenario: demo.json")
                    for action in self.tasksList:
                        if action['act'] == 'RST':
                            gv.iCtrlManger.addRestTask()
                        elif action['act'] == 'MOV':
                            gv.iCtrlManger.addMotorMovTask(action['key'], action['val'])
                    resp = "ready"
        return resp