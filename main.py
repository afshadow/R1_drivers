import os
import time
from Extension.ina219 import logUPSStatus

from machine import Pin

led = Pin(25, Pin.OUT)

os.listdir()

if __name__=='__main__':

    while True:
        led(1)
        time.sleep(1)
        led(0)
        time.sleep(1)
        logUPSStatus()
