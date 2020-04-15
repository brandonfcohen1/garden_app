import time
from sensors.barometric_sensor import *
from sensors.cpu_temp import *
from sensors.rpio_sensors import *
from sensors.humidity_sensor import *
import requests
import time
import RPi.GPIO as GPIO

#Humidity Sensor Configs
HUMIDITY_SENSOR = 15



def get_all_readings():
    baro = read_barometric()
    cpu_temp = get_cpu_temp()
    light = read_light()
    humid = DHT11(pin = HUMIDITY_SENSOR).read().return_results()
    soil_moisture = 0
    GPIO.cleanup()
    return(
        {'baro_temp':baro[0],
         'baro_pressure': baro[1],
         'cpu_temp': cpu_temp,
         'humid_temp': humid[0],
         'humid_humid': humid[1],
         'light': light,
         'time': time.time(),
         "soil_moisture": soil_moisture
         }
        )


url = 'https://cohengarden.herokuapp.com/api/add'


while True:
    read = get_all_readings()
    print(read)
    r = requests.post(url, json = read)
    print(r.status_code)
    time.sleep(5)
