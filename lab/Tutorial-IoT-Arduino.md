# IoT Lab - Tutorial Arduino + HiveMQ Cloud + Node-RED
*Johan Odelius, Operation and Maintenance, Luleå University of Technology, Sweden*  

## Hardware and Software Setup
- Connect your Arduino/ESP board. One of: MKR WiFi 1010, UNO WiFi Rev2, or ESP32.
- In Arduino IDE:  
  - Install the correct board package (e.g., *Arduino SAMD Boards* for MKR WiFi 1010, or *ESP32 boards* for ESP32).  
  - Select the correct serial port under **Tools → Port**.

### Required Libraries
Install these libraries from the Arduino IDE Library Manager:
- **WiFiNINA** (MKR/UNO) or **WiFi** (ESP32).
- **ArduinoMqttClient** (or PubSubClient).
- **ArduinoJson**.
- (optional) **NTPClient** for timestamps.

---
## Broker info (provided in class / Canvas)
   - **Application name** 
   - **IBM cloud subdomain**
   - **Cluster hostname** (e.g. `xxxxxx.s1.eu.hivemq.cloud`)  
   - **Port**: 8883 (TLS)  
   - **Username and password**
---

## 3. Arduino Code
### Example sketch Arduino MKR WiFi 1010 (WiFiNINA)
```cpp
#include <WiFiNINA.h>
#include <WiFiSSLClient.h>
#include <ArduinoMqttClient.h>
#include <ArduinoJson.h>

// ---- EDIT ----
const char* WIFI_SSID = "YOUR_WIFI";
const char* WIFI_PASS = "YOUR_PASS";

const char* MQTT_HOST = "YOUR_CLUSTER.s1.<region>.hivemq.cloud";
const int   MQTT_PORT = 8883;
const char* MQTT_USER = "YOUR_USER";
const char* MQTT_PASS = "YOUR_PASS";

const char* USERID    = "YOUR_APPID";  // e.g. ltu11
// -------------


// TLS socket + MQTT client
WiFiSSLClient  net;
MqttClient     mqtt(net);

// Topics
String baseTopic  = String(USERID) + "/";
String tTelemetry = baseTopic + "telemetry";   // USERID/telemetry
String tStatus    = baseTopic + "status";      // optional
String tMeta      = baseTopic + "meta";        // optional

void connectWifi() {
  if (WiFi.status() == WL_CONNECTED) return;
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) delay(300);
  net.setInsecure(); // classroom shortcut (no CA file)
}

void connectMqtt() {
  if (mqtt.connected()) return;

  mqtt.setId("mkr1010-" + String(millis()));
  mqtt.setUsernamePassword(MQTT_USER, MQTT_PASS);

  // Connect (blocking retry loop kept simple for class)
  while (!mqtt.connect(MQTT_HOST, MQTT_PORT)) { delay(1000); }

  // Optional meta/status
  mqtt.beginMessage(tMeta);
  mqtt.print("{\"device\":\"mkr1010\"}");
  mqtt.endMessage();

  mqtt.beginMessage(tStatus);
  mqtt.print("{\"online\":true}");
  mqtt.endMessage();
}

void setup() {
  connectWifi();
  connectMqtt();
}

void loop() {
  connectWifi();
  connectMqtt();

  // ---- Build your JSON payload ----
  DynamicJsonDocument doc(128);
  doc["ts"] = millis();                 // or a formatted string if you use NTP
  doc["d"]["distance"]["v"] = 123.4;    // <--- replace with your real value

  // Publish (stream JSON directly; no buffers needed)
  mqtt.beginMessage(tTelemetry);
  serializeJson(doc, mqtt);
  mqtt.endMessage();

  delay(2000);
}
```
### Notes for ESP32 / UNO WiFi Rev2
 - ESP32: use `#include <WiFi.h>` and `WiFiClientSecure net;` instead of WiFiNINA/WiFiSSLClient. Keep `ArduinoMqttClient` the same. Use `net.setInsecure();` the same way.
 - UNO WiFi Rev2: RAM is tighter. Keep `DynamicJsonDocument doc(128);` and payload small.

