#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, time, datetime, glob
import sys 
import requests
import Adafruit_BMP.BMP085 as BMP085

api_url = 'http://0.0.0.0:3000/api/'

def cleanup():
   sys.exit(0)

try:
   sensor = BMP085.BMP085()
   while True:
      temperature = sensor.read_temperature()
      altitude = sensor.read_altitude()
      pressure = sensor.read_pressure()
      sea_level_pressure = sensor.read_sealevel_pressure()
      timestamp = "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())
      bmp180_payload = {'temperature': temperature, 'altitude': altitude, 'pressure': pressure, 'sea_level_pressure': sea_level_pressure, 'timestamp': timestamp}
      requests.post(api_url+'BMP180', bmp180_payload)
      time.sleep(60)
except KeyboardInterrupt:
      print("Ctrl+C pressed... exiting.")
      cleanup()
except requests.exceptions.ConnectionError:
      print("Loopback Connection Error. Please ensure that "+api_url+" is running.")
      cleanup()
except IOError:
      print("IOError. Please check your sensor GPIO configuration.")
      cleanup()
