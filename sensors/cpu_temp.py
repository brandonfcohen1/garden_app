import os

def get_cpu_temp():
    temp = os.popen('/opt/vc/bin/vcgencmd measure_temp').read()
    tempF = int(temp[5:7])*(9.0/5.0) + 32.0
    return(tempF)

