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
from collections import OrderedDict
import serialCom

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class CtrlManager(object):
    """ The data manager is a module running parallel with the main thread to 
        connect to PLCs to do the data communication with modbus TCP.
    """
    def __init__(self, parent, comInfo) -> None:
        self.connector = serialCom.serialCom(None, serialPort='COM3',baudRate=9600)
        self.cmdSeq = []
        if self.connector.connected:
            print("Linked to the Braccio robot successfully")
        else:
            print("Error: serical port under usage.")

    #-----------------------------------------------------------------------------
    def getPos(self):
        cmd = 'POS'
        self.connector.write(cmd.encode('utf-8'))
        msg = self.connector.readline()
        msg = msg.decode('utf-8')
        if 'POS' in msg:
            data = msg.split(':')[1]
            angles = [ int(float(val)) for val in data.split(';')[:6]]
            return angles
        else:
            return None

    #-----------------------------------------------------------------------------
    def movPart(self, key, value):
        Tag = 'MOV'
        cmd = Tag+str(key)+str(value)
        self.connector.write(cmd.encode('utf-8'))

    def resetPos(self):
        cmd = 'RST'
        self.connector.write(cmd.encode('utf-8'))

    def stop(self):
        if self.connector:
            self.connector.close()

    def hasNewTask(self):
        if len(self.cmdSeq) == 0:
            return False
        prt, val = self.cmdSeq.pop(0)
        print("run action: %s" %str((prt, val)))
        self.movPart(prt, val)
        return True
    
    def setTask(self, tasklist):
        self.cmdSeq = tasklist