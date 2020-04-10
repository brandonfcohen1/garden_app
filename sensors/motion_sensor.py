import glob
import time
import pandas as pd
import os
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(14,GPIO.IN)

def get_motion():
    return(GPIO.input(14))

 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f



def get_cpu_temp():
        cpu = os.popen("vcgencmd measure_temp").readline()
        return (cpu.replace("temp=",""))

temp = []
motion = []
timestamp = []
cpu_temp=[]

for t in range(0,60*60):
    temp.append(read_temp())
    motion.append(get_motion())
    timestamp.append(time.time())
    cpu_temp.append(get_cpu_temp())
    print(t)
    time.sleep(1)

result = pd.DataFrame({'timestamp':timestamp,'motion':motion,'temp':temp, 'cpu_temp':cpu_temp})
result.to_csv('result.csv')