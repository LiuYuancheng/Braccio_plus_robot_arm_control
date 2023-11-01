import time
import serialCom

connector = serialCom.serialCom(None, serialPort='COM3',baudRate=9600)

if connector.connected:
    while True:
        print("Connected to the Braccio arm")
        print("Input the cmd :")
        cmd = str(input())
        connector.write(cmd.encode('utf-8'))
        time.sleep(3)
        print("Got feed back:")
        msg = connector.readline()
        print(msg)
