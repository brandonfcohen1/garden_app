import RPi.GPIO as GPIO


#GPIO Ports
#TOUCH_SENSOR = 15
#RELAY_SWITCH = 14
LIGHT_SENSOR = 14


#Initialize all settings
def initialize():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LIGHT_SENSOR, GPIO.IN)

    

#
##Touch Sensor
#GPIO.setup(TOUCH_SENSOR, GPIO.IN)
#def get_touch_input():
#    return GPIO.input(TOUCH_SENSOR)
#
#
##Relay Pump (relay must be on 3.3v)
#GPIO.setup(RELAY_SWITCH, GPIO.OUT)
#def pump_on():
#    GPIO.output(RELAY_SWITCH,0)
#
#def pump_off():
#    GPIO.output(RELAY_SWITCH,1)


#Light Sensor
def read_light(port_light):
    return(GPIO.input(port_light))


