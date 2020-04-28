import time
import requests
import RPi.GPIO as GPIO
import sensors.barometric_sensor as barometric_sensor
import sensors.cpu_temp as cpu_temp
import sensors.rpio_sensors as rpio_sensors
import sensors.humidity_sensor as humidity_sensor
import sensors.mcp3008 as mcp3008
from signal import pause


# Sensor Configs
HUMIDITY_SENSOR = 15
LIGHT_SENSOR = 14
TOUCH_SENSOR = 27
RELAY_SWITCH = 17

# Program Configs
READING_FREQUENCY = 60*5            # Frequency with which to collect data, in seconds
TOUCH_SENSOR_CHECK_FREQUENCY = 10   # Frequency with which to check if the touch sensor has been pressed
DRY_SOIL_BENCHMARK = 800            # This is experimentally determined and should be tweaked over time
MAX_WATER_LEVEL = 758               # This is what the water sensor reads when the water is full
MIN_WATER_LEVEL = 249               # This is what the water sensor reads when the water is empty
LONG_PUMP_RUN = 1                   # How long to run the pump for (in seconds) when the soil is dry
SHORT_PUMP_RUN = 0.5                # How long to run the pump for (in seconds) when the touch sensor is pressed
POST_URL = 'https://cohengarden.herokuapp.com/api/add'

# READING_FREQUENCY must be divisible by TOUCH_SENSOR_CHECK_FREQUENCY
if READING_FREQUENCY % TOUCH_SENSOR_CHECK_FREQUENCY != 0:
    raise ValueError("READING_FREQUENCY must be divisible by TOUCH_SENSOR_CHECK_FREQUENCY")


def get_all_readings():
    
    # The DHT11 sensor often fails. If this happens, try 3 more times before giving up and skipping the reading.
    humid = 32.0,0.0
    k=0
    while (humid[0] == 32.0) and (k < 4):
        humid = humidity_sensor.DHT11(pin = HUMIDITY_SENSOR).read().return_results()
        GPIO.cleanup()
        k+=1
     
    baro = barometric_sensor.read_barometric()
    cpu_t = cpu_temp.get_cpu_temp()
    light = rpio_sensors.read_light(LIGHT_SENSOR)
    
    
    soil_moisture = mcp3008.read_mcp3008(0)
    water_level = (mcp3008.read_mcp3008(1) - MIN_WATER_LEVEL)/(MAX_WATER_LEVEL - MIN_WATER_LEVEL) 
    
    # Pump status will be set during program run
    pump_status = 0
    
    # Clean up GPIO board
    GPIO.cleanup()
    
    return(
        {'baro_temp': round(baro[0],2),
         'baro_pressure': round(baro[1],2),
         'cpu_temp': round(cpu_t,2),
         'humid_temp': round(humid[0],2),
         'humid_humid': round(humid[1],2),
         'light': light,
         'time': time.time(),
         "soil_moisture": soil_moisture,
         "water_level": round(water_level,2)*100,
         "pump_status": pump_status
         }
        )



last_run = 0 #Initialize this variable which will store the last time the pump was on
while True:
    read = get_all_readings()
    print(read)
    
    # If the soil moisture is above the benchmark (drier), run the pump for LONG_PUMP_RUN second.
    # I am worried about a lag in the moisture sensor picking up the change in moisture content and I don't want to over-water.
    # Therefore, I only want the program to water once per day, which will be checked for using the "last_run" variable
    if (time.time() - last_run > 60*60*24) and (read["soil_moisture"] > DRY_SOIL_BENCHMARK):
        rpio_sensors.pump_on(RELAY_SWITCH)
        time.sleep(LONG_PUMP_RUN)
        rpio_sensors.pump_off(RELAY_SWITCH)
        read["pump_status"] = 1 #Set the pump status to ON during this interval
        last_run = time.time() #Set the last time the pump was run
        time.sleep(TOUCH_SENSOR_CHECK_FREQUENCY - LONG_PUMP_RUN)
        GPIO.cleanup()
    
    # I also want the ability to manually run the pump using the touch sensor
    # Every TOUCH_SENSOR_CHECK_FREQUENCY seconds the program will check to see if the touch sensor has been pressed
    # If it has (regardless of when the pump was last run), run the pump for SHORT_PUMP_RUN seconds
    for i in range(0,int(READING_FREQUENCY/TOUCH_SENSOR_CHECK_FREQUENCY)):
        p = rpio_sensors.get_touch_input(TOUCH_SENSOR)
        if p == 1:
            rpio_sensors.pump_on(RELAY_SWITCH)
            time.sleep(SHORT_PUMP_RUN)
            rpio_sensors.pump_off(RELAY_SWITCH)
            read["pump_status"] = 1
            time.sleep(TOUCH_SENSOR_CHECK_FREQUENCY - SHORT_PUMP_RUN)
            GPIO.cleanup()
        else:
            time.sleep(TOUCH_SENSOR_CHECK_FREQUENCY)
    

    
    try:
        r = requests.post(POST_URL, json = read)
        print(r.status_code)
    except:
        print('post failed at ' + str(time.time()))
        
    
