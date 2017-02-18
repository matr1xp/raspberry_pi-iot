#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, time, datetime, glob
import sys 
import requests
import Adafruit_DHT as DHT

dht_sensor = DHT.DHT11
dht_pin = 26

api_url = 'http://0.0.0.0:3000/api/'

def read_dht():
    humidity, temperature = DHT.read_retry(dht_sensor, dht_pin)
    return temperature, humidity

def cleanup():
   sys.exit(0)

try:
   while True:
      temperature, humidity = read_dht()
      timestamp = "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())
      dht11_payload = {'temperature': temperature, 'humidity': humidity, 'timestamp': timestamp}
      requests.post(api_url+'DHT11', dht11_payload)
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
