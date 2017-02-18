#!/usr/bin/python
#
# 3 LED random blinker
#
import RPi.GPIO as GPIO
import sys, time
from random import randint

# Set pin numbers
button = 5
red = 20
green = 18
yellow = 16
LEDS = {red:'red', yellow:'yellow', green:'green'}

# Randomize function
def random(x):
    return {
        1: red,
        2: green,
        3: yellow
    }[x]

# Turn OFF LEDs
def turn_off(n=0):
    if n == 0:
       for led in LEDS:
         GPIO.output(led, GPIO.LOW)
    else:
       GPIO.output(n, GPIO.LOW)

# Use Broadcom SOC channel pins
GPIO.setmode(GPIO.BCM)

# Setup GPIO Pins
GPIO.setup(button, GPIO.IN)
for led in LEDS:
   GPIO.setup(led, GPIO.OUT)

i = 0
try:
  while True:
    input_state = GPIO.input(button)
    if input_state == False:
       # turn OFF all LEDs first
       turn_off()
       on = random(randint(1,3))
       GPIO.output(on, GPIO.HIGH)
       print('(%s) Button pressed: %s' % (str(i), LEDS[on]))
       time.sleep(0.5)
       i += 1
except KeyboardInterrupt:
      turn_off()
      GPIO.cleanup()
      print("<Ctrl+C> pressed... exiting.")
      sys.exit(0) 
except:
      GPIO.cleanup()
      print("Error: {0} {1}".format(sys.exc_info()[0], sys.exc_info()[1]))

