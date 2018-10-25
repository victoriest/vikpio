#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Tkinter import *
from tkFont import Font as tk_font
import threading
import time
import queue
import random


# from vikpio.senor.dht11.dht11_reader import DHT11SensorReader
# from vikpio.senor.bmp085.bmp085 import BMP085SensorReader
# from vikpio.senor.pm25.pm25 import Pm25SensorReader


class Data:
    def __init__(self, hu=0, tp=0, pressure=0, pm25=0, pm10=0):
        self.hu = hu
        self.tp = tp
        self.pressure = pressure
        self.pm25 = pm25
        self.pm10 = pm10


def time_now():
    return str(time.strftime('%H:%M:%S', time.localtime(time.time())))


def days_now():
    return str(time.strftime('%Y/%b/%d %a', time.localtime(time.time())))


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
label1 = Label(frame, bg="white", text=time_now(), font=ft1)
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

label4 = Label(frame, bg="white", text=days_now(), font=ft2)
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

thread_lock = threading.Lock()

# pm25_sensor_reader = Pm25SensorReader(locker=thread_lock)
# pm25_sensor_reader.start()
# bmp_sensor_reader = BMP085SensorReader(locker=thread_lock)
# bmp_sensor_reader.start()
# dht11_sensor_reader = DHT11SensorReader(locker=thread_lock)
# dht11_sensor_reader.start()


q = []


def random_data_for_test():
    data = Data()
    data.pm10 = random.randrange(200, 2000)
    data.pm25 = random.randrange(100, 1800)
    data.hu = random.uniform(50.0, 100.0)
    data.tp = random.uniform(18.0, 25.0)
    data.pressure = random.uniform(101325.0 - 100, 101325.0 + 100)
    return data


for i in range(86400):
    q.append(random_data_for_test())


def clock():
    label1.configure(text=time_now())
    label4.configure(text=days_now())

    d = random_data_for_test()
    q.append(d)
    if len(q) > 86400:
        q.pop(0)

    label5.configure(text=("%.1f℃" % d.tp))
    label6.configure(text=("%.1fPa" % d.pressure))
    label7.configure(text=("%d%%" % d.hu))
    label9.configure(text="PM2.5: %.1f" % (d.pm25 / 10.0))
    labelA.configure(text="PM10: %.1f" % (d.pm10 / 10.0))

    # label5.configure(text=("%.1f℃" % BMP085SensorReader.TEMPERATURE_VALUE))
    # label6.configure(text=("%.1fPa" % BMP085SensorReader.PRESSURE_VALUE))
    # label7.configure(text=("%d%%" % DHT11SensorReader.HUMIDITY_VALUE.humidity))
    # label9.configure(text="PM2.5: %.1f" % (Pm25SensorReader.PM_2_5_VALUE / 10.0))
    # labelA.configure(text="PM10: %.1f" % (Pm25SensorReader.PM_10_VALUE / 10.0))
    root.after(1000, clock)


clock()


def show_chart(fuc):
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt

    f = plt.figure(figsize=(5, 4))
    plt.subplot(111)

    data = []
    ti = []

    n = 0
    avg = 0
    for i, val in enumerate(q):
        if n > 720:
            ti.append(i)
            data.append(avg / n)
            n = 0
            avg = 0
        avg += fuc(val)
        n += 1

    plt.plot(ti, data, color='blue', linewidth=1.0, linestyle='-')
    #
    # # 设置x轴和y轴范围
    # plt.xlim(-4.0, 4.0)
    # plt.ylim(-1.0, 1.0)
    #
    # # 设置x轴下标和y轴下标
    # plt.xticks(np.linspace(-4, 4, 9, endpoint=True))
    # plt.yticks(np.linspace(-1, 1, 5, endpoint=True))

    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=1)

    def on_button_press_event(event):
        canvas.get_tk_widget().destroy()
        plt.close("all")

    canvas.mpl_connect('button_press_event', on_button_press_event)


label5.bind("<Button-1>", lambda e: show_chart(lambda x: x.tp))
label6.bind("<Button-1>", lambda e: show_chart(lambda x: x.pressure))
label7.bind("<Button-1>", lambda e: show_chart(lambda x: x.hu))
label9.bind("<Button-1>", lambda e: show_chart(lambda x: x.pm25))
labelA.bind("<Button-1>", lambda e: show_chart(lambda x: x.pm10))


root.mainloop()
