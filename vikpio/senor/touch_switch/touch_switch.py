#!/usr/bin/env python
import RPi.GPIO as GPIO


class TouchSwitch(object):
    __touch_pin__ = 13

    __key_up_callback__ = []
    __key_down_callback__ = []

    @classmethod
    def __on_key_event__(cls, channel):
        if GPIO.input(TouchSwitch.__touch_pin__) == 1:
            for c in TouchSwitch.__key_down_callback__:
                c()
        else:
            for c in TouchSwitch.__key_up_callback__:
                c()

    def __init__(self, touch_pin=13):
        TouchSwitch.__touch_pin__ = touch_pin
        print self.__touch_pin__
        print TouchSwitch.__touch_pin__
        GPIO.setmode(GPIO.BOARD)

        GPIO.cleanup(TouchSwitch.__touch_pin__)
        # Set BtnPin's mode is input, and pull up to high level(3.3V)
        GPIO.setup(TouchSwitch.__touch_pin__, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(TouchSwitch.__touch_pin__, GPIO.BOTH,
                              callback=TouchSwitch.__on_key_event__, bouncetime=100)

    def __del__(self):
        GPIO.remove_event_detect(TouchSwitch.__touch_pin__)
        GPIO.cleanup(TouchSwitch.__touch_pin__)

    def addKeyUpEvent(self, callback):
        TouchSwitch.__key_up_callback__.append(callback)

    def addKeyDownEvent(self, callback):
        TouchSwitch.__key_down_callback__.append(callback)

    def removeKeyUpEvent(self, callback):
        TouchSwitch.__key_up_callback__.remove(callback)

    def removeKeyDownEvent(self, callback):
        TouchSwitch.__key_down_callback__.remove(callback)

# tmp = 0
#
# 
# def Led(x):
#     if x == 0:
#         GPIO.output(Rpin, 1)
#         GPIO.output(Gpin, 0)
#     if x == 1:
#         GPIO.output(Rpin, 0)
#         GPIO.output(Gpin, 1)
#
#
# def Print(x):
#     global tmp
#     if x != tmp:
#         if x == 0:
#             print '    **********'
#             print '    *     ON *'
#             print '    **********'
#
#         if x == 1:
#             print '    **********'
#             print '    * OFF    *'
#             print '    **********'
#         tmp = x
#
#
# def loop():
#     while True:
#         Led(GPIO.input(TouchPin))
#         Print(GPIO.input(TouchPin))
#
#
# def destroy():
#     GPIO.output(Gpin, GPIO.HIGH)  # Green led off
#     GPIO.output(Rpin, GPIO.HIGH)  # Red led off
#     GPIO.cleanup()  # Release resource
#
#
# if __name__ == '__main__':  # Program start from here
#     setup()
#     try:
#         loop()
#     except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
#         destroy()
