#!/usr/bin/python
'''
This reads DHT11 sensor data and sends it to Adafruit.io (https://adafruit.io/)
for data analysis and visualization. Requires a valid account.
'''
import sys, time
import Adafruit_DHT
from Adafruit_IO import Client
aio = Client('<Insert Adafruit AIO key here>')

# Setup sensor type and Pin connection (BCM)
sensor = Adafruit_DHT.DHT11 
pin = 26 
INTERVAL = 30

try:
   # Try until you get a reading 
   while True:
      humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
      if humidity is not None and temperature is not None:
         aio.send('dht11-temp', temperature)
	 aio.send('dht11-humidity', humidity)
         time.sleep(INTERVAL)
      else:
         print('Failed to get reading. Please check your connection and try again!')
         sys.exit(1)
except KeyboardInterrupt:
      print("Ctrl+C pressed... exiting.")
      sys.exit(0)
except:
      print("Error: {0} {1}".format(sys.exc_info()[0], sys.exc_info()[1]))   