# Node-RED
## Open the editor
Open your Node-RED editor, e.g. `https://<your-nodered-app>.<your-ibmcloud-subdomain>.eu-de.codeengine.appdomain.cloud/red/`.

## Add the MQTT broker (HiveMQ Cloud)
1. Drag an mqtt in node onto the canvas and double-click it.
2. Next to Server, click the pencil to add a new broker.
3. In the Connection tab:
    - **Server**: YOUR_CLUSTER.s1.<region>.hivemq.cloud (your cluster host)
    - **Port**: 8883    
    - **Enable secure (TLS)**: ON
    - **Client ID**: (leave empty)
    - **Username / Password**: (your recieved credentials)
4. TLS configuration (drop-down → Add new tls-config → pencil):
    - **Server name (SNI)**: YOUR_CLUSTER.s1.<region>.hivemq.cloud
    - Leave **CA certificate / Client cert / Key** empty
    - Keep Verify server certificate enabled
    - Click **Add** (to save the TLS config)
5. Back in the broker dialog, ensure your TLS config is selected → **Add** (or **Update**).

## Subscribe & view messages
  - Set the **Topic** in the **mqtt in** node to YOUR_STUDENT_APPID/# (e.g. ltu11/#)    
  - Wire the **mqtt in** node to a **debug** node.
  - Click **Deploy**. When devices publish, you’ll see messages in the right-side **Debug** panel.

## Build a tiny dashboard (gauge only)

1. Drag a **function** node onto the workspace and double-click it.
   - (Optional) Set the name.
   - Paste this code:
     ```js
     return { payload: msg.payload.d.distance.v };
     ```
   - Click **Done**

2. Add a **ui_gauge** (Dashboard → Gauge).
   - Setup a dashboard tab and group
   - Give the gauge a label (e.g. *Distance (cm)*)   
   - Click **Done**

3. Wire it together ([mqtt in] → [function] → [gauge]) and **Deploy**

4. Open the dashboard:
- Top-right menu → **Dashboard**
- At the top-right, click the **link-out icon (↗️)**
- A new browser tab opens and you’ll see the gauge update when data arrives.


# Connecting a sensor
## Hardware Setup
### Components

- HC-SR04 ultrasonic sensor  
- Breadboard + jumper wires  

## Wiring (HC-SR04 → Arduino)
 - See previous lab or the Documents tab in https://www.sparkfun.com/products/13959
---

## Arduino Code
1. Add your HC-SR04 distance code: 
  - Pin definitions. Example:
    ```cpp
    // HC-SR04 pins for MKR WiFi 1010
    const int TRIG_PIN = 5; 
    const int ECHO_PIN = 6;   
    ```
  - In `setup()` set the pin modes, example:
    ```cpp
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    digitalWrite(TRIG_PIN, LOW);
    ```
  - Add a function `readDistance` to measure distance. Copy in your code from the SparkFun example or your earlier lab:
    ```cpp
    long readDistance() {
        
        // --- Your HC-SR04 code here ---

        return distance; 
    }
    ```

3. In your MQTT publishing loop, replace the simulated value with the real sensor value:
    ```cpp
    long distance = readDistance(); 
    doc["d"]["distance"]["v"] = distance;
    ```

4. (Optional) Add an accurate timestamp to your MQTT payload:     
   - Use [`NTPClient`](https://github.com/arduino-libraries/NTPClient) to sync with an NTP server.  
   - On **ESP32**, you can use the built-in `configTime()` instead of an extra library.  
   - With extra hardware, you can use a Real-Time Clock (RTC) module (e.g. DS3231).  


## Node-RED
### (Optional) Add dashboard chart
1. Drag a new **function** node onto the workspace and double-click it.
   - (Optional) Set the name.
   - Paste this code:
     ```js
     return { payload: { ts: msg.payload.ts, value: msg.payload.d.distance.v } };
     ```
   - Click **Done**

2. Add a **ui_chart** (Dashboard → Chart).
   - Setup a dashboard tab and group
   - Give the chart a label   
   - Click **Done**

3. Wire it together and **Deploy**

4. Open the dashboard

