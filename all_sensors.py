import RPi.GPIO as GPIO
import time



#Initialize BCM
GPIO.setmode(GPIO.BCM)

#GPIO Ports
TOUCH_SENSOR = 15
RELAY_SWITCH = 14


#Touch Sensor
GPIO.setup(TOUCH_SENSOR, GPIO.IN)
def get_touch_input():
    return GPIO.input(TOUCH_SENSOR)


#Relay Pump (relay must be on 3.3v)
GPIO.setup(RELAY_SWITCH, GPIO.OUT)
def pump_on():
    GPIO.output(RELAY_SWITCH,0)

def pump_off():
    GPIO.output(RELAY_SWITCH,1)
