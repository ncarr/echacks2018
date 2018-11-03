int valve1 = 15;
int valve2 = 13;
int valve3= 12;

void setup() {
  // put your setup code here, to run once:
  pinMode(valve1, INPUT);
  pinMode(valve2, INPUT);
  pinMode(valve2, INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  int v1 = digitalRead(valve1);
  int v2 = digitalRead(valve2);
  int v3 = digitalRead(valve3);
  
  Serial.println(String(v1) + " " + String(v2) + " " + String(v3));
  delay(1000);
}
