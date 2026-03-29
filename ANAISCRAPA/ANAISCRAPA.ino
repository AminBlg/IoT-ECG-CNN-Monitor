#include <WiFi.h>
#include <WiFiClient.h>
#include "DHT.h"

#define DHTPIN 5          // Pin where the DHT22 is connected
#define DHTTYPE DHT11     // DHT22 sensor type

const char* ssid = "FALCON";           // Your WiFi SSID
const char* password = "falcon00";   // Your WiFi password

DHT dht(DHTPIN, DHTTYPE);   // Initialize DHT sensor

WiFiClient client;

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  // Connect to WiFi network
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
     Serial.print(".");
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  
  Serial.println("Connected to WiFi");
}

void loop() {

  // Read temperature and humidity from DHT22
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  
  // Check if any reading failed
  if (isnan(humidity) || isnan(temperature)) 
  {
    Serial.println("Failed to read data from DHT22 sensor");
    //return;
  }
  
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print("°C\tHumidity: ");
  Serial.print(humidity);
  Serial.println("%");
  
  // Connect to server
  if (client.connect("192.168.154.27", 8888)) 
  {
    // Send temperature and humidity data to server
    String data = "temperature=" + String(temperature) + "     humidity=" + String(humidity);
    //client.print("POST /path/to/data HTTP/1.1");
    //client.print("Host: server_address");
    //client.print("Content-Length: ");
    //client.print(data.length());
    //client.println();
    client.print(data);
    client.println("deleeegueeeeeeeeeee ");
    client.stop();

    
    Serial.println("Data sent to server");
  }
  else 
  {
    Serial.println("Failed to connect to server");
  }
  
  delay(5000);   // Wait for 5 seconds before sending data again
}
