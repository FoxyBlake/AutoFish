from PIL import ImageGrab
import numpy as np
from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con
import time
import ctypes

#bar Pos 1 X:   930     Y: 1100
#bar Pos 2 X:   1630     Y: 1100
#Fishing Icon X: 1307 Y: 1268 RGB: (147, 111,  74)

SendInput = ctypes.windll.user32.SendInput

# Constants
MOUSE_LEFTDOWN = 0x0002
MOUSE_LEFTUP = 0x0004

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("mi", MOUSEINPUT)]


def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def is_grey_pixel_present(region_start_x, y, width):
    img = ImageGrab.grab(bbox=(region_start_x, y, region_start_x + width, y + 1))
    img_np = np.array(img)  # shape: (1, width, 3)
    
    # Extract green channel only
    green_channel = img_np[0, ::3, 1]  # check every 2nd pixel's green
    
    # Boolean mask: green values in desired range
    green_match = (green_channel > 60) & (green_channel < 170)
    
    return np.any(green_match)

def send_fast_click():
    extra = ctypes.c_ulong(0)
    ii_ = INPUT(type=0, mi=MOUSEINPUT(0, 0, 0, MOUSE_LEFTDOWN, 0, ctypes.pointer(extra)))
    SendInput(1, ctypes.pointer(ii_), ctypes.sizeof(ii_))
    ii_.mi.dwFlags = MOUSE_LEFTUP
    SendInput(1, ctypes.pointer(ii_), ctypes.sizeof(ii_))

random_integer = random.randint(1, 10)

while keyboard.is_pressed('q') == False:
    
    r, g, b = pyautogui.pixel(1307, 1268)

    if r == 147:
        click(1277 + random_integer, 1288 + random_integer)
        random_integer = random.randint(1, 10)
        time.sleep(0.3)
    elif r != 242:
        if not is_grey_pixel_present(933, 1100, 694):
            for i in range(12):
                send_fast_click()
                #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                #time.sleep(0.001)  # 1 ms (optional)
                #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(0.002)
