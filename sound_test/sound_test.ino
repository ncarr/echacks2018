/*
  Remote Valve Release - For Watering System
*/

// Import required libraries
int input = A0;
int sensorValue = 0;



void setup(void)
{ 

  
  pinMode(input, INPUT);
  // Start Serial
  Serial.begin(115200);


}

void loop() {

  sensorValue = analogRead(input);
  Serial.println(sensorValue);
  delay(100);

}
