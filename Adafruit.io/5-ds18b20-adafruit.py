#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This reads DS18B20 sensor data and sends it to Adafruit.io (https://adafruit.io/)
for data analysis and visualization. Requires a valid account.
'''
import sys, os, time, glob
from Adafruit_IO import Client

INTERVAL = 30
aio = Client('dec373cb22994ee094a33f22f3f7a0e2')

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

device_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(device_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_raw_temperature():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temperature():
    lines = read_raw_temperature()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.5)
        lines = read_raw_temperature()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_str = lines[1][equals_pos+2:]
        temp_c = float(temp_str) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

try:
   while True:
      temp = read_temperature()
      temp_c = "{0:.2f}".format(round(temp[0],2))
      aio.send('ds18b20-temp', temp_c)
      time.sleep(INTERVAL)
except KeyboardInterrupt:
      print("Ctrl+C pressed... exiting.")
      sys.exit(0) 
except:
      print("Error: {0} {1}".format(sys.exc_info()[0], sys.exc_info()[1]))

