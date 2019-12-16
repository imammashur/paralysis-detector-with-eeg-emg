// register terlebih dahulu di https://www.cloudmqtt.com/
// lalu buat objek dengan nama topic : esp/emg
// cara buat topic bisa cek di https://www.cloudmqtt.com/docs/index.html

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

int temp_emg[10], emg;
float nilai;
 
const char* ssid = "ina-techno";
const char* password =  "2701sahh";
const char* mqttServer = "m11.cloudmqtt.com";
const int mqttPort = 12948;
const char* mqttUser = "mqttUser";
const char* mqttPassword = "mqttUserPassword";
 
WiFiClient espClient;
PubSubClient client(espClient);
 
void setup() {
 
  Serial.begin(115200); 
  pinMde(0, INPUT);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
 
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
 
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
 
    if (client.connect("ESP8266Client", mqttUser, mqttPassword )) {
 
      Serial.println("connected");  
 
    } else {
 
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
 
    }
  }
 
  client.publish("esp/emg", nilai);
  client.subscribe("esp/emg");
 
}
 
void callback(char* topic, byte* payload, unsigned int length) {
 
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
 
  Serial.print("EMG:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
 
  Serial.println();
  Serial.println("-----------------------");
 
}
 
void loop() {

  emg = 0;
  for (int i = 0; i<10; i++)	{
  	temp_emg[i] = analogRead(0);
  	emg = emg+temp_emg[i];
  }
  nilai = emg;

  client.loop();
}
