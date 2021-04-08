#!/usr/bin/env python3

import time
from rpi_ws281x import *
import argparse
from math import floor, ceil





class LEDStrip():

    def __init__(self):
        # LED strip configuration:
        self.LED_COUNT      = 42      # Number of LED pixels.
        self.LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
        
        #LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
        self.LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
        self.LED_BRIGHTNESS = 5     # Set to 0 for darkest and 255 for brightest
        self.LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        self.LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

        # LED module parameters:
        self.NUM_PIXEL_ON = 14							# Number of pixels to light up at one time:
        self.MAX_PIXEL_NUM = self.LED_COUNT - self.NUM_PIXEL_ON	# Max pixel number that will be controlled
        self.center_PIXEL = floor(self.LED_COUNT/3)

        # initialise and start strip
        self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
        self.strip.begin()

    def change_brightness(self, brightness):
        
        #sanity check
        if (brightness > 255):
            brightness = 255
        elif (brightness < 0):
            brightness = 0

        print("setting brightness to {}".format(brightness))

        self.strip.setBrightness(brightness)
        self.strip.show()

    def colour_wipe(self, colour):
        '''
        Wipe the LED strip
        Parameters: 
            strip: NeoPixel Object
            colour: LED colour
        '''
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, colour)
        
        self.strip.show()


    def boundary_control(self, pixel):
        '''
        This function checks if the pixel number has gone outside of the boundaries,
        and will keep it at the boundary.
        Parameters:
            pixel: pixel number on LED strip
        Return Value:
            pixel: return pixel number
        '''
        if (pixel > self.MAX_PIXEL_NUM):
            pixel = self.MAX_PIXEL_NUM
        elif (pixel < 0):
            pixel = 0
        return pixel
        
        
    def colour_warning(self, pos, colour, laneWidth):
        '''	
        This function changes LED colour to yellow if vehicle starts to veer,
        and to red if vehicle is close to the edge.  If the vehicle is in the center
        it keeps the colour as the default green.
        Parameters:
            pos: vehicle position relative to center (left is negative, center is 0, right is positive)
            colour: LED colour
        Return Value:
            colour: LED colour
        '''
        center = laneWidth/2.0
        if (abs(pos) > (center*0.5)):
            if (abs(pos) > (center*0.8)):
                # red warning if vehicle has veered 80% from center
                colour = Color(255, 10, 14)
            else:
                # yellow warning if vehicle has veered 50% from center
                colour = Color(255, 255, 0)
        return colour
            
            
                    
    def set_pixel_colour(self, pixel, colour):
        '''
        This function sets the pixel colour on the LED.
        Parameters:
            strip: NeoPixel Object
            pixel: pixel number on LED strip
            colour: LED colour
        '''
        # set pixel
        print("setting pixel {}".format(int(pixel)))
        for offset in range(self.NUM_PIXEL_ON):
            self.strip.setPixelColor(int(pixel + offset), colour)
        self.strip.show()
        

    def goal_posts(self, laneWidth):
        self.strip.setPixelColor(0, Color(0,0,200))
        self.strip.setPixelColor(self.LED_COUNT-1, Color(0,0,200))

            
    def vehicle_position(self, pos, laneWidth, goalPost = True, colour=Color(18, 255, 30)):
        '''
        This function lights up 10 LEDs in the LED array.
        The LEDs depict the vehicle position in the lane, relative to the center.
        Parameters:
            strip: NeoPixel Object
            pos: vehicle position relative to center (left is negative, center is 0, right is positive)
            colour: LED colour
        '''
        self.colour_wipe(Color(0,0,0))
        
        # map pos to pixel number	
        if (pos > 0):
            pixel = self.center_PIXEL - abs(pos*10)
        elif (pos < 0):
            pixel = self.center_PIXEL + abs(pos*10)
        else:
            pixel = self.center_PIXEL
            
        pixel = self.boundary_control(pixel)
        colour = self.colour_warning(pos, colour, laneWidth)
        
        #light up lanes if we want to show them
        if (goalPost):
            self.goal_posts(laneWidth)
            
        self.set_pixel_colour(pixel, colour)
        
        

    def direction_to_travel(self, pos, laneWidth, goalPost = True, colour=Color(18, 255, 30)):
        '''
        This function lights up 10 LEDs in the LED array.
        The LEDs depict the direction that the user must travel in, to make it back to the center.
        Parameters:
            strip: NeoPixel Object
            pos: vehicle position relative to center (left is negative, center is 0, right is positive)
            colour: LED colour
        '''
        self.colour_wipe(Color(0,0,0))
        
        # map pos to pixel number	
        if (pos > 0):
            pixel = self.center_PIXEL + abs(pos*10)
        elif (pos < 0):
            pixel = self.center_PIXEL - abs(pos*10)
        else:
            pixel = self.center_PIXEL
            
            
        pixel = self.boundary_control(pixel)	 
        colour = self.colour_warning(pos, colour, laneWidth)
        
        #light up lanes if we want to show them
        if (goalPost):
            self.goal_posts(laneWidth)
            
        self.set_pixel_colour(pixel, colour)

    def vehicle_position_conversion(self, distFromLeft, distFromRight):
        '''
        This function takes the vehicle's distance from the left and right lane and converts that
        to a vehicle position relative to the center of the lane.  This is to be passed to the
        module that controls the LED array.
        Parameters:
            distFromLeft: vehicle distance (metres) from left lane
            distFromRight: vehicle distance (metres) from right lane
        Return Value:
            pos: vehicle position (metres) relative to center of lane
            laneWidth: width of the lane (metres)
        '''
        print("distFromLeft = {}, distFromRight = {}".format(distFromLeft, distFromRight))
        laneWidth = distFromLeft + distFromRight
        center = laneWidth / 2.0
        pos = distFromLeft - center  #position relative to center. left of center is negative, center is 0, right is positive.
        return (pos, laneWidth)

	


