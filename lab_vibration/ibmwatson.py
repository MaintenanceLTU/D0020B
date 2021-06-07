 # import json an mqtt
import json
import ibmiotf.device

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
    