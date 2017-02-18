#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  DS18B20 Temperature sensor
#
import os, time, glob

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
    temp_c = "{0:.2f}°C".format(round(temp[0],2))
    temp_f = "{0:.2f}°F".format(round(temp[1],2))
    print("Temperature is " + temp_c + " or " + temp_f)
    time.sleep(1)
except KeyboardInterrupt:
    print("<Ctrl+C> pressed... exiting.")

