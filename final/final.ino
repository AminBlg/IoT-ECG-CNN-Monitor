#include <WiFi.h>              // include librarry to connect on wifi 
#include <Preferences.h> 

#include <WiFiClient.h>        //include library to connect to the server 

#include <BluetoothSerial.h>   // library to comminicate with th bleutooth of the esp32 
#include <esp_bt.h>

#include "DHT.h"               //library of th DHT22 

#define VARIABLE_LABEL "sensor" // Assign the variable label
#define DEVICE_LABEL "esp32" // Assig the device label


const char* ssid = "Nissou";           // Name of the Wifi 
const char* password = "Nissou2004";   // pswd of the Wifi 

const char* serverIP = "192.168.154.27"; //  My server IP address
const uint16_t serverPort = 8888;        //  My  server port

#define DHTPIN 5            // DHT connected in pin 5 
#define DHTTYPE DHT22       // Select the type of the DHT
DHT dht(DHTPIN,DHTTYPE);

const unsigned long TIME_INTERVAL = 5000;     // time of storing 5(s)
unsigned long previousMillis;


float h ,e ,t ;  // Declare value type of the variables 


void setup() 
{
  
  Serial.begin(115200);
  
  pinMode(22, INPUT);    // Setup for leads off detection LO +
  pinMode(23, INPUT);     // Setup for leads off detection LO -
 
  dht.begin();
  
  previousMillis = millis();
  
  wificon();        // function to connect the esp32 to the Wifi 
  
  delay(2000);

}

void loop()
{  

  float A[100][3];   // Declare an 2D array to store the data from the Sensors 

  setModemSleep(); // function to set the esp32 in Sleep Mode 

  delay(2000);
  
 if (millis() - previousMillis >= TIME_INTERVAL) {
    previousMillis = millis();


          
      for(int i=0; i<20 ; i++)
        {
                dht22();
                ECG();
       
            A[i][0] = t;
            A[i][1] = h;
            A[i][2] = e;

            delay(10);
        }}
    

  wakeModemSleep();  // Function to set the esp32 in the Active Mode 

   delay(2000);
  
  
    
  for(int i=0; i<20 ; i++)
    {
     dsend(A[i][0],A[i][1],A[i][2]);   // Function to send the received data to the Server 
    }    
    delay(2000);

}


///////////////////////////////** Sleep Mode **//////////////////////////////////////////////////

void setModemSleep()
{
  Serial.println("Modem sleep mode :");
  disableWiFi();
  disableBluetooth();
  setCpuFrequencyMhz(80);            //Set the frequency of the CPU to 80 MHz
  Serial.println("--------------------------");
  return;
}

///////////////////////////////** Turn OFF the Wifi  **//////////////////////////////////////////

void disableWiFi() 
{
  Serial.println(" 1/ WiFi disconnected!");
  WiFi.disconnect(true);  // Disconnect from the network
  WiFi.mode(WIFI_OFF);    // Switch WiFi off
  delay(500);
  return;
}

///////////////////////////////** Turn off the Bluetooth  **//////////////////////////////////////

void disableBluetooth() 
{
  Serial.println(" 2/ Bluetooth stop!");
  btStop();
  delay(500);  
  return;
}

///////////////////////////////** Active Mode **//////////////////////////////////////////////////


void wakeModemSleep()
{ 
  Serial.println("Active mode:");
  setCpuFrequencyMhz(240);         // Set the frequency of the CPU to 240 MHz
  delay(500);
  enableWiFi();
  delay(500);
  return;
  
}

///////////////////////////////** Turn ON the Wifi   **///////////////////////////////////////////

void enableWiFi()
{

  WiFi.disconnect(false);  // Reconnect the network
  WiFi.mode(WIFI_STA);    // Switch WiFi on
  delay(500);
  Serial.println("START WIFI");

  WiFi.begin(ssid, password); 
  
  while (WiFi.status() != WL_CONNECTED) 
    {
      Serial.print(".");
    }

  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  delay(500);

}

///////////////////////////////** Read data from DHT22  **/////////////////////////////////////////

void dht22()
{
   h= dht.readHumidity();
   t= dht.readTemperature();

   if(isnan(h)||isnan(t))
      {
          Serial.println("Echec reception"); 
          return;
      }
      

}



///////////////////////////////** Read data from  the ECG    **///////////////////////////////////////////

void ECG()
{
   if((digitalRead(22) == 0)||(digitalRead(23)== 0))
   {
      e=analogRead(A0);
      return;
  }

  //Wait for a bit to keep serial data from saturating
  delay(10);
}



void wificon()
{
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
}

  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  delay(500);
  
}




void dsend( float T,  float H,   float E)
{
   
  WiFiClient client;

  if (client.connect(serverIP, serverPort)) {
   
    Serial.println("Connected to server:  ");
    client.print(T);
    client.print(" , ");
    client.print(H);
    client.print(" , ");
    client.print(E);
    client.flush();
    delay(100);
    client.stop();

    Serial.print ("T= ");
    Serial.println (T);
    Serial.print ("H= ");
    Serial.println (H);
    Serial.print ("E= ");
    Serial.println (E);
    }
   else {
    Serial.println("Connection failed.");
    delay(1000);
  }
}
