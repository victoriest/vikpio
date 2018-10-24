import RPi.GPIO as GPIO
from vikpio.senor.dht11 import dht11


if __name__ == "__main__":
    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.cleanup()

    # read data using pin 14
    instance = dht11.DHT11(pin=22)
    result = instance.read()

    if result.is_valid():
        print("Temperature: %d C" % result.temperature)
        print("Humidity: %d %%" % result.humidity)
    else:
        print("Error: %d" % result.error_code)
