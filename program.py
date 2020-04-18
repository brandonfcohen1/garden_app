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
    if humid[0]==32.0:
        time.sleep(3)
        #If reading fails, try one more time
        humid = DHT11(pin = HUMIDITY_SENSOR).read().return_results()
    soil_moisture = 0
    GPIO.cleanup()
    return(
        {'baro_temp': round(baro[0],2),
         'baro_pressure': round(baro[1],2),
         'cpu_temp': round(cpu_temp,2),
         'humid_temp': round(humid[0],2),
         'humid_humid': round(humid[1],2),
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
    time.sleep(60)
