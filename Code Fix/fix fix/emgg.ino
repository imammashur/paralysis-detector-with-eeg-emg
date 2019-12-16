#include <ESP8266WiFi.h> // load library wifi esp8266
#include <PubSubClient.h> // load library untuk mqtt

int emg=0; // variabel keluaran emg
float nilai; // variabel untuk keluaran emg yg diubah jadi float
char hasil[8]; // variabel yg dikirim ke broker
 

// pengaturan wifi dan mqtt
const char* ssid = "Guntur";
const char* password =  "guntur123";
const char* mqttServer = "postman.cloudmqtt.com";
const int mqttPort = 15198;
const char* mqttUser = "wqwqirvv";
const char* mqttPassword = "PrZi1N3woApH";
 
WiFiClient espClient;
PubSubClient client(espClient);
 
void setup() {
 
  Serial.begin(9600); // pengaturan serial untuk debugging
  pinMode(0, INPUT); // pengaturan bahwa pin 0 adalah pin input, dalam hal ini adalah emg
  WiFi.begin(ssid, password); // mulai connecting wifi
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
 
  // set server mqtt
  client.setServer(mqttServer, mqttPort); 
  client.setCallback(callback);
 
  // connecting mqtt
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

  // tes hasil mqtt dengan publish ke broker
  client.publish("esp/emg", hasil);

  // cek hasil mqtt dengan subscribe dari broker
  client.subscribe("esp/emg");
 
}
 
 // fungsi utuk callback pesan pada broker
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
  emg = analogRead(A0); // baca nilai emg
  nilai = emg; // nilai = emg
  dtostrf(nilai, 6, 2, hasil); // ubah data "nilai" ke bentuk string dlm variabel "hasil"
  client.publish("esp/emg", hasil); // kirim niai "hasil" ke topic "esp/emg" pada broker
  client.loop(); // sda
  emg = 0;  // kembalikan nilai emg jadi 0 untuk mempermudah pembacaan berikutnya
}
