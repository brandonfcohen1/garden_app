#!/usr/bin/python
 
from Adafruit_BMP085 import BMP085
 

bmp = BMP085(0x77)
 

 
temp = bmp.readTemperature()
 
# Read the current barometric pressure level
pressure = bmp.readPressure()
 
# To calculate altitude based on an estimated mean sea level pressure
# (1013.25 hPa) call the function as follows, but this won't be very accurate
altitude = bmp.readAltitude()
 
# To specify a more accurate altitude, enter the correct mean sea level
# pressure level.  For example, if the current pressure level is 1023.50 hPa
# enter 102350 since we include two decimal places in the integer value
# altitude = bmp.readAltitude(102350)
 
