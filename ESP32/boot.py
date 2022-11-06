# Complete project details at https://RandomNerdTutorials.com

import webrepl
webrepl.start()
import network
import time

try:
  import usocket as socket
except:
  import socket

from machine import Pin

def do_connect(ssid, password):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

import esp
esp.osdebug(None)

import gc
gc.collect()

#ssid = 'TIM-37482183-5G'
#password = 'HnbD76SPtLs7G8vS'
#ssid = 'Xiaomi 11T Pro'
#password = 'mau12397'
#ssid = 'RedmiMau'
#password = 'mau12397'
#ssid = 'LenovoTizio'
#password = 'tizio1234'
import defaultWifi
ssid = defaultWifi.ssid
password = defaultWifi.password

do_connect(ssid, password)

#led = Pin(2, Pin.OUT)

#try:
    #uos.mount(machine.SDCard(), '/sd')
    #uos.chdir('sd')
#except:
    #print('could not mount SD card')
