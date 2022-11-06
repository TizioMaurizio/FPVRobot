#python udp server on localhost
import socket
import sys
#thread
import threading
import time

#while true receive data
#create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#bind socket to localhost and port 10000
server_address = ('192.168.1.12', 1234)
sock.bind(server_address)
print('starting up on %s port %s' % sock.getsockname())
#start new thread for receiving data
def receive():
    while True:
        #if present print received data
        #print('waiting to receive message')
        data, address = sock.recvfrom(1234)
        #print('received %s bytes from %s' % (len(data), address))
        #print(data)
        #data decode string
        #if data is string "stop" break
        if data.decode() == "stop":
            sys.exit()
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
        print(data)

#launch receive thread
receive_thread = threading.Thread(target=receive)
receive_thread.start()


while True:
    if receive_thread.is_alive() == False:
        break
