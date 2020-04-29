# Garden App

During quarantine, I bought a <a href = "https://www.raspberrypi.org/products/raspberry-pi-4-model-b/" target="_blank"> Raspberry Pi</a> and <a href = "https://www.amazon.com/gp/product/B07TLRYGT1/ref=ppx_yo_dt_b_asin_title_o04_s01?ie=UTF8&psc=1" target="_blank"> some </a> <a href = "https://www.amazon.com/gp/product/B01J9GD3DG/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1" target="_blank"> sensors </a> from Amazon to learn about IoT programming. After some tinkering, I thought an interesting project to learn would be to build a self-watering garden. Then, I bought some <a href = "https://www.amazon.com/gp/product/B06ZY8JGJ4/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&psc=1" target="_blank"> seeds </a> in an attempt to make this useful for more than my own learning to try to actually grow some herbs.

Obviously, what I've done here is not the easiest, cheapest, or most effective way to grow herbs! I basically just built it to use any and all sensors I could. I don't even know if the herbs will grow well here, but it was a fun project (and I've got some seedlings coming in)! 

Also during quarantine, I wanted to beef up my web development skills, so built an API to which the pi can post the sensor readings, and a front-end which will render some cool graphics. Since I built the rest of the project in Python and it is my preferred programming language, I chose <a href="https://flask.palletsprojects.com/en/1.1.x/" target="_blank"> Flask </a> to build the web app. Flask is incredibly intuitive and simple to work with. I hosted the app on <a href = "https://www.heroku.com/" target="_blank"> Heroku </a>, since it is so simple to use and has a free "hobby" tier and used <a href = "https://www.postgresql.org/" target="_blank"> PostgreSQL</a> for the database which will store the readings.

The code for the app which manages the garden can be found <a href="https://github.com/brandonfcohen1/garden_app" target="_blank">here</a> on GitHub.



The main script which I keep constantly running is called program.py. 

The following configurations can be set at the start of the script:

*GPIO ports:*
```python
# Sensor Configs
HUMIDITY_SENSOR = 15
LIGHT_SENSOR = 14
TOUCH_SENSOR = 27
RELAY_SWITCH = 17
```

*Timing/sensitivity parameters:*
```python
# Program Configs
READING_FREQUENCY = 60*5            # Frequency with which to collect data, in seconds
TOUCH_SENSOR_CHECK_FREQUENCY = 10   # Frequency with which to check if the touch sensor has been pressed
DRY_SOIL_BENCHMARK = 800            # This is experimentally determined and should be tweaked over time
MAX_WATER_LEVEL = 758               # This is what the water sensor reads when the water is full
MIN_WATER_LEVEL = 650               # This is what the water sensor reads when the water is empty
LONG_PUMP_RUN = 1                   # How long to run the pump for (in seconds) when the soil is dry
SHORT_PUMP_RUN = 0.5                # How long to run the pump for (in seconds) when the touch sensor is pressed
POST_URL = 'https://cohengarden.herokuapp.com/api/add'

```

The script then defines a function get_all_readings() which pulls readings from each sensor:
```python
def get_all_readings():
    
     # The DHT11 sensor often fails. If this happens, try 5 more times before giving up and skipping the reading.
    humid = 32.0,0.0
    k=0
    while (humid[0] == 32.0) and (k < 5):
        humid = humidity_sensor.DHT11(pin = HUMIDITY_SENSOR).read().return_results()
        time.sleep(.3)
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
```
The only piece of this that is really of note is that the DHT11 sensor fails quite often, so I put it in a while loop to try a few times. Unfortunately, it will still fail from time to time.

In an infinite loop, I then take a reading, and run two checks to see if the pump should run (based on either soil moisture or pressing the touch sensor.
```python
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
    
```

Finally, I attempt to post this data to the API
```python
    try:
        r = requests.post(POST_URL, json = read)
        print(r.status_code)
    except:
        print('post failed at ' + str(time.time()))

```

This script pulls from several files in the /sensors folder. I used code from the following sources where noted:
* cpu_temp.py
* rpio_sensors.py
* humidity_sensor.py: *Adapted from http://osoyoo.com/driver/dht11-test.py*
* mcp3008.py: *Adapted from https://github.com/adafruit/Adafruit_Python_MCP3008/blob/master/examples/simpletest.py*
* barometric.py: *Adapted from Matt Hawkins, https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/bmp180.py*
