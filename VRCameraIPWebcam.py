#udp server to receive images
import socket
import cv2
import numpy as np
import time
import sys
import threading
import serial.tools.list_ports
import keyboard
#IP webcam sends image to this pc, this pc elaborates and sends to Godot Mobile
#Godot Mobile sends angles to this pc, this pc elaborates and sends to Robot
#        IP webcam <-angles|image-> PC <-angles|image-> Godot Mobile
FULL_REMOTE = True
MY_IP = '192.168.1.14' #'192.168.213.219'
VR_IP = '192.168.1.7' #'192.168.213.156'
STREAM_URL = 'http://192.168.1.7:4747/video'
#-------------on IP webcam-------------
#
#
#---------on Godot Mobile (VR)---------
#ARVRCamera line 13: udp.connect_to_host("MY_IP",1235)
#Button3 line 43: scale the streamed image

#FULL_REMOTE (yellow 2 RX green 13 TX)
#import cameraStream4
#cameraStream4.start("192.168.43.183",1234)

#SERIAL
#import cameraStream2
#cameraStream4.start("192.168.43.183",1234)

#ESP32 at http://micropython.org/webrepl/#192.168.1.6:8266/ once the hotspot is on, change ip to "espressif"
#in case of different network name the network id and password are in boot.py inside the sd card
#----GET ESP IP
#ESP = str(socket.gethostbyname('espressif'))

#stream image scaling parameters
#0.13 good compromise
scaleX = 1
scaleY = scaleX
MIN_ANGLE = '036'

#main just reads, for some reason using threads 
#works better and avoids freezing after some time

#todo automatic scaling in godot application

ports = list(serial.tools.list_ports.comports())
for p in ports:
    if "Arduino" in p.description:
        bot = serial.Serial(p.device, 115200)
        break
#print(bot)

sockImageReceive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (MY_IP, 1234)
sockImageReceive.bind(server_address)

sockGyro = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (MY_IP, 1235)
sockGyro.bind(server_address)

sockImageSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (MY_IP, 1236)
sockImageSend.bind(server_address)

sockSendAngles = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (MY_IP, 1233)
sockSendAngles.bind(server_address)

def angleToString(angle):
    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180
    angle = str(angle)
    if len(angle) == 1:
        angle = "00" + angle
    elif len(angle) == 2:
        angle = "0" + angle
    return angle



calibrated = False
posZero = [0,0]
prevSendTime = time.time()

def receiveGyro():
    calibrated = False
    posZero = [0,0]
    prevSendTime = time.time()
    while True:
        try:
            print("receiveGyro")
            data, address = sockGyro.recvfrom(100)
            print(data)
            data = data.decode()
            #data remove Vector3
            data = data.replace("Vector3", "")
            #data remove ()
            data = data.replace("(", "")
            data = data.replace(")", "")
            #for element in data convert from radians to degrees
            data = data.split(",")
            for i in range(len(data)):
                data[i] = float(data[i])
                data[i] = data[i] * 180 / 3.14159265358979323846
            #for i in data print float with 3 decimal places
            if not calibrated:
                posZero = [int(0), int(data[1])] #int(data[0])
                calibrated = True
            data = [int(data[0] - posZero[0] + 90), int(data[1] - posZero[1] + 90)]
            #if data[1] between 0 and 180
            data[1] = min(max(data[1],0),180)
            data[0] = min(max(data[0],0),180)
            if data[1] >= 0 and data[1] <= 180:
                if data[0] >= 0 and data[0] <= 180:
                    #data = [data[0] - posZero[0] + 90, data[1] - posZero[1] + 90]
                    data[0] = angleToString(data[0])
                    data[1] = angleToString(data[1])
            #print(data)
                if(int(data[0])<int(MIN_ANGLE)):
                    data[0] = MIN_ANGLE
                data = f's{data[1]}000000{data[0]}000000000000000000000000000000000000\n'
                # s090000000090000000000000000000000000000000000000\n
                #print(data)
            #if time since last send > 0.5
            if time.time() - prevSendTime > 0.1:
                prevSendTime = time.time()
                if(FULL_REMOTE):
                    adds=(ESP,1233)
                    sockSendAngles.sendto(data.encode('utf-8'), adds)
                else:
                    bot.write(data.encode())
            print(data)
            #for i in data:
            #    print("%7.1f" % i, end=" ")
            #print()
            if keyboard.is_pressed('space'):
                break
        except Exception as e:
            print(e)
            pass


