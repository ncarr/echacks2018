/*
  Remote Valve Release - For Watering System
*/

// Import required libraries
int input = A0;
int sensorValue = 0;
int measurementsToAverage = 50;

void setup(void)
{ 
  pinMode(input, INPUT);
  // Start Serial
  Serial.begin(115200);
}

void loop() {
  float avgNoise = 0;
  for(int i = 0; i < measurementsToAverage; i ++){
    avgNoise += analogRead(input);
    delay(1);
  }
  avgNoise /= measurementsToAverage;
  if(avgNoise >= 200){
    Serial.println("loud ahhhh");
  } else {
    Serial.println("shhh quiet");
  }
}
