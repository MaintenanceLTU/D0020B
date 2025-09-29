'''
    File name: lab_ambient.py
    Author: Johan Odelius
            Luleå University of Technology
    %
'''

import os
from time import sleep
from datetime import datetime
import json
import numpy as np
import matplotlib.pyplot as plt
import ibmiotf.device
#%%
########Input########
interval = 1.0   #Sec


#######Input GPIO pins for MAX31855########
from max31855 import MAX31855, MAX31855Error
cs_pin = 16         #SPI1 CS0
clock_pin = 21      #SPI1 SCLK
data_pin = 19       #SPI1 MISO
units = "c"         #(optional) unit of measurement to return. ("c" (default) | "k" | "f")
properties = {
    'name' : 'Thermocouple',    
    'amplifier_model': 'MAX31855', #'captured_at': '',
    'units': 'c',
    }

MAX31855_TEMPS = MAX31855(cs_pin, clock_pin, data_pin, units)

####### SUBFUNCTIIONS ########
def get_ambient():
    #Varb for class with given GPIO inputs
    return MAX31855_TEMPS.get()        
   
####### MAIN LOOP ########
try:
    while True:
        t = datetime.utcnow()     
        
        # Get ambient
        ambient_temperature = get_ambient()
        
        print(ambient_temperature)
        sleep(interval)
        
except KeyboardInterrupt:
    print("Stop")
    MAX31855_TEMPS.cleanup()
#except:
#    MAX31855_TEMPS.cleanup()
    
