# This file may define an action that is executed every interval time in the analog loop
# The action must be defined in the addon() function.
# This could be for example switching a relais on or off at a given voltage level
# If this file does not exist: no problem as there is a try / except to check

# addon.py must contain a function addon(voltages)
# voltages is the array of 4 voltages 0...3V read at the analog inputs

# Digital pins for output:
from machine import Pin, I2C, UART
d18 = Pin(18, Pin.OUT)
d19 = Pin(19, Pin.OUT)
d20 = Pin(20, Pin.OUT)
d21 = Pin(21, Pin.OUT)

# User defined threshold:
threshold = 2.0


def addon(voltages):
    
    # Examples:
    # print('*')
    # d21.toggle()
    # print('*', voltages[0], '*')
    
    # threshold switching:
    if voltages[0] > threshold:
        d21.value(1)
    else:
        d21.value(0)
        
    
    