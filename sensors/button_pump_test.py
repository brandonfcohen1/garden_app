from rpio_sensors import *
from signal import pause
import time
import RPi.GPIO as GPIO

#Sensor Configs
HUMIDITY_SENSOR = 15
LIGHT_SENSOR = 14
TOUCH_SENSOR = 27
RELAY_SWITCH = 17




print(get_touch_input(TOUCH_SENSOR))