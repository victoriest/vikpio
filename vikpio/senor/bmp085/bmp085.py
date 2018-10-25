import threading
import Adafruit_BMP.BMP085 as BMP085
import time


class BMP085SensorReader(threading.Thread):
    TEMPERATURE_VALUE = 0
    PRESSURE_VALUE = 0
    ALTITUDE_VALUE = 0

    def __init__(self, locker=None):
        threading.Thread.__init__(self)
        self._locker = locker

    def run(self):
        try:
            bmp = BMP085.BMP085()
            idx = 0
            while 1:
                idx += 1
                if idx > 10:
                    idx = 0
                    if self._locker is not None:
                        self._locker.acquire()

                    BMP085SensorReader.TEMPERATURE_VALUE = bmp.read_temperature()
                    BMP085SensorReader.PRESSURE_VALUE = bmp.read_pressure()
                    BMP085SensorReader.ALTITUDE_VALUE = bmp.read_altitude()
                    if self._locker is not None:
                        self._locker.release()

                time.sleep(0.1)
        except Exception, ex:
            print ex
