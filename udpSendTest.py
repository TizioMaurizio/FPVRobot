import socket
import cv2
import numpy as np
import time
import sys
import threading
import serial.tools.list_ports
import keyboard

MY_IP = '192.168.43.183'
sockSendAngles = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (MY_IP, 1233)
sockSendAngles.bind(server_address)

esp = str(socket.gethostbyname('espressif'))
print(esp)
adds=(esp,1233)
sockSendAngles.sendto("s090000000075000000000000000000000000000000000000\n".encode('utf-8'), adds)