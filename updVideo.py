#python udp server on localhost
import socket
import sys
#thread
import threading
import time
import cv2
import numpy as np
#open mp4 and save it to a buffer

#convert video mp4 to array of images
def videoToByteArray(video):
    #open video
    cap = cv2.VideoCapture(video)
    #read frame
    ret, frame = cap.read()
    #create array of images
    images = []
    #while frame is present
    while ret:
        #convert image to byte array
        #rescale frame to 10%
        frame = cv2.resize(frame, (0,0), fx=0.2, fy=0.2)
        images.append(frame)
        #read next frame
        ret, frame = cap.read()
    return images

print(cv2.imencode('.jpg', videoToByteArray("The Wolf of the Wall Street (2013)_ Jordan's First Day at Wall Street (online-video-cutter.com).mp4")[1])[1])
#read the data from the file
with open('wolf.png', 'rb') as infile:
     buf = infile.read()

#use numpy to construct an array from the bytes
x = np.fromstring(buf, dtype='uint8')
#for i in x append to array
image = []
#for i in cv2.imencode('.png', videoToByteArray("The Wolf of the Wall Street (2013)_ Jordan's First Day at Wall Street (online-video-cutter.com).mp4")[1])[1]:
for i in x:
    image.append(i)

#foreach frame in videoToByteArray("The Wolf of the Wall Street (2013)_ Jordan's First Day at Wall Street (online-video-cutter.com).mp4") show frame
for frame in videoToByteArray("The Wolf of the Wall Street (2013)_ Jordan's First Day at Wall Street (online-video-cutter.com).mp4"):
    break
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
##cv2.imshow('frame', videoToByteArray("The Wolf of the Wall Street (2013)_ Jordan's First Day at Wall Street (online-video-cutter.com).mp4")[1])
#cv2.imshow('frame', cv2.imencode('.jpg', videoToByteArray("The Wolf of the Wall Street (2013)_ Jordan's First Day at Wall Street (online-video-cutter.com).mp4")[1])[1])
##if cv2.waitKey(1):
##     pass

print(image)

#while true receive data
#create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#bind socket to localhost and port 10000
server_address = ('192.168.1.12', 1234)
sock.bind(server_address)

sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#bind socket to localhost and port 10000
server_address = ('192.168.1.12', 1236)
sock2.bind(server_address)

print('starting up on %s port %s' % sock.getsockname())
print('starting up on %s port %s' % sock2.getsockname())
#start new thread for receiving data
def receive():
    while True:
        #if present print received data
        data, address = sock.recvfrom(1234)
        if data.decode() == "stop":
            sys.exit()
        if data.decode() == "image":
            print('sending image')
            #sock2.sendto(bytes("ciao".encode()), ('192.168.1.12', 1234))
            adds = ('192.168.1.12', 1236)
            sock2.sendto(bytes(image), adds)
            print(adds)
            print('image sent')
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
        for i in data:
            print("%7.1f" % i, end=" ")
        print()
         
#launch receive thread
receive_thread = threading.Thread(target=receive)
receive_thread.start()

import keyboard
sent = False

#prevtime
prevtime = time.time()

while True:
    if receive_thread.is_alive() == False:
        break
    #if space is pressed
    if keyboard.is_pressed('space') and sent == False: 
        #if time passed is greater than 0.5 seconds
        if time.time() - prevtime > 1:
            prevtime = time.time()
            print("sending image")
            adds = ('192.168.1.4', 1236)
            sock2.sendto(bytes(image), adds)
