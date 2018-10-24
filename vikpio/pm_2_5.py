#!/usr/bin/python
#encoding=utf-8
import serial
import time
import json
import requests
import copy

# 起始位  PM2.5(H)  PM2.5(L)  PM10(H)  PM10(L)  校验位  结束位
# 0xAA   如:0x01    如:0xE0   如:0x01  如 0xFA   0xDC   0xFF
# 7 个字节，其中校验位=PM2.5(H)+PM2.5(L)+PM10(H)+PM10(L)。

def pm():
    ser = serial.Serial("/dev/ttyAMA0", 9600)
    while True:
        time.sleep(0.1)
        count = ser.inWaiting()
        if count >= 7:
            recv = ser.read(count)
            data = map(lambda c: ord(c), recv)
            if check_data(data) != True:
                ser.flushInput()
                continue
            iii = get_data(data)
            return iii
        ser.flushInput()
    ser.close()
    return 0, 0


def check_data(data):
        if data[0] != int('0xAA', 16):
                return False
        if data[6] != int('0xFF', 16):
                return False
        return True


def get_data(data):
        pm2_5 = (data[1] << 8) | data[2]
        pm10 = (data[3] << 8) | data[4]
        print(pm2_5, pm10)
        return pm2_5, pm10


if __name__ == '__main__':
        pm2_5, pm10 = pm()
