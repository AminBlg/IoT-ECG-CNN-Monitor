

 

/****************************************
 * Define Constants
 ****************************************/
#define VARIABLE_LABEL "sensor" // Assign the variable label
#define DEVICE_LABEL "esp32" // Assig the device label

void setup() {
  Serial.begin(115200);

 pinMode(15, INPUT); // Setup for leads off detection LO +
  pinMode(4, INPUT); // Setup for leads off detection LO -
 
}
 
void loop() {
  
  if((digitalRead(4) == 1)||(digitalRead(15)== 1)){
    Serial.println('!');
  }
  else{
    // send the value of analog input 0:
      Serial.println(analogRead(34));
  }
  //Wait for a bit to keep serial data from saturating
  delay(8);
}