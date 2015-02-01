#!/usr/bin/python

import time
import json
from pprint import pprint
import urllib2

response = urllib2.urlopen('http://api.no3x.de/app_dev.php/CircleTimer/Settings')

data = json.load(response)   
connections = data['connections']

for key, value in data.iteritems():
	print key
	print value


# Number of segments
SEGMENTS_SIZE = 60
# 3 bytes per pixel
PIXEL_SIZE = 3
# Brightness
BRIGHTNESS_MAX = 2

# Colors
BLACK = bytearray(b'\x00\x00\x00')
BLUE = bytearray(b'\x00\x00\xff')
RED = bytearray(b'\xff\x00\x00')

def write_stream(pixels):
    spidev.write(pixels)
    return

def all_off():
    pixel_output = bytearray(SEGMENTS_SIZE * PIXEL_SIZE + 3)
    print "Turning all LEDs Off"
    for led in range(SEGMENTS_SIZE):
        pixel_output[led * PIXEL_SIZE:] = filter_pixel(BLACK, 1)
    write_stream(pixel_output)
    spidev.flush()

def all_on():
    pixel_output = bytearray(SEGMENTS_SIZE * PIXEL_SIZE + 3)
    print "Turning all LEDs On"
    for led in range(SEGMENTS_SIZE):
        pixel_output[led * PIXEL_SIZE:] = filter_pixel(BLUE, 0.2)
    write_stream(pixel_output)
    spidev.flush()

# Apply Gamma Correction and RGB / GRB reordering
# Optionally perform brightness adjustment
def filter_pixel(input_pixel, brightness):
    if(brightness > BRIGHTNESS_MAX):
        brightness = BRIGHTNESS_MAX
    
    pixel = bytearray(PIXEL_SIZE)
    output_pixel = bytearray(PIXEL_SIZE)

    # also fix colors
    pixel[0] = int(brightness * input_pixel[1])
    pixel[1] = int(brightness * input_pixel[2])
    pixel[2] = int(brightness * input_pixel[0])

    output_pixel[0] = gamma[pixel[0]]
    output_pixel[1] = gamma[pixel[1]]
    output_pixel[2] = gamma[pixel[2]]
    print(output_pixel[2])
    return output_pixel

print "Circle Timer"

spi_dev_name = "/dev/spidev0.0"
spidev = file(spi_dev_name, "wb")

gamma = bytearray(256)
for i in range(256):
    gamma[i] = int(pow(float(i) / 255, 2.5) * (255))

all_on()
time.sleep(2)
all_off()
