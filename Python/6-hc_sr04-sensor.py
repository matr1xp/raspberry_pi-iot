#!/usr/bin/python
#
# HC-SR04 Ultrasonic ranging sensor
#
import RPi.GPIO as GPIO
import sys, time

try:
    GPIO.setmode(GPIO.BCM)
    
    TRIG = 23
    ECHO = 24
    
    print "Distance measurement in progress..."
    
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)
    while True:
        print "Waiting for sensor to settle"
        
        time.sleep(2)
        
        GPIO.output(TRIG, True)
        
        time.sleep(0.00001)
        
        GPIO.output(TRIG, False)
        
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()
            
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()
                
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        
        print "Distance: ", distance, "cm"
except KeyboardInterrupt:
      GPIO.cleanup()
      print("<Ctrl+C> pressed... exiting.")  
except:
      GPIO.cleanup()
      print("Error: {0} {1}".format(sys.exc_info()[0], sys.exc_info()[1]))
   
