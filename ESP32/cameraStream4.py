import camera
import socket
import time
import network
import _thread

def receiver():
    from machine import UART
    uart = UART(1,115200,tx=2,rx=13)
    sReceive=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sReceive.bind((network.WLAN().ifconfig()[0],1233))
    while True:
        data, address = sReceive.recvfrom(100)
        uart.write(data.decode())
    
camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)
def start(ip,port):
    _thread.start_new_thread(receiver,())
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((network.WLAN().ifconfig()[0],port))
    while True:
        time.sleep(0.1)
        s.sendto(camera.capture(),(ip,port))
