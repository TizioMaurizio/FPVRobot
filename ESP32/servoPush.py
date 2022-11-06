try:
    from machine import Pin, PWM
    from time import sleep
    servoPin = PWM(Pin(13))
    servoPin.freq(50)
    def servo(degrees):
        if degrees > 180: degrees=180
        if degrees < 0: degrees=0
        maxDuty=9000
        minDuty=1000
        newDuty=minDuty+(maxDuty-minDuty)*(degrees/180)
        servoPin.duty_u16(int(newDuty))
        
    def servoPush(start, end, delay):
        print("push")
        servo(start)
        sleep(delay)
        servo(end)
        print("retract")
    print("servoPush loaded correctly")   
    
except:
    print("servoPush not loaded")