#receive_thread = threading.Thread(target=receiveGyro)
#receive_thread.start()

def sendImage():
    prevRecvTime = time.time()
    #cv2.namedWindow("VRCamera", cv2.WINDOW_AUTOSIZE)
    vcap = cv2.VideoCapture(STREAM_URL)
    if not vcap.isOpened():
        print("File Cannot be Opened")
        exit()
    while True:
        try:
            print("sendImage")
            #opencv url video
            ret, frame = vcap.read()
            #frame = cv2.imdecode(frame, 1)
            #frame2 = cv2.imencode('.jpg', frame)[1]
            if time.time() - prevRecvTime > 0.001:
                if frame is not None:
                    print("show")
                    #resize frame
                    frame = cv2.resize(frame, (0,0), fx=0.7, fy=0.7)
                    cv2.imshow("VRCamera",frame)
                    cv2.waitKey(1)
                    adds = (VR_IP, 1236)
                    frame = cv2.imencode('.jpg', frame)[1]
                    sockImageSend.sendto(bytes(frame), adds)
                prevRecvTime = time.time()
            if keyboard.is_pressed('space'):
                break
        except Exception as e:
            print(e)
            pass

send_thread = threading.Thread(target=sendImage)
send_thread.start()

while True:
    bot.read()
    if keyboard.is_pressed('space'):
        break

#receive_thread.join()
#send_thread.join()
exit()

while True:
    try:
        data, address = sockGyro.recvfrom(100)
        data = data.decode()
        #data remove Vector3
        data = data.replace("Vector3", "")
        #data remove ()
        data = data.replace("(", "")
        data = data.replace(")", "")
        #for element in data convert from radians to degrees
        data = data.split(",")
        for i in range(len(data)):
            data[i] = float(data[i])
            data[i] = data[i] * 180 / 3.14159265358979323846
        #for i in data print float with 3 decimal places
        if not calibrated:
            posZero = [int(0), int(data[1])] #int(data[0])
            calibrated = True
        data = [int(data[0] - posZero[0] + 90), int(data[1] - posZero[1] + 90)]
        #if data[1] between 0 and 180
        if data[1] >= 0 and data[1] <= 180:
            if data[1] >= 0 and data[1] <= 180:
                #data = [data[0] - posZero[0] + 90, data[1] - posZero[1] + 90]
                data[0] = angleToString(data[0])
                data[1] = angleToString(data[1])
        #print(data)
            data = f's{data[1]}000000{data[0]}000000000000000000000000000000000000\n'
            #print(data)
        #if time since last send > 0.5
        if time.time() - prevSendTime > 0.1:
            bot.write(data.encode())
            prevSendTime = time.time()
        print(data)
        #for i in data:
        #    print("%7.1f" % i, end=" ")
        #print()
    except Exception as e:
        print(e)
        pass
        
    try:
        data, address = sockImageReceive.recvfrom(50000)
        #data = data.decode()
        #for element in data convert from radians to degrees
        image = []
        #print(data.decode('utf-8', 'ignore'))
        nparr = np.fromstring(data, np.uint8)
        print(nparr.size)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img_np = cv2.resize(img_np, (0,0), fx=0.1, fy=0.1)
        #print(img_np)
        # f = cv2.resize(f, (0,0), fx=2, fy=2)
        for i in cv2.imencode('.bmp', img_np)[1]: #only bmp seems to work in godot mobile
            image.append(i)
        #show image
        #print(image)
        #cv2.imshow('image', img_np)
        #cv2.waitKey(0)
        adds = (VR_IP, 1236)
        sockImageSend.sendto(bytes(image), adds)
    except Exception as e:
        print(e)
        pass
         
#launch receive thread
#receive_thread = threading.Thread(target=receive)
#receive_thread.start()



#def receive():
data, address = sockImageReceive.recvfrom(20000)
#data = data.decode()
#for element in data convert from radians to degrees
image = []
#print(data.decode('utf-8', 'ignore'))
nparr = np.fromstring(data, np.uint8)
print(nparr.size)
img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#print(img_np)
# f = cv2.resize(f, (0,0), fx=2, fy=2)
for i in cv2.imencode('.bmp', img_np)[1]: #only bmp seems to work in godot mobile
    image.append(i)
#show image
#print(image)
cv2.imshow('image', img_np)
cv2.waitKey(0)