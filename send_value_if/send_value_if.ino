#include <WiFi.h>
#include <Preferences.h>
#include <WiFiClient.h>
#include <BluetoothSerial.h>
#include <esp_bt.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

const char* serverIP = "192.168.154.27"; // Change to your server IP address
const uint16_t serverPort = 8888; // Change to your server port

void setup() {
  Serial.begin(115200);
  delay(1000);




 /* WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }

  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  */
}

void loop() {
wakeModemSleep() ;
/*int myArray[3];
       setModemSleep();

for (int A =0 ; A<3 ;A++)
{

    myArray[A]=random(100);
    delay(1000);
       setModemSleep();
}

  wakeModemSleep();
  
  WiFiClient client;

  if (client.connect(serverIP, serverPort))
  {
   
    Serial.println("Connected to server.");
        for( int i=0; i<3; i++)
        {
           Serial.println(myArray[i]);
            client.print(myArray[i]);
            delay(1000);
        }

  }  
   else 
   {
    Serial.println("Connection failed.");
   }
   delay(3000);
       client.stop();
    setModemSleep();
 delay(3000);   */
}





void setModemSleep() 
{
    Serial.println("Modem sleep mode :");
    disableWiFi();
    disableBluetooth();
    setCpuFrequencyMhz(80);
    Serial.println("--------------------------");

    delay(3000);
}


void disableWiFi(){
    //adc_power_off();
    WiFi.disconnect(true);  // Disconnect from the network
    WiFi.mode(WIFI_OFF);    // Switch WiFi off
    Serial.println(" 1/ WiFi disconnected!");
}


void disableBluetooth(){
    // Quite unusefully, no relevable power consumption
    btStop();
    Serial.println(" 2/ Bluetooth stop!");
}


void wakeModemSleep() 
{   Serial.println("Active mode:");
    setCpuFrequencyMhz(240);
    enableWiFi();

    delay(3000);
}



void enableWiFi()
{
   // adc_power_on();
   //delay(200);
 
    WiFi.disconnect(false);  // Reconnect the network
    WiFi.mode(WIFI_STA);    // Switch WiFi on
 
   // delay(200);
 
    Serial.println("START WIFI");
    
    WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }

  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.println("--------------------------");

 

}
