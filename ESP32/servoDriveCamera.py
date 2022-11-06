import pca9865
import utime
import _thread
import ujson
import sys
import camera
import socket

SDA = 12
SCL = 13

drive = pca9865.pca9865(SDA, SCL)
STOP = 0

SOCK = 0
RECEIVER = 0

def sign(n):
    if n > 0:
        return 1
    elif n < 0:
        return -1
    else:
        return 0


# Smoothly move to the destination angle
currentMotor = 1
targetPoses = [0, 45, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
startingPoses = [0, 45, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
servos = [0, 45, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
INTERVAL = 10  # (milliseconds) lower value speeds up the movement but beware of the real speed of the thread, 0 will make it depend completely on thread's speed
INCREMENT = 2  # increase this to move faster when interval is at minimum possible
jsonPoses = [0, 45, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#camera.init(1)
#camera.framesize(camera.FRAME_QVGA)
 # The options are the following:
 # FRAME_96X96 FRAME_QQVGA FRAME_QCIF FRAME_HQVGA FRAME_240X240
 # FRAME_QVGA FRAME_CIF FRAME_HVGA FRAME_VGA FRAME_SVGA
 # FRAME_XGA FRAME_HD FRAME_SXGA FRAME_UXGA FRAME_FHD
 # FRAME_P_HD FRAME_P_3MP FRAME_QXGA FRAME_QHD FRAME_WQXGA
 # FRAME_P_FHD FRAME_QSXGA
 # Check this link for more information: https://bit.ly/2YOzizz
#camera.quality(10)

def power_all():
    global targetPoses, startingPoses, jsonPoses
    jsonPoses = [0, 45, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(16):
        drive.setangle(i, jsonPoses[i])

def move():
    global servos, targetPoses, STOP
    previousMillis = 0
    power_all()
    camera.init(1)
    camera.framesize(camera.FRAME_QVGA)
 # The options are the following:
 # FRAME_96X96 FRAME_QQVGA FRAME_QCIF FRAME_HQVGA FRAME_240X240
 # FRAME_QVGA FRAME_CIF FRAME_HVGA FRAME_VGA FRAME_SVGA
 # FRAME_XGA FRAME_HD FRAME_SXGA FRAME_UXGA FRAME_FHD
 # FRAME_P_HD FRAME_P_3MP FRAME_QXGA FRAME_QHD FRAME_WQXGA
 # FRAME_P_FHD FRAME_QSXGA
 # Check this link for more information: https://bit.ly/2YOzizz
    camera.quality(10)
    n = 0
    while not STOP:
        try:
            currentMillis = utime.ticks_ms()
            if (currentMillis - previousMillis >= INTERVAL):
                for i in range(16):
                    _pose = jsonPoses[i]
                    if (_pose is None):
                        continue
                    _pose = int(_pose)
                    _servo = servos[i]
                    '''
                    try: #THIS SLOWS EVERYTHING BY A LOT, it's better to be able to assume the json is valid
        targetPoses[i] = jsonPoses[str(i)]
    except:
        pass
                    '''
                    if (_servo != _pose):
                        deltaMove = _pose - _servo
                        if (abs(deltaMove) <= INCREMENT):
                            _servo = _pose
                        else:
                            _servo += INCREMENT * sign(deltaMove)
                        drive.setangle(i, _servo)
                        servos[i] = _servo
                        targetPoses[i] = _pose
                previousMillis = currentMillis
                #camera.capture() goes here
                try:
                    SOCK.sendto(cap(), (RECEIVER, 5555))
                    pass
                except:
                    print("camera error")
        except:
            print('movement error')
    drive.alloff()
    STOP = 2
    print('servoDrive.move() end\n')

def cap():
    buf = camera.capture()
    return buf

def resetMotors():
    global targetPoses, startingPoses, jsonPoses
    jsonPoses = [0, 45, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(16):
        targetPoses[i] = startingPoses[i]


def stop():
    global STOP
    drive.alloff()
    STOP = 1
    del sys.modules['servoDrive']
    print('Stopping servoDrive.move()')


_thread.start_new_thread(move, ())