#!/usr/bin/python
#
# SG90 Servo motor control
#  
import time
import wiringpi

# use 'GPIO naming'
wiringpi.wiringPiSetupGpio()

# set #18 to be a PWM output
wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)

# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)
delay_period = 0.01

while True:
   for pulse in range(48, 210, 1):
	wiringpi.pwmWrite(18, pulse)
   	time.sleep(delay_period)
   for pulse in range(210, 48 -1):
	wiringpi.pwmWrite(18, pulse)
	time.sleep(delay_period)


