#include <ESP8266WiFi.h>
#include <WebSocketClient.h>

const char* ssid  = "echacks";
const char* password = "Fall2020";
char path[] = "/";
char host[] = "";
  
WebSocketClient webSocketClient;
// Use WiFiClient class to create TCP connections
WiFiClient client;

int valve1 = 15;
int valve2 = 13;
int valve3= 12;

void setup() {
  // Pin + serial initialization
  pinMode(valve1, INPUT);
  pinMode(valve2, INPUT);
  pinMode(valve3, INPUT);
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
  // put your main code here, to run repeatedly:
  if (client.connected()) {
    webSocketClient.getData(data);
    if (data.length() > 0) {
      Serial.print("Received data: ");
      Serial.println(data);
    }
    
    int v1 = digitalRead(valve1);
    int v2 = digitalRead(valve2);
    int v3 = digitalRead(valve3);
  
    String data = String(v1) + " " + String(v2) + " " + String(v3);
    Serial.println(data);
    webSocketClient.sendData(data);
    delay(100);
  } else {
    Serial.println("Client disconnected.");
    while (1) {
      // Hang on disconnect.
    }
  }
}
