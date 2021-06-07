import json
import ibmiotf.device
from datetime import datetime
import ntplib
import numpy as np


import sys
sys.path.append('/home/pi/Documents/D0020B/lab_vibration')

import LIS33HH

LIS33HH.power("normal")
LIS33HH.rang("12g")
LIS33HH.BDU("block")

#Setup MQZZ for IBM IOT platform
options = {
    "org": "bd0yob",
    'type': 'RPi',
    'id': '9',
    'auth-method': 'token',
    'auth-token': 'KaDeMaTa4',
    'port': 8883,
    'keepAlive': 60
    }
client = ibmiotf.device.Client(options)

#connect to client
client.connect()

#creating timestamps

#
from datetime import datetime
from time import sleep
#t = datetime.utcnow()

#Return POSIX timestamp from datetime object
#see https://en.wikipedia.org/wiki/Unix_time
#tts = t.timestamp()

#create a timestamp in string in format '2019-11-15T16:23:43.359171'
#tstring = t.isoformat()

#Resolution can be changed specifying timespec
#tstring = t.isoformat(timespec = 'milliseconds') #'2019-11-15T16:23:43.359'


# Use ntp to get accurate network time
import ntplib
ntpclient = ntplib.NTPClient()
#response = c.request('europe.pool.ntp.org', version = 3)
# Create datetime object from ntp network time
#t = datetime.utcfromtimestamp(response.tx_time)
#tstring = t.isoformat(timespec = 'milliseconds')



#Publishing data package
#
#
import ibmiotf.device
#from datetime import datetime
import ntplib
#import numpy as np

#Setup MQTT for IBM IOT platform
#options = {
    #"org": "bd0yob",
    #'type': 'RPi',
    #'id': '9',
    #'auth-method': 'token',
    #'auth-token': 'KaDeMaTa4',
    #'port': 8883,
    #'keepAlive': 60
    #}
#client = ibmiotf.device.Client(options)

#connect to client
#client.connect()


#Define Timestamp function
def timestamp(timespec = 'milliseconds', ntp=True):
    if ntp:
        response = ntpclient.request('europe.pool.ntp.org', version = 3)
        t = datetime.utcfromtimestamp(response.tx_time)
    else:
        t = datetime.utcnow()
    return t.isoformat(timespec=timespec)

# Data acqustion

# Example pkg (to be replaced with your code)

try: 
    while True:
        pkg = {
            'ts' : timestamp() ,
            'accelero' : LIS33HH.get_res("all")
    }

    
# publish data
        client.publishEvent('data', 'json', pkg)
        sleep(1)
    
except KeyboardInterrupt:     
# disconnect to client
    client.disconnect()
    