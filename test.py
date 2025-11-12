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

    logging.info("showing GIFs in rotation")
    
    # List of GIF files to rotate through
    gif_files = ["1.gif", "2.gif", "3.gif", "4.gif"]
    
    # Duration to show each GIF (in seconds)
    gif_duration = 3
    
    # Loop through GIFs continuously
    try:
        while True:
            for gif_file in gif_files:
                logging.info(f"Loading {gif_file}")
                gif_image = Image.open(gif_file)
                
                # Get the number of frames in the GIF
                try:
                    frame_count = gif_image.n_frames
                except AttributeError:
                    frame_count = 1
                
                # Record start time for this GIF
                start_time = time.time()
                frame_num = 0
                
                # Display frames for the specified duration
                while time.time() - start_time < gif_duration:
                    gif_image.seek(frame_num % frame_count)
                    
                    # Copy the current frame
                    current_frame = gif_image.copy()
                    
                    # Fit to display without scaling up
                    img_width, img_height = current_frame.size
                    display_width, display_height = disp.width, disp.height
                    
                    # Only scale down if image is larger than display
                    if img_width > display_width or img_height > display_height:
                        # Calculate scale factor to fit within display
                        scale = min(display_width / img_width, display_height / img_height)
                        new_width = int(img_width * scale)
                        new_height = int(img_height * scale)
                        current_frame = current_frame.resize((new_width, new_height), Image.LANCZOS)
                    
                    # Create a blank image with display size
                    display_image = Image.new('RGB', (display_width, display_height), 'BLACK')
                    
                    # Center the image on the display
                    paste_x = (display_width - current_frame.width) // 2
                    paste_y = (display_height - current_frame.height) // 2
                    
                    # Convert to RGB if needed before pasting
                    if current_frame.mode != 'RGB':
                        current_frame = current_frame.convert('RGB')
                    
                    display_image.paste(current_frame, (paste_x, paste_y))
                    
                    # Display the frame
                    disp.ShowImage(display_image)
                    time.sleep(0.05)  # Delay between frames
                    
                    frame_num += 1
                
                gif_image.close()
                logging.info(f"Finished {gif_file}, moving to next")
                
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