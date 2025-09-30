#!/usr/bin/env python3
# mqtt_pub_hivemq.py
import json, time, random, sys
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

HOST  = "YOUR_BROKER_ADDRESS"          # e.g. xxxxxx.s1.eu.hivemq.cloud
PORT  = 8883
USER  = "YOUR_USERNAME"
PASS  = "YOUR_PASS"
TOPIC = "YOUR_APP/telemetry"           # e.g. ltu11/telemetry

NUMBER_OF_MESSAGES = 10                # set to None for infinite
DELAY_S = 1.0
QOS = 1

client = mqtt.Client(protocol=mqtt.MQTTv311)
client.username_pw_set(USER, PASS)
client.tls_set()                       # use system CAs (recommended for HiveMQ Cloud)


client.connect(HOST, PORT, keepalive=30)
client.loop_start()

try:
    count = 0
    while NUMBER_OF_MESSAGES is None or count < NUMBER_OF_MESSAGES:
        value = random.uniform(10.0, 20.0)
        payload = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "d": {"distance": {"v": value}}
        }
        info = client.publish(TOPIC, json.dumps(payload), qos=QOS)
        info.wait_for_publish(timeout=5)
        time.sleep(DELAY_S)
        count += 1
except KeyboardInterrupt:
    pass
finally:
    client.loop_stop()
    client.disconnect()
    print("Stopped and disconnected")
