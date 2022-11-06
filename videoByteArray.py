#python udp server on localhost
import socket
import sys
#thread
import threading
import time
import cv2
import numpy as np

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
        frame = cv2.resize(frame, (0,0), fx=0.1, fy=0.1)
        images.append(frame)
        #read next frame
        ret, frame = cap.read()
    return images

#open cv2 widnow
cv2.namedWindow("preview")
x = videoToByteArray("The Wolf of the Wall Street (2013)_ Jordan's First Day at Wall Street (online-video-cutter.com).mp4")[1]
x = cv2.resize(x, (0,0), fx=0.3, fy=0.3)
#show first frame
cv2.imshow("preview", videoToByteArray("The Wolf of the Wall Street (2013)_ Jordan's First Day at Wall Street (online-video-cutter.com).mp4")[1])
#hold window open
cv2.waitKey(0)
image = []
#convert to byte array
for i in cv2.imencode('.png', x)[1]:
    image.append(i)
print(image)
#save image to file
#with open('wolf.txt', 'wb') as outfile:
    #convert image to string
    #outfile.write(str(image))