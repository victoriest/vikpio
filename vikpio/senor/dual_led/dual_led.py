# -*- coding: UTF-8 -*-

import RPi.GPIO as GPIO
import time


class DualLed(object):
    __r_pin__ = 11
    __g_pin__ = 12

    def __init__(self, r_pin=11, g_pin=12):
        DualLed.__r_pin__ = r_pin
        DualLed.__g_pin__ = g_pin

        GPIO.setmode(GPIO.BOARD)

        GPIO.cleanup(DualLed.__r_pin__)
        GPIO.cleanup(DualLed.__g_pin__)

        GPIO.setup(DualLed.__r_pin__, GPIO.OUT)
        GPIO.setup(DualLed.__g_pin__, GPIO.OUT)

    def __del__(self):
        GPIO.cleanup(DualLed.__r_pin__)
        GPIO.cleanup(DualLed.__g_pin__)

    def lightRed(self, lightUp=True):
        if lightUp:
            GPIO.output(DualLed.__r_pin__, 1)
        else:
            GPIO.output(DualLed.__r_pin__, 0)

    def lightGreen(self, lightUp=True):
        if lightUp:
            GPIO.output(DualLed.__g_pin__, 1)
        else:
            GPIO.output(DualLed.__g_pin__, 0)

    def breatheLightRed(self):
        # 通道为 11 频率为 50Hz
        p = GPIO.PWM(DualLed.__r_pin__, 50)
        p.start(0)
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
        p.stop()
