from rpio_sensors import *
from signal import pause
import time

#Sensor Configs
HUMIDITY_SENSOR = 15
LIGHT_SENSOR = 14
TOUCH_SENSOR = 21
RELAY_SWITCH = 17

while True:
    p = get_touch_input(TOUCH_SENSOR)
    if p == 1:
        pump_on(RELAY_SWITCH)
        time.sleep(1)
        pump_off(RELAY_SWITCH)
    else:
        pump_off(RELAY_SWITCH)
    
    time.sleep(.5)


