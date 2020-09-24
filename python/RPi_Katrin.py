# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 14:32:03 2020

@author: KB
"""

# import packages
import ntplib
import ibmiotf.device
from datetime import datetime
import numpy as np

# setup MQTT for IBM IOT Platform
options = {
    "org": "bd0yob",
    "type": "RPi",
    "id": "8",
    "auth-method": "token",
    "auth-token": "Y2kBVWh)Pmb4)?)Az)",
    "port": 8883,
    "keepAlive": 60
    }
client = ibmiotf.device.Client(options)

#######Input GPIO pins for MAX31855########
import sys
sys.path.append('/home/pi/Documents/D0020B/lab_temperature/')
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

# connect to client
client.connect()

# conncet to ntp client
ntpclient = ntplib.NTPClient()

# Define timestamp function
def timestamp(ntp=True): #timespec='milliseconds'
    if ntp:
        response = ntpclient.request('europe.pool.ntp.org', version=3)
        t = datetime.utcfromtimestamp(response.tx_time)
    else:
        t = datetime.utcnow()
    return t.isoformat() #timespec=timespec

ambient_temperature = get_ambient()

#timestamped  datapackage
pkg = {
    "ts": timestamp(),
    "d": {
        "ambient_temperature": {
            'value': ambient_temperature
            }
            }
    }


# publish
client.publishEvent('data', 'json', pkg)

#disconnect to client
client.disconnect()