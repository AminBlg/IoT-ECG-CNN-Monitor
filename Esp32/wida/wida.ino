#include <WiFi.h>
#include <Preferences.h>
#include <WiFiClient.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

const char* serverIP = "192.168.154.27"; // Change to your server IP address
const uint16_t serverPort = 8888; // Change to your server port

void setup() {
  Serial.begin(115200);
  delay(1000);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }

  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  WiFiClient client;

  if (client.connect(serverIP, serverPort)) {
   
    Serial.println("Connected to server.");
    client.print("Hello from ESP32!");
    client.stop();
    }
   else {
    Serial.println("Connection failed.");
  }
  delay(3000);
}
