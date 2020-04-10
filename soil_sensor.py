import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
 
port = 14
GPIO.setup(port, GPIO.IN)


while True:
    if(GPIO.input(14)==GPIO.LOW):
        print("watery soil")
    else:
        print("Dry Soil")
