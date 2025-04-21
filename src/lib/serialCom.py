#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        serialCom.py
#
# Purpose:     This module will inherit the standard python serial.Serial module 
#              with automatically serial port search and connection function.
#              Install serial: pip install pyserial
#
# Author:      Yuancheng Liu
#
# version:     v1.0.1
# Created:     2019/04/01
# Copyright:   Copyright (c) 2023 LiuYuancheng
# License:     MIT License  
#-----------------------------------------------------------------------------

import sys
import glob
import time
from serial import Serial, SerialException

BYTE_SIZE = 8
PARITY = 'N'
STOP_BIT = 1
TIME_OUT = 1

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class serialCom(Serial):
    """ The serialCom class inherit python serial.Serial class. Call read(int *) 
        or write(bytes *) to read number of bytes from the serial port or send bytes 
        to the port. Call close() to close the port.
    """
    def __init__(self, serialPort=None, baudRate=9600):
        """ Init the serial communication and if serialPort is None the program 
            will automatically find the port which it can connect.
            serialPort(string): port name string. 
            baudRate(int): serial communication baud rate.
        """
        self.connected = False
        # Automatically find the serial port which can read and write.
        self.serialPort = self._getConnectableSerial() if serialPort is None else serialPort
        # Call the parent __init__() to connect to the port.
        if self.serialPort is None:
            print('serialCom Error: no COM port can be used for connection.')
            self.connected = None
        else:
            print ('serialCom: the serial ports can be used : %s' % str(self.serialPort))
            try:
                super().__init__(self.serialPort, baudRate, BYTE_SIZE, PARITY, STOP_BIT, timeout=TIME_OUT)
                self.connected = True
            except:
                print("serialCom Error: serial port open error.")
                self.connected = False
        time.sleep(0.01) # Sleep a short while to wait the I/O to be ready for different system.

    #-----------------------------------------------------------------------------
    def _getConnectableSerial(self):
        """ Search all the connectable ports.For Windows-OS we use the last port(idx=-1) 
            in the list and in Linux-OS we use first port(idx=0). For Windows usage 
            please also set the baudRate at the windows device manager.   
        """
        conIdx = 0  # port index used for connection.
        portList = []   # port list can be used for connection.
        # search all the ports
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
            conIdx = -1
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            print ('serialCom: Serial Port comm connection error: Unsupported platform.')
            return None 
        # Check whether the ports can be open.
        for port in ports:
            try:
                s = Serial(port)
                s.close()
                portList.append(port)
            except (SerialException, OSError, Exception):
                pass
        # Return the result:
        return None if len(portList) == 0 else portList[conIdx]
    
    #-----------------------------------------------------------------------------
    def isConnected(self):
        return self.connected
    
    def getPortVal(self):
        return self.serialPort

    #-----------------------------------------------------------------------------
    def receiveStr(self, decodeType='utf-8'):
        """ Receive one line of string from the serial port.
            Args:
                decodeType (str, optional): byte to string decode type. Defaults to 'utf-8'.
            Returns:
                _type_: string if got data, '' if no data, None if error.
        """
        if not self.connected: return False
        try:
            data = self.readline()
            return data.decode(decodeType)
        except Exception as err:
            print("Err: [ read cmd ] connection lose.")
            self.connected = False
            return None

    #-----------------------------------------------------------------------------
    def sendStr(self, cmdStr, encodeType='utf-8'):
        """ Send a string cmd to the serial peer
            Args:
                cmdStr (str): command string
                encodeType (str, optional): string to byte encode type. Defaults to 'utf-8'.
            Returns:
                bool : True if send successful, else false.
        """
        if not self.connected: return False
        try:
            cmdByte = cmdStr.encode(encodeType) if isinstance(cmdStr, str) else cmdStr
            self.write(cmdByte)
            return True
        except Exception as err:
            print("Err: [ send cmd ] connection lose.")
            self.connected = False
            return False

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def testCase(mode):
    if mode == 0:
        print("Start serial port communication test. Test mode %s \n" %str(mode))
        print("Test Case 1: test connect to the un-readable port.")
        connector = serialCom(serialPort="COM_NOT_EXIST", baudRate=115200)

        print("Test Case 2: test connect to com port.")
        connector = serialCom(baudRate=115200)
        try:
            connector.write('Test String'.encode('utf-8'))
        except Exception as e:
            print('I/O exception:%s', e)
        try:
            msg = connector.read(128)
            print("Read message from the com: %s" %str(msg))
        except Exception as e:
            print('I/O exception:%s', e)
    else:
         print("Add more other exception test here.")

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    testCase(0)
