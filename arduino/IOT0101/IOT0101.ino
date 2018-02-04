#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

// === SETTINGS
// WLAN ssid and password
const char* ssid = "...";
const char* password = "...";
// Device name
const String devname = "esprelay01";
// digital output pin number
const int dev = 0;
// ===

ESP8266WebServer server(80);
String devStatus = "off";

String createJsonKeyValue(String key, String value) {
  return "\"" + key + "\":\"" + value + "\"";
}

void sendJson(String str) {
  str = "{" + str + "}";
  server.send(200, "text/plain", str);
}

void handleRoot() {
  String str = createJsonKeyValue("device", devname);
  str = str + "," + createJsonKeyValue("task","onoff");
  sendJson(str);
}

void handleOn() {
  digitalWrite(dev, 1);
  devStatus = "on";
  handleStatus();
}

void handleOff() {
  digitalWrite(dev, 0);
  devStatus = "off";
  handleStatus();
}

void handleStatus() {
  String str = createJsonKeyValue("status",devStatus);
  sendJson(str);
}

void handleNotFound() {
  String str = createJsonKeyValue("error","empty");
  sendJson(str);
}

void setup(void){
  pinMode(dev, OUTPUT);
  digitalWrite(dev, 0);
  
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
 
  if (MDNS.begin("esp8266")) {
    Serial.println("MDNS responder started");
  }

  server.on("/", handleRoot);

  server.on("/on", handleOn);

  server.on("/off", handleOff);

  server.on("/status", handleStatus);

  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void){
  server.handleClient();
}
