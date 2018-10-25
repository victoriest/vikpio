import threading
import time
import serial


class Pm25SensorReader(threading.Thread):
    PM_2_5_VALUE = 0
    PM_10_VALUE = 0

    def __init__(self, locker=None, dev_url="/dev/ttyUSB0"):
        threading.Thread.__init__(self)
        self._locker = locker
        self._dev_url = dev_url

    def run(self):
        try:
            ser = serial.Serial(self._dev_url, 9600)
            while 1:
                time.sleep(1)
                count = ser.inWaiting()
                if count != 0:
                    recv = ser.read(count)
                    data = map(lambda c: ord(c), recv)
                    if not self.check_data(data):
                        ser.flushInput()
                        continue
                    if self._locker is not None:
                        self._locker.acquire()
                    # label9.configure(text="PM2.5: %.1f" % (pm2_5 / 10.0))
                    # labelA.configure(text="PM10: %.1f" % (pm10 / 10.0))
                    Pm25SensorReader.PM_2_5_VALUE, Pm25SensorReader.PM_10_VALUE = self.get_data(data)
                    if self._locker is not None:
                        self._locker.release()
                ser.flushInput()
            ser.close()
        except Exception, ex:
            print ex

    @staticmethod
    def check_data(data):
        if data[0] != int('0xAA', 16):
            return False
        if data[6] != int('0xFF', 16):
            return False
        return True

    @staticmethod
    def get_data(data):
        pm2_5 = (data[1] << 8) | data[2]
        pm10 = (data[3] << 8) | data[4]
        print(pm2_5, pm10)
        return pm2_5, pm10
