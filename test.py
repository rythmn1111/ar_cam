#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch83
from PIL import Image

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level = logging.DEBUG)

try:
    # display with hardware SPI:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    #disp = LCD_1inch83.LCD_1inch83(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_1inch83.LCD_1inch83()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    #Set the backlight to 50
    disp.bl_DutyCycle(50)

    logging.info("showing sad.gif")
    
    # Open and display the sad.gif
    gif_image = Image.open("sad.gif")
    
    # If it's an animated GIF, loop through frames
    try:
        frame_count = 0
        while True:
            # Resize to fit display if needed
            resized_image = gif_image.copy()
            if resized_image.size != (disp.width, disp.height):
                resized_image = resized_image.resize((disp.width, disp.height), Image.LANCZOS)
            
            # Convert to RGB mode if needed (GIFs might be in palette mode)
            if resized_image.mode != 'RGB':
                resized_image = resized_image.convert('RGB')
            
            # Display the frame
            disp.ShowImage(resized_image)
            
            frame_count += 1
            
            # Try to move to next frame
            try:
                gif_image.seek(gif_image.tell() + 1)
                time.sleep(0.1)  # Delay between frames
            except EOFError:
                # End of frames, loop back to start
                gif_image.seek(0)
                time.sleep(0.1)
                
    except KeyboardInterrupt:
        pass
    
    disp.module_exit()
    logging.info("quit:")
    
except IOError as e:
    logging.info(e)    
    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()