import RPi.GPIO as GPIO

#GPIO Ports
LIGHT_SENSOR = 14



def read_light():
    #GPIO Setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LIGHT_SENSOR, GPIO.IN)
    return(GPIO.input(LIGHT_SENSOR))



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




