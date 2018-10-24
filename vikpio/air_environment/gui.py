#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Tkinter import *

from tkFont import Font as tk_font
import threading
import time
import serial
# import RPi.GPIO as GPIO
# import victoriest_gpio.dht11 as dht11
# import Adafruit_BMP.BMP085 as BMP085


time_now = lambda x: str(time.strftime('%H:%M:%S', time.localtime(x)))
days_now = lambda x: str(time.strftime('%Y/%b/%d %a', time.localtime(x)))

root = Tk()

w = 480
h = 320
root.geometry("%dx%d" % (w, h))
# root.attributes("-fullscreen", True)

ft1 = tk_font(family='Arial', size=40, weight="bold")
ft2 = tk_font(family='Arial', size=20, weight="bold")
ft3 = tk_font(family='Arial', size=15, weight="bold")
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)

frame = Frame(root)
frame.grid(row=0, column=0, sticky=N + S + E + W)

Grid.rowconfigure(frame, 0, weight=2)
Grid.columnconfigure(frame, 0, weight=3)
label1 = Label(frame, bg="white", text=time_now(time.time()), font=ft1)
label1.grid(row=0, column=0, columnspan=3, rowspan=2, sticky='wens', padx=2, pady=2)

Grid.rowconfigure(frame, 0, weight=1)
Grid.columnconfigure(frame, 3, weight=1)
label2 = Label(frame, bg="white", text="晴", font=ft3)
label2.grid(row=0, column=3, columnspan=1, rowspan=1, sticky='wens', padx=2, pady=2)

Grid.rowconfigure(frame, 1, weight=1)
Grid.columnconfigure(frame, 1, weight=1)
label3 = Label(frame, bg="white", text="- ℃", font=ft3)
label3.grid(row=1, column=3, columnspan=1, rowspan=1, sticky='wens', padx=2, pady=2)

Grid.rowconfigure(frame, 2, weight=1)
Grid.columnconfigure(frame, 0, weight=4)

label4 = Label(frame, bg="white", text=days_now(time.time()), font=ft2)
label4.grid(row=2, column=0, columnspan=3, rowspan=1, sticky='wens', padx=2, pady=2)

Grid.columnconfigure(frame, 3, weight=1)
label5 = Label(frame, bg="white", text="---℃", font=ft3)
label5.grid(row=2, column=3, columnspan=1, rowspan=1, sticky='wens', padx=2, pady=2)

Grid.rowconfigure(frame, 3, weight=1)
Grid.columnconfigure(frame, 0, weight=2)
label6 = Label(frame, bg="white", text="--------Pa", font=ft2)
label6.grid(row=3, column=0, columnspan=3, rowspan=1, sticky='wens', padx=2, pady=2)

Grid.columnconfigure(frame, 3, weight=1)
label7 = Label(frame, bg="white", text="RH: ----%", font=ft3)
label7.grid(row=3, column=3, columnspan=1, rowspan=1, sticky='wens', padx=2, pady=2)

Grid.rowconfigure(frame, 4, weight=1)
Grid.columnconfigure(frame, 0, weight=1)
label9 = Label(frame, bg="white", text="PM2.5: ----", font=ft2)
label9.grid(row=4, column=0, columnspan=2, rowspan=1, sticky='wens', padx=2, pady=2)

Grid.columnconfigure(frame, 2, weight=1)
labelA = Label(frame, bg="white", text="PM10: ----", font=ft2)
labelA.grid(row=4, column=2, columnspan=2, rowspan=1, sticky='wens', padx=2, pady=2)


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


# class DHT11SensorReader(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#
#     def run(self):
#         try:
#             GPIO.setwarnings(False)
#             GPIO.setmode(GPIO.BOARD)
#             GPIO.cleanup()
#             dht = dht11.DHT11(pin=38)
#             while 1:
#                 result = dht.read()
#                 thread_lock.acquire()
#                 if result.is_valid():
#                     label7.configure(text=("%d%%" % result.humidity))
#                 thread_lock.release()
#                 time.sleep(1)
#         except Exception, ex:
#             print ex


# class BMP085SensorReader(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#
#     def run(self):
#         try:
#             bmp = BMP085.BMP085()
#             idx = 0
#             while 1:
#                 idx += 1
#                 if idx > 10:
#                     idx = 0
#                     temp = bmp.read_temperature()
#                     pressure = bmp.read_pressure()
#                     thread_lock.acquire()
#                     label5.configure(text=("%.1f℃" % temp))
#                     label6.configure(text=("%.1fPa" % pressure))
#                     thread_lock.release()
#                 time.sleep(0.1)
#         except Exception, ex:
#             print ex


# class Pm25SensorReader(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#
#     def run(self):
#         try:
#             ser = serial.Serial("/dev/ttyUSB0", 9600)
#             while 1:
#                 time.sleep(1)
#                 count = ser.inWaiting()
#                 if count != 0:
#                     recv = ser.read(count)
#                     data = map(lambda c: ord(c), recv)
#                     if not check_data(data):
#                         ser.flushInput()
#                         continue
#                     pm2_5, pm10 = get_data(data)
#                     # 获得锁，成功获得锁定后返回True 可选的timeout参数不填时将一直阻塞直到获得锁定 否则超时后将返回False
#                     thread_lock.acquire()
#                     label9.configure(text="PM2.5: %.1f" % (pm2_5 / 10.0))
#                     labelA.configure(text="PM10: %.1f" % (pm10 / 10.0))
#                     thread_lock.release()
#                 ser.flushInput()
#             ser.close()
#         except Exception, ex:
#             print ex


def clock():
    label1.configure(text=time_now(time.time()))
    label4.configure(text=days_now(time.time()))
    root.after(200, clock)


thread_lock = threading.Lock()

# pm25_sensor_reader = Pm25SensorReader()
# pm25_sensor_reader.start()
# bmp_sensor_reader = BMP085SensorReader()
# bmp_sensor_reader.start()
# dht11_sensor_reader = DHT11SensorReader()
# dht11_sensor_reader.start()

clock()


def quit_callback(event):
    root.quit()


label1.bind("<Button-1>", quit_callback)

root.mainloop()

#GPIO.cleanup()
