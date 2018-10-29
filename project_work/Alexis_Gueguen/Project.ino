//Include libraries

#include <SerialESP8266wifi.h>
#include <WiFiEsp.h>
#include <WiFiEspClient.h>
#include <WiFiEspServer.h>
#include <WiFiEspUdp.h>
#include <SoftwareSerial.h>
#include <Wire.h>
#include <Adafruit_MLX90614.h>
#include <SPI.h>

// Local Network Settings
byte mac[] = { 0xD4, 0x28, 0xB2, 0xFF, 0xA0, 0xA1 };

// ThingSpeak Settings
char thingSpeakAddress[] = "api.thingspeak.com";
String thingtweetAPIKey = "6PZ0AL7O19VLNOZV";

//Declare and initialize global arrays for WiFi settings
char ssid[] = "MSI3700";
char pass[] = "379g/0R6";

//Set radio status
int status = WL_IDLE_STATUS;

//Declare and initialize global variables/arrays for ThingSpak connection
const char server [] = "thingspeak.com";
const char thingspeakAPIKey[]="NW3IMWE5SFIVWSXI";

//Declare global variable for timing
long lastConnectionTime;
long postingInterval = 30000;
long noSpamming=0;

//Create Client Object
WiFiEspClient client;

//Connect WiFi module object on GPIO pin 6 (RX) and 7 (TX)
SoftwareSerial Serial1(6,7);

//Create sensor object
Adafruit_MLX90614 sensor = Adafruit_MLX90614(); 

float object_temperature;
float temperature;

void setup() {
  //Initialize for debugging
  Serial.begin(115200);
  
  //Initialize serial for ESP
  Serial1.begin(9600);
  
  //Initialize I2C bus
  Wire.begin(); 
  
  //Initialize sensor
  sensor.begin(); 

  //Initialize ESP
  WiFi.init(&Serial1);

  //Check for shields
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield absent, go hang yourself");
    while(true);
  }

  //Attempt to connect to network
  while (status != WL_CONNECTED){
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);

    //Connect to WPA/WPA2
    status = WiFi.begin(ssid,pass);
  }

  Serial.println("Connected to the network");
  printWifiStatus();
}

void loop() {

  //Get oject & ambiant temperature
  object_temperature = sensor.readObjectTempC(); // acquisition de la valeur de la température de l'objet
  temperature = sensor.readAmbientTempC(); // acquisition de la valeur de la température ambiante

  //Get connection info on serial monitor
  while (client.available()){
    char c = client.read();
    Serial.write(c);
  }

  if(noSpamming =0){
    if(object_temperature > 99){
      // Update Twitter via ThingTweet
      updateTwitterStatus("The machine is overheating");
      noSpamming=1;
    }
  }

  if(noSpamming =1){
    if(object_temperature < 99){
      // Update Twitter via ThingTweet
      updateTwitterStatus("The machine has cooled down");
      noSpamming=0;
    }
  }
  
  if (millis() - lastConnectionTime > postingInterval){
    sendThingspeak(object_temperature, temperature);
    lastConnectionTime= millis();
  }
}

void sendThingspeak(float value1,float value2){
  if (client.connectSSL(server, 443)){
    Serial.println("Connected to server");
    client.println("GET /update?api_key=" + String(thingspeakAPIKey) + "&field1=" + String(value1) + "&field2=" + String(value2) + " HTTP/1.1");
    client.println("Host: api.thingspeak.com");
    client.println("Connection: close");
    client.println();
    delay(200);
    Serial.println("Sent to server");
    }
    client.flush();
    client.stop();
}

void printWifiStatus(){
  //Print SSID
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  //Print IP
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
}

void updateTwitterStatus(String tsData){
  if (client.connectSSL(server, 443)){ 
    // Create HTTP POST Data
    tsData = "api_key="+thingtweetAPIKey+"&status="+tsData;
            
    client.print("POST /apps/thingtweet/1/statuses/update HTTP/1.1\n");
    client.print("Host: api.thingspeak.com\n");
    client.print("Connection: close\n");
    client.print("Content-Type: application/x-www-form-urlencoded\n");
    client.print("Content-Length: ");
    client.print(tsData.length());
    client.print("\n\n");

    client.print(tsData);
    client.flush();
    client.stop();
    
    lastConnectionTime = millis();
  }
}
