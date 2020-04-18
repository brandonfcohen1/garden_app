import Adafruit_MCP3008
import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
 
port = 17
GPIO.setup(port, GPIO.OUT)
GPIO.output(port,1)

CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

def read_moisture():
    return(mcp.read_adc(0))


while True:
    m = read_moisture()
    print(m)
    if m > 800:
        GPIO.output(port,0)
        time.sleep(3)
        GPIO.output(port,1)
    
    time.sleep(5)