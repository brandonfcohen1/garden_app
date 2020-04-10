import RPi.GPIO as GPIO
from signal import pause

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)


while True:
    print(GPIO.input(14))

