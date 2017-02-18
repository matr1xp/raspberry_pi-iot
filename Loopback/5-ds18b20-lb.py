#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, time, datetime, glob
import sys 
import requests

INTERVAL = 60

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

device_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(device_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

api_url = 'http://0.0.0.0:3000/api/'

def read_raw_temp():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_ds_temp():
    lines = read_raw_temp()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.5)
        lines = read_raw_temp()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_str = lines[1][equals_pos+2:]
        temp_c = float(temp_str) / 1000.0
        return temp_c   

def cleanup():
   sys.exit(0)

try:
   while True:
      temp = read_ds_temp() 
      temperature = float("{0:.2f}".format(temp))
      timestamp = "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())
      ds18b20_payload = {'temperature': temperature, 'timestamp': timestamp}
      requests.post(api_url+'DS18B20', ds18b20_payload)
      time.sleep(INTERVAL)
except KeyboardInterrupt:
      print("Ctrl+C pressed... exiting.")
      cleanup()
except requests.exceptions.ConnectionError:
      print("Loopback Connection Error. Please ensure that "+api_url+" is running.")
      cleanup()
except IOError:
      print("IOError. Please check your sensor GPIO configuration.")
      cleanup()
