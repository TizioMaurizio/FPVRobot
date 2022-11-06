# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import webrepl
webrepl.start()

import wifiConnect
from time import sleep
#wifiConnect.connect('TIM-37482183', 'HnbD76SPtLs7G8vS') #if network not found start Access Point mode
wifiConnect.connect('Xiaomi 11T Pro', 'mau12397') #if network not found start Access Point mode

import machine
import os
try:
    sleep(1)
    uos.mount(machine.SDCard(), "/sd")
    os.chdir("sd")
except:
    print("could not mount SD card")
