import time
import requests
import RPi.GPIO as GPIO
import sensors.barometric_sensor
import sensors.cpu_temp
import sensors.rpio_sensors
import sensors.humidity_sensor
import sensors.mcp3008


#Sensor Configs
HUMIDITY_SENSOR = 15
LIGHT_SENSOR = 14


#Program Configs
READING_FREQUENCY = 60*5
DRY_SOIL_BENCHMARK = 800     #This is experimentally determined and should be tweaked over time


def get_all_readings():
    
    #The DHT11 sensor often fails. If this happens, try two more times before giving up and skipping the reading.
    humid = 32.0,0.0
    k=0
    while (humid[0] == 32.0) and (k < 3):
        humid = humidity_sensor.DHT11(pin = HUMIDITY_SENSOR).read().return_results()
        k+=1
     
    baro = barometric_sensor.read_barometric()
    cpu_temp = cpu_temp.get_cpu_temp()
    light = rpio_sensors.read_light()
    
    
    soil_moisture = mcp3008.read_mcp3008(0)
    water_level = mcp3008.read_mcp3008(1)
    pump_status = 0
    
    #Clean up GPIO board
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
        
    time.sleep(READING_FREQUENCY)
