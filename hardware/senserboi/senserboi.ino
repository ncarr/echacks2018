#include <ESP8266WiFi.h>
#include <WebSocketClient.h>

const char* ssid  = "echacks";
const char* password = "Fall2020";
char path[] = "/";
char host[] = "192.168.9.28";
  
WebSocketClient webSocketClient;
// Use WiFiClient class to create TCP connections
WiFiClient client;

//Valves
int valve1 = 15;
int valve2 = 13;
int valve3= 12;

//Mic
int mic = A0;
int sensorValue = 0;
int measurementsToAverage = 50;
int loud;

void setup() {
  // Pin + serial initialization
  pinMode(valve1, INPUT);
  pinMode(valve2, INPUT);
  pinMode(valve3, INPUT);
  pinMode(mic, INPUT);
  Serial.begin(9600);
  delay(10);

  //Wifi init
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  delay(1000);
  // Connect to the websocket server
  if (client.connect(host, 6789)) {
    Serial.println("Connected");
  } else {
    Serial.println("Connection failed.");
    while(1) {
      // Hang on failure
    }
  }

  // Handshake with the server
  webSocketClient.path = path;
  webSocketClient.host = host;
  if (webSocketClient.handshake(client)) {
    Serial.println("Handshake successful");
  } else {
    Serial.println("Handshake failed.");
    while(1) {
      // Hang on failure
    }
  }
}

void loop() {
  String data;
  // Websocket
  if (client.connected()) {
    webSocketClient.getData(data);
    if (data.length() > 0) {
      Serial.print("Received data: ");
      Serial.println(data);
    }

    //Valve read
    int v1 = digitalRead(valve1);
    int v2 = digitalRead(valve2);
    int v3 = digitalRead(valve3);
  
    //
    float avgNoise = 0;
    for(int i = 0; i < measurementsToAverage; i ++){
      avgNoise += analogRead(mic);
      delay(1);
    }
    avgNoise /= measurementsToAverage;
    if(avgNoise >= 200){
      loud = 1;
    } else {
      loud = 0;
    }
  
    String result = String(v1) + " " + String(v2) + " " + String(v3) + " " + String(loud);
    Serial.println(result);
    
    webSocketClient.sendData(result);
    delay(100);
  } else {
    Serial.println("Client disconnected.");
    while (1) {
      // Hang on disconnect.
    }
  }
}
