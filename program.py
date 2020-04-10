import pandas as pd
from sensors.barometric_sensor import *
from sensors.cpu_temp import *
from sensors.rpio_sensors import *
from sensors.humidity_sensor import *
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

#GPIO Ports
LIGHT_SENSOR = 14
HUMIDITY_SENSOR = 15

humidity_reading = DHT11(pin = HUMIDITY_SENSOR)
print(humidity_reading.read().humidity)