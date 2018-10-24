# -*- coding: UTF-8 -*-
import threading
import RPi.GPIO as GPIO
import dht11
import time

dht11_humidity_value = 0


class DHT11SensorReader(threading.Thread):
    def __init__(self, pin=38, locker=None):
        threading.Thread.__init__(self)
        self._pin = pin
        self._locker = locker

    def run(self):
        global dht11_humidity_value
        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            GPIO.cleanup()
            dht = dht11.DHT11(pin=38)
            while 1:
                result = dht.read()

                if self._locker is not None:
                    self._locker.acquire()
                if result.is_valid():
                    dht11_humidity_value = result.humidity
                    # label7.configure(text=("%d%%" % result.humidity))
                if self._locker is not None:
                    self._locker.release()

                time.sleep(1)
        except Exception, ex:
            print ex
