 # import json an mqtt
import json
import ibmiotf.device

# accelerometer data
import sys
sys.path.append('/home/pi/Documents/D0020B/lab_vibration')
import LIS33HH

# datetime import
from datetime import datetime
import ntplib
from time import sleep

# SETUP parameters for accelero
LIS33HH.power("normal")
LIS33HH.rang("12g")
LIS33HH.BDU("block")

# Setup MQTT for IBM IOT platform
options = {
    "org": "bd0yob",
    "type": "RPi",
    "id": "7",
    "auth-method": "token",
    "auth-token": "LOXv)aw8bQQ)92?1UC",
    "port":8883,
    "keepAlive": 60
    }
client = ibmiotf.device.Client(options)

# connect to client
client.connect()


# connect to NTP client
ntpclient = ntplib.NTPClient()

# define timestamp function

def timestamp(timespec= 'milliseconds', ntp=True) :
    if ntp:
        response = ntpclient.request('europe.pool.ntp.org', version=3)
        t = datetime.utcfromtimestamp(response.tx_time)
    else:
        t = datetime.utcnow()
    return  t.isoformat(timespec=timespec)

# gets le data
try:
    while True:
        package = {
            'ts' : timestamp() ,
            'accelero' : LIS33HH.get_res("all")
        }

        #publish data
        client.publishEvent('data', 'json', package)
        
        sleep(1)
except KeyboardInterrupt: 
    #disconnect
    client.disconnect()
