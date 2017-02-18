#!/usr/bin/python
'''
This reads BMP180/BMP085 sensor data and sends it to Initial State 
(https://app.initialstate.com/)
for data analysis and visualization. Requires a valid account.
'''
import signal, time
import sys
import Adafruit_BMP.BMP085 as BMP085
from ISStreamer.Streamer import Streamer

streamer = Streamer(bucket_name="BMP 180 Sensor", bucket_key="bmp_180", access_key="<Insert your Access Key Here>")

def signal_handler(signal, frame):
   streamer.log("Status", "offline")
   print("You exited")
   sys.exit(0)

try:
   sensor = BMP085.BMP085()
   streamer.log("Status", "online")
   signal.signal(signal.SIGINT, signal_handler)

   while True:
      streamer.log("Temperature", sensor.read_temperature())
      streamer.log("Pressure", sensor.read_pressure())
      streamer.log("Altitude", sensor.read_altitude())
      streamer.log("Sealevel Pressure", sensor.read_sealevel_pressure())
      time.sleep(60)

   signal.pause()

except KeyboardInterrupt:
      streamer.close()
except IOError:
      streamer.log("Status", "offline")
      sys.exit(1)

