import camera
import socket
import time
import network
from machine import UART
uart = UART(1,115200,tx=2,rx=13)
camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)
def start(ip,port):
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sReceive=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((network.WLAN().ifconfig()[0],port))
    sReceive.bind((network.WLAN().ifconfig()[0],port-1))
    while True:
        time.sleep(0.1)
        s.sendto(camera.capture(),(ip,port))
        data, address = sReceive.recvfrom(100)
        uart.write(data.decode())
