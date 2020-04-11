import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
 
port = 15
GPIO.setup(port, GPIO.OUT)

#Turn on
GPIO.output(port,1)
time.sleep(3)

#Turn off
GPIO.output(port,1)