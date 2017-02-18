#!/usr/bin/python
#
# HC-SR501 PIR Motion sensor
#
import RPi.GPIO as GPIO
import sys, time

GPIO.setmode(GPIO.BCM)
DATA_PIN = 4 

GPIO.setup(DATA_PIN, GPIO.IN)

def motion_detect(DATA_PIN):
   print "Motion detected!"

try:
   GPIO.add_event_detect(DATA_PIN, GPIO.RISING, callback=motion_detect)
   while 1:
      time.sleep(60)
except KeyboardInterrupt:
      GPIO.cleanup()
      print("<Ctrl+C> pressed... exiting.")
      sys.exit(0) 
except:
      GPIO.cleanup()
      print("Error: {0} {1}".format(sys.exc_info()[0], sys.exc_info()[1]))
   
