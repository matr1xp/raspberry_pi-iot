#!/usr/bin/python
#
# 128x64 OLED I2C Display for Raspberry Pi
#   - 1-bit Images Slideshow
#
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from os import listdir
from os.path import isfile, join

# Raspberry Pi pin configuration:
RST = 24

try:
  # 128x64 display with hardware I2C:
  disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

  # Initialize library.
  disp.begin()

  # Clear display.
  disp.clear()
  disp.display()

  # Look for `images` folder 
  img_path = 'images'
  imgfiles = [f for f in listdir(img_path) if isfile(join(img_path, f))]
  while True:
  	# Display slideshow
  	for f in imgfiles:
  		# Convert image to 1 bit color
	  	image = Image.open(img_path+'/'+f).resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
		# Display image.
		disp.image(image)
		disp.display()
		time.sleep(1)
except IOError:
	print("IOError: Please check your OLED display connection.")
except KeyboardInterrupt:
	disp.clear()
	disp.display()
