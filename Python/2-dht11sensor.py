#!/usr/bin/python
'''
 DHT11/DHT22 Sensor
 Requires Adafruit DHT library
    git clone https://github.com/adafruit/Adafruit_Python_DHT
    cd Adafruit_Python_DHT
    sudo python setup.py install
'''
import sys
import Adafruit_DHT

try:
    # Setup sensor type and Pin connection (BCM)
    sensor = Adafruit_DHT.DHT11 
    pin = 4
    
    # Get a sensor reading
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    
    # Try until you get a reading 
    if humidity is not None and temperature is not None:
        print('The temperature is {0:0.1f}*  and relative humidity is {1:0.1f}%.'.format(temperature, humidity))
    else:
        print('Failed to get reading. Please check your connection and try again!')
        sys.exit(1)
except KeyboardInterrupt:
      print("<Ctrl+C> pressed... exiting.")
      sys.exit(0) 
except:
      print("Error: {0} {1}".format(sys.exc_info()[0], sys.exc_info()[1]))
