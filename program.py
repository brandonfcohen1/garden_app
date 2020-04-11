import pandas as pd
from sensors.barometric_sensor import *
from sensors.cpu_temp import *
from sensors.rpio_sensors import *
from sensors.humidity_sensor import *

#Humidity Sensor Configs
HUMIDITY_SENSOR = 15


def get_all_readings():
    baro = read_barometric()
    cpu_temp = get_cpu_temp()
    humid = DHT11(pin = HUMIDITY_SENSOR).read().return_results()
    light = read_light()
    return(baro, cpu_temp, humid, light)

x = get_all_readings()