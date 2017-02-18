#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
  BMP180/BMP085 Barometric sensor
  Requires Adafruit BMP library
    git clone https://github.com/adafruit/Adafruit_Python_BMP.git
    cd Adafruit_Python_BMP
    sudo python setup.py install
'''
import sys, time
import Adafruit_BMP.BMP085 as BMP085

try:
    sensor = BMP085.BMP085()
    #sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)
    
    print('Temp = {0:0.2f}°C'.format(sensor.read_temperature()))
    print('Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()))
    print('Altitude = {0:0.2f} m'.format(sensor.read_altitude()))
    print('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()))
except:
    print("Error: {0} {1}".format(sys.exc_info()[0], sys.exc_info()[1]))
   
