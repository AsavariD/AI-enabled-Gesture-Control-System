#include <WiFiS3.h>

const char* ssid = "CTPL_Airtel";
const char* pass = "ctpl08nov12";

WiFiServer server(80);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while (!Serial) delay(10);

  pinMode(LED_BUILTIN, OUTPUT);

  //connect to wifi
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, pass);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print("Status: ");
    Serial.println(WiFi.status());
  }
  
  // Display connection information
  Serial.println("Connection Information:");
  Serial.print("  Status: ");
  Serial.println(WiFi.status());
  Serial.print("  SSID: ");
  Serial.println(WiFi.SSID());
  Serial.print("  IP Address: ");
  delay(2000);
  Serial.println(WiFi.localIP());
  Serial.print("");

  server.begin();
}

void loop() {
  // put your main code here, to run repeatedly:

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Connection lost! Attempting to reconnect...");
    WiFi.begin(ssid, pass);
  }
  else {
    WiFiClient client = server.available();
    if (client) {
      Serial.println("Client connected.");
      while (client.connected()) {
        if (client.available()) {
          String message = client.readStringUntil('\n');
          Serial.print("Received: ");
          Serial.println(message);

          // Respond or act upon message
          client.println("Arduino received: " + message);

          if (message == "1"){
            digitalWrite(LED_BUILTIN, HIGH);
          }
          else if (message == "2"){
            digitalWrite(LED_BUILTIN, LOW);
          }
        }
      }
      client.stop();
      Serial.println("Client disconnected.");
    }
  }

}
