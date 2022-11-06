import camera
import socket
import time
import network
camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)
def start(ip,port):
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((network.WLAN().ifconfig()[0],port))
    while True:
        time.sleep(0.1)
        s.sendto(camera.capture(),(ip,port))
