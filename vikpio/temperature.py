# -*- coding: UTF-8 -*-

import time

import Adafruit_BMP.BMP085 as BMP085
import RPi.GPIO as GPIO

from vikpio.senor.lcd1602 import LCD1602
from vikpio.senor.dht11 import dht11

dht = None
bmp = None


def init():
    global dht
    global bmp
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.cleanup()

    LCD1602.init(0x27, 1)
    LCD1602.clear()

    bmp = BMP085.BMP085()

    dht = dht11.DHT11(pin=22)
    result = dht.read()

    if result.is_valid():
        print("Temperature: %d C" % result.temperature)
        print("Humidity: %d %%" % result.humidity)
    else:
        print("Error: %d" % result.error_code)


idx = 0
temp = 0


def loop():
    global idx
    global dht
    global bmp
    global temp
    idx += 1
    if idx > 10:
        try:
            idx = 0

            # Read temperature to veriable temp
            temp = bmp.read_temperature()
            # Read pressure to veriable pressure
            pressure = bmp.read_pressure()
            result = dht.read()
            if result.is_valid():
                LCD1602.write(1, 1, "%d%%, %.1fPa" % (result.humidity, pressure))
                with open('./temperature.txt', 'w') as f:
                    f.write("%.1f\n%d\n%.1f" % (temp, result.humidity, pressure))
        except AttributeError:
            pass

    time_str = time.strftime("%H:%M", time.localtime())
    LCD1602.write(0, 0, "%s %.1fC" % (time_str, temp))

    time.sleep(0.1)


if __name__ == "__main__":
    try:
        init()
        while True:
            loop()
    except KeyboardInterrupt:
        LCD1602.clear()
        GPIO.cleanup()
