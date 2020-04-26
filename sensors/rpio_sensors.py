import RPi.GPIO as GPIO

#GPIO Ports



#Light Sensor
def read_light(LIGHT_SENSOR):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LIGHT_SENSOR, GPIO.IN)
    return(GPIO.input(LIGHT_SENSOR))


#Touch Sensor
def get_touch_input(TOUCH_SENSOR):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TOUCH_SENSOR, GPIO.IN)
    return GPIO.input(TOUCH_SENSOR)


#Relay Pump (relay must be on 3.3v)

def pump_on(RELAY_SWITCH):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_SWITCH, GPIO.OUT)
    GPIO.output(RELAY_SWITCH,0)

def pump_off(RELAY_SWITCH):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_SWITCH, GPIO.OUT)
    GPIO.output(RELAY_SWITCH,1)




