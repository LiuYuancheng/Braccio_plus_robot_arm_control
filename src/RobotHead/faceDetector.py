
import time
import threading
import udpCom

import cv2

UDP_PORT = 3004

class connectionHandler(threading.Thread):

    def __init__(self, parent) -> None:
        threading.Thread.__init__(self)
        self.parent = parent
        self.server = udpCom.udpServer(None, UDP_PORT)
        #self.server.setBufferSize(bufferSize=gv.BUF_SZ)

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
        
        # Reply tojan connection accept
        resp = 'FD;result;'
        result = 0
        reqKey, reqType, data = self.parseIncomeMsg(msg)
        if reqKey == 'FD':
            if self.parent.getDetectionResult():
                result = 1
        resp += str(result)
        return resp

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class faceDetector(object):

    def __init__(self, parent, frameInterval=None,  detectEye=False, imageSize =(640, 480)) -> None:
        self.parent = parent
        self.detectEye = detectEye
        self.framInterval = frameInterval
        print("Start to try to open the device camera.")
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, imageSize[0])
        self.cap.set(4, imageSize[1])
        self.faceDetResult = [0]*10
        # import cascade file for facial recognition
        self.faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        if self.detectEye:
            # if you want to detect any object for example eyes, use one more layer of classifier as below:
            self.eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml")
        self.terminate = False

        connHandler = connectionHandler(self)
        connHandler.start()

    #-----------------------------------------------------------------------------   
    def run(self):
        while not self.terminate:
            #print("start")
            success, img = self.cap.read()
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Getting corners around the face
            faces = self.faceCascade.detectMultiScale(imgGray, 1.3, 5)  # 1.3 = scale factor, 5 = minimum neighbor
            # drawing bounding box around face
            self.faceDetResult.pop(0)
            
            for (x, y, w, h) in faces:
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            if len(faces) > 0:    
                self.faceDetResult.append(1)
            else:
                self.faceDetResult.append(0)

            if self.detectEye: 
            # detecting eyes
                eyes = self.eyeCascade.detectMultiScale(imgGray)
                # drawing bounding box for eyes
                for (ex, ey, ew, eh) in eyes:
                    img = cv2.rectangle(img, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)

            cv2.imshow('face_detect', img)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            time.sleep(self.framInterval)
            #self.getDetectionResult()

    #-----------------------------------------------------------------------------   
    def getDetectionResult(self):
        count = self.faceDetResult.count(1)
        return count > 7

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main(mode):
    detector = faceDetector(None, frameInterval=0.1)
    detector.run()

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main(0)