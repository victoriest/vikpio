# -*- coding: UTF-8 -*-
import threading
import RPi.GPIO as GPIO
import dht11
import time


class DHT11SensorReader(threading.Thread):
    HUMIDITY_VALUE = 0

    def __init__(self, locker=None, pin=38):
        threading.Thread.__init__(self)
        self._pin = pin
        self._locker = locker

    def run(self):
        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            GPIO.cleanup()
            dht = dht11.DHT11(pin=self._pin)
            while 1:
                result = dht.read()

                if self._locker is not None:
                    self._locker.acquire()
                if result.is_valid():
                    DHT11SensorReader.HUMIDITY_VALUE = result.humidity
                    # label7.configure(text=("%d%%" % result.humidity))
                if self._locker is not None:
                    self._locker.release()

                time.sleep(1)
        except Exception, ex:
            print ex
