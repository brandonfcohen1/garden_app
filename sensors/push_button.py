
from gpiozero import Button, Buzzer
import Adafruit_DHT
from signal import pause


button = Button(15, pull_up = False)
buzz = Buzzer(14, initial_value=True)

def print_temp():
    hum,temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11,14)
    temp = temp*(9/5)+32
    print('temp    : %.1f' % temp)
    print('humidity: %.1f' % hum)

def sound_alarm():
    buzz.toggle()
    print(1)

#button.when_pressed = print_temp

button.when_pressed = sound_alarm

pause()