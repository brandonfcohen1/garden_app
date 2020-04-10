from gpiozero import LightSensor
import RPi.GPIO as GPIO
from signal import pause

ldr = LightSensor(14)
GPIO.setup(15, GPIO.OUT, initial=GPIO.HIGH)


while True:
    print(ldr.value)
    if ldr.value < 0.1:
        GPIO.output(15,GPIO.LOW)
    else:
        GPIO.output(15,GPIO.HIGH)

