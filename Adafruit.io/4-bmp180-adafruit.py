#!/usr/bin/python
'''
This reads BMP180 sensor data and sends it to Adafruit.io (https://adafruit.io/)
for data analysis and visualization. Requires a valid account.
'''
import sys, time
import Adafruit_BMP.BMP085 as BMP085
from Adafruit_IO import Client

aio = Client('dec373cb22994ee094a33f22f3f7a0e2')
INTERVAL = 30

try:
   sensor = BMP085.BMP085()
   
   while True:
      aio.send('bmp180-temp', sensor.read_temperature())
      aio.send('bmp180-pressure', sensor.read_pressure())
      aio.send('bmp-alt', "{0:.2f}".format(float(sensor.read_altitude())))      
      aio.send('bmp-seapress', sensor.read_sealevel_pressure())      
      time.sleep(INTERVAL)
except KeyboardInterrupt:
      print("Ctrl+C pressed... exiting.")
      sys.exit(0)
except:
      print("Error: {0} {1}".format(sys.exc_info()[0], sys.exc_info()[1]))
