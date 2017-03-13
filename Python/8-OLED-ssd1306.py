#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# 128x64 OLED I2C Display for Raspberry Pi
#   - Display system metrics (CPU temp, load, available disk & memory)
#
import os, time
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Interval for display refresh (seconds)
INTERVAL = 10

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware I2C:
#disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
try:
  # 128x64 display with hardware I2C:
  disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

  # Initialize library.
  disp.begin()

  # Clear display.
  disp.clear()
  disp.display()

  # Create blank image for drawing.
  # Make sure to create image with mode '1' for 1-bit color.
  width = disp.width
  height = disp.height
  image = Image.new('1', (width, height))
  bottom = height

  # Get drawing object to draw on image.
  draw = ImageDraw.Draw(image)

  x = 2
  top = 0

  # Load default font.
  # font = ImageFont.load_default()

  # Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
  font = ImageFont.truetype('vcr_osd_mono.ttf', 12)

  while True:
    # Display system metrics
	  cpu_load = os.popen("top -d 0.5 -b -n2 | grep \"Cpu(s)\"|tail -n 1 | awk '{print $2 + $4}'").read().strip('\n')
	  temperature = os.popen("vcgencmd measure_temp").read()[5:-3]
	  mem_free = os.popen("free -h | grep 'Mem:' | awk '{print $4}'").read()
	  disk_free = os.popen("df -h / | tail -1 | awk '{print $4}'").read()

	  # Write 4 lines of text.
	  draw.text((x, top),    'CPU Temp: %s\xB0C' % temperature,  font=font, fill=255)
	  draw.text((x, top+16), 'CPU Load: %s%%' % cpu_load,  font=font, fill=255)
	  draw.text((x, top+32), 'Mem Free: %s' % mem_free,  font=font, fill=255)
	  draw.text((x, top+48), 'DiskFree: %s' % disk_free,  font=font, fill=255)

	  # Display image.
	  disp.image(image)
	  disp.display()
	  time.sleep(INTERVAL)

	  # Clear for next display
	  # Draw a black filled box to clear the image.
	  draw.rectangle((0,0,width,height), outline=0, fill=0)
except IOError:
	print("IOError: Please check your OLED display connection.")
except KeyboardInterrupt:
	disp.clear()
	disp.display()
