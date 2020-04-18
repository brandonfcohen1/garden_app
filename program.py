import time
from sensors.barometric_sensor import *
from sensors.cpu_temp import *
from sensors.rpio_sensors import *
from sensors.humidity_sensor import *
from sensors.mcp3008 import *
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
    soil_moisture = read_mcp3008(0)
    water_level = read_mcp3008(1)
    pump_status = 0
    GPIO.cleanup()
    return(
        {'baro_temp': round(baro[0],2),
         'baro_pressure': round(baro[1],2),
         'cpu_temp': round(cpu_temp,2),
         'humid_temp': round(humid[0],2),
         'humid_humid': round(humid[1],2),
         'light': light,
         'time': time.time(),
         "soil_moisture": soil_moisture,
         "water_level": water_level,
         "pump_status": pump_status
         }
        )


url = 'https://cohengarden.herokuapp.com/api/add'


while True:
    read = get_all_readings()
    print(read)
    
    try:
        r = requests.post(url, json = read)
        print(r.status_code)
    except:
        print('post failed at ' + str(time.time()))
        
    time.sleep(60)
