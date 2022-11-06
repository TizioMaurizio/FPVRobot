#udp server to receive images
import socket
import cv2
import numpy as np
import time
import sys
import threading
import serial.tools.list_ports
import keyboard
MIN_ANGLE = '036'
#ESP32 sends image to this pc, this pc elaborates and sends to Godot Mobile
#Godot Mobile sends angles to this pc, this pc elaborates and sends to Robot
#        ESP32 <-angles|image-> PC <-angles|image-> Godot Mobile

MY_IP = '192.168.43.183' #'192.168.213.219'
VR_IP = '192.168.43.98' #'192.168.213.156'
#--------------on ESP32----------------
#import cameraStream2
#cameraStream2.start("MY_IP",1234)
#---------on Godot Mobile (VR)---------
#ARVRCamera line 13: udp.connect_to_host("MY_IP",1235)
#Button3 line 43: scale the streamed image

#ESP32 at http://micropython.org/webrepl/#192.168.1.6:8266/ once the hotspot is on, change ip to "espressif"
#in case of different network name the network id and password are in boot.py inside the sd card

#stream image scaling parameters
#0.13 good compromise
scaleX = 0.25
scaleY = scaleX
#cameraStream2.start("192.168.43.183",1235)
#main just reads, for some reason using threads 
#works better and avoids freezing after some time

#todo automatic scaling in godot application

ports = list(serial.tools.list_ports.comports())
for p in ports:
    if "Arduino" in p.description:
        bot = serial.Serial(p.device, 115200)
        break
print(bot)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (MY_IP, 1234)
sock.bind(server_address)

sockGyro = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (MY_IP, 1235)
sockGyro.bind(server_address)

sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (MY_IP, 1236)
sock2.bind(server_address)

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
                #print(data)
            #if time since last send > 0.5
            if time.time() - prevSendTime > 0.1:
                bot.write(data.encode())
                prevSendTime = time.time()
            print(data)
            #for i in data:
            #    print("%7.1f" % i, end=" ")
            #print()
            if keyboard.is_pressed('space'):
                break
        except Exception as e:
            print(e)
            pass


receive_thread = threading.Thread(target=receiveGyro)
receive_thread.start()

def sendImage():
    prevRecvTime = time.time()
    #cv2.namedWindow("VRCamera", cv2.WINDOW_AUTOSIZE)
    while True:
        try:
            print("sendImage")
            data, address = sock.recvfrom(60000)
            #data = data.decode()
            #for element in data convert from radians to degrees
            image = []
            #print(data.decode('utf-8', 'ignore'))
            nparr = np.fromstring(data, np.uint8)
            print(nparr.size)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            img_np = cv2.resize(img_np, (0,0), fx=scaleX, fy=scaleY)
            #print(img_np)
            # f = cv2.resize(f, (0,0), fx=2, fy=2)
            for i in cv2.imencode('.bmp', img_np)[1]: #only bmp seems to work in godot mobile
                image.append(i)
            #show image
            #print(image)
            if time.time() - prevRecvTime > 0.1:
                prevRecvTime = time.time()
                print("show")
                cv2.imshow("VRCamera",cv2.resize(img_np, (0,0), fx=768/img_np.shape[0], fy=1024/img_np.shape[1]))
                cv2.waitKey(1)
            adds = (VR_IP, 1236)
            sock2.sendto(bytes(image), adds)
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
        data, address = sock.recvfrom(50000)
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
        sock2.sendto(bytes(image), adds)
    except Exception as e:
        print(e)
        pass
         
#launch receive thread
#receive_thread = threading.Thread(target=receive)
#receive_thread.start()



#def receive():
data, address = sock.recvfrom(20000)
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