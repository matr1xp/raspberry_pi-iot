#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This reads DS18B20 and DHT11 sensor data and sends it to Initial State 
(https://app.initialstate.com/)
for data analysis and visualization. Requires a valid account.
'''
import os, time, glob
import sys, signal
import Adafruit_DHT as DHT
from ISStreamer.Streamer import Streamer

streamer = Streamer(bucket_name="DS18B20/DHT11 Sensors", bucket_key="ds18b20dht11", access_key="<Insert your Access Key Here>")
dht_sensor = DHT.DHT11
dht_pin = 26

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

device_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(device_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_dht():
    humidity, temperature = DHT.read_retry(dht_sensor, dht_pin)
    return temperature, humidity

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

def signal_handler(signal, frame):
   streamer.log("Status", "offline")
   print("Process killed")

def cleanup():
   streamer.log("Status", "offline")
   streamer.close()
   sys.exit(0)

try:
   signal.signal(signal.SIGINT, signal_handler)
   streamer.log("Status", "online")

   while True:
      temp1, humidity = read_dht()
      temp2 = read_ds_temp() 
      streamer.log("DS_Temp", "{0:.2f}".format(round(temp2,2)))
      streamer.log("DH_Temp", temp1)
      streamer.log("Humidity", humidity)
      time.sleep(60)

   signal.pause()

except KeyboardInterrupt:
      print("Ctrl+C")
      cleanup()
except IOError:
      print("Error")
      cleanup()
