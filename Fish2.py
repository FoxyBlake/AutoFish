from PIL import ImageGrab
import numpy as np
from pyautogui import *
import pyautogui
import time
import keyboard
import random
import cv2
import win32api, win32con
import time

#bar Pos 1 X:   930     Y: 1100
#bar Pos 2 X:   1630     Y: 1100
#Fishing Icon X: 1307 Y: 1268 RGB: (147, 111,  74)

#Functions

#Click Function, Argument of x and y position to click
def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

#Detect grey pixel in range of width argument starting at the start x argument and the
#y argument
def isGreyPixelPresent(region_start_x, y, width):
    img = ImageGrab.grab(bbox=(region_start_x, y, region_start_x + width, y + 1))
    img_np = np.array(img)  # shape: (1, width, 3)
    
    # Convert RGB to BGR for OpenCV
    img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    
    # Extract blue channel
    blueChannel = img_cv[0, ::3, 0]  # OpenCV uses BGR order
    
       # Boolean mask: green values in desired range
    blueMatch = (blueChannel < 160)
    
    return np.any(blueMatch)

def whereGreenPixelPresent(region_start_x, y, width):
    img = ImageGrab.grab(bbox=(region_start_x, y, region_start_x + width, y + 1))
    img_np = np.array(img)  # shape: (1, width, 3)

    # Extract green channel only
    green_channel = img_np[0, :, 1]  # all x values at y = 0

    # Boolean mask: green values in desired range
    green_match = (green_channel > 160)

    # Get indices where green is in range
    green_indices = np.where(green_match)[0]

    if green_indices.size == 0:
        return None, None  # No green pixel found

    first_x = region_start_x + green_indices[0]
    last_x = region_start_x + green_indices[-1]

    return first_x, last_x #return the coordinates of the first and last green pixel detected

#variables
random_integer = random.randint(1, 10)
found = False

#Run Loop, Press Q to end
while keyboard.is_pressed('q') == False:
    
    r, g, b = pyautogui.pixel(1307, 1268)

    if r == 147: #If fish button is there click it
        click(1277 + random_integer, 1288 + random_integer)
        random_integer = random.randint(1, 10)
        found = False
        time.sleep(0.3)
    elif r != 242: #If the cancel button is not there then it is actively fishing so continue
        
        if not found: #If greenbar hasnt been found yet then find it
            greenStart, greenEnd = whereGreenPixelPresent(933, 1100, 694) #detect where the green bar is
            if greenStart is not None:
                found = True #change found to true if green bar is found
        elif isGreyPixelPresent(greenStart+8, 1080, greenEnd - greenStart-8):#detect if the grey pixel is in the range of where the green bar is
            for i in range(8): #Raise or lowerer depending on how rare of a fish you are going for(Lower for rarer fish)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                time.sleep(0.001)  # 1 ms (optional)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    else:
        time.sleep(0.2)
    time.sleep(0.002)
