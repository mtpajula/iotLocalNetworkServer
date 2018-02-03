/*
  Web Server
  
 */

#include <SPI.h>
#include <Ethernet.h>
// Enter a MAC address and IP address for your controller below.
// The IP address will be dependent on your local network:
byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};
// ================================================== CHANGE TO YOUR OWN
IPAddress ip(192, 168, 1, 199);
// Initialize the Ethernet server library
// with the IP address and port you want to use
// (port 80 is default for HTTP):
EthernetServer server(80);

// DHT
#include "DHT.h"
#define DHTPIN 5     // what digital pin we're connected to
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// RELAY
int rpin   = 3;
int rpower = 2;
String rstatus = "off";

#define ARRAYSIZE 2
String devices[ARRAYSIZE] = { "onoff", "humitemp" };

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  // DHT
  dht.begin();

  // RELAY
  pinMode(rpin, OUTPUT);
  pinMode(rpower, OUTPUT);
  digitalWrite(rpin, LOW);
  digitalWrite(rpower, HIGH);
  

  // start the Ethernet connection and the server:
  Ethernet.begin(mac, ip);
  server.begin();
  Serial.print("server is at ");
  Serial.println(Ethernet.localIP());
}


void loop() {
  // listen for incoming clients
  EthernetClient client = server.available();
  if (client) {
    Serial.println("new client");
    // an http request ends with a blank line

    String getstr = readGet(client);
    
    responseHeader(client);
    
    if (getstr == "/virtualdevs") {
      virtualDevs(client);
    } else if (getstr == "/virtualdevs/humitemp") {
      dhtRoot(client);
    } else if (getstr == "/virtualdevs/humitemp/status") {
      dhtStatus(client);
    } else if (getstr == "/virtualdevs/onoff") {
      relayRoot(client);
    } else if (getstr == "/virtualdevs/onoff/status") {
      relayStatus(client);
    } else if (getstr == "/virtualdevs/onoff/on") {
      relayOn(client);
    } else if (getstr == "/virtualdevs/onoff/off") {
      relayOff(client);
    } else {
      defaultResponse(client);
    }
    
    // give the web browser time to receive the data
    delay(1);
    // close the connection:
    client.stop();
    Serial.println("client disconnected");
  }
}

String readGet(EthernetClient client) {
  boolean currentLineIsBlank = true;
  String inputString = "";
  String recordString = "";
  boolean record = false;
  while (client.connected()) {
    if (client.available()) {
      char c = client.read();
      Serial.write(c);

      inputString += c;
      if (inputString.endsWith(" ") && record) {
        Serial.println("[GET END]");
        record = false;
      }

      if (record) {
        recordString += c;
      }

      if (inputString.endsWith("GET ")) {
        Serial.print("[GET FOUND]");
        record = true;
      }
      
      // if you've gotten to the end of the line (received a newline
      // character) and the line is blank, the http request has ended,
      // so you can send a reply
      if (c == '\n' && currentLineIsBlank) {

        //Serial.println(recordString);
        //defaultResponse(client);
        return recordString;
        //break;
      }
      if (c == '\n') {
        // you're starting a new line
        currentLineIsBlank = true;
      } else if (c != '\r') {
        // you've gotten a character on the current line
        currentLineIsBlank = false;
      }
    }
  }
}

String devicesToStringArray() {
  // [ "Ford", "BMW", "Fiat" ]
  String res = "[";
  for (int i =0; i < ARRAYSIZE; i++) {
    res += "\"" + devices[i] + "\"";
    if (i < ARRAYSIZE - 1) {
      res += ",";
    }
  }
  return res + "]";
}

void relayRoot(EthernetClient client) {
  String str = createJsonKeyValue("device", "relay", true);
  str = str + "," + createJsonKeyValue("task","onoff", true);
  sendJson(client, str);
}

void relayOn(EthernetClient client) {
  digitalWrite(rpin, HIGH);
  rstatus = "on";
  relayStatus(client);
}

void relayOff(EthernetClient client) {
  digitalWrite(rpin, LOW);
  rstatus = "off";
  relayStatus(client);
}

void relayStatus(EthernetClient client) {
  String str = createJsonKeyValue("status",rstatus, true);
  sendJson(client, str);
}

void dhtRoot(EthernetClient client) {
  //{"device":"owmtemp","task":"weatherStation"}
  String res = createJsonKeyValue("device","dht22",true);
  res += "," + createJsonKeyValue("task","humitemp",true);
  sendJson(client, res);
}

void dhtStatus(EthernetClient client) {
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  
  String sens = "{" + createJsonKeyValue("temp",String(t),true);
  sens += "," + createJsonKeyValue("humidity",String(h),true) + "}";

  String res = createJsonKeyValue("status",sens, false);
  sendJson(client, res);
}

void virtualDevs(EthernetClient client) {
  String res = createJsonKeyValue("devices",devicesToStringArray(),false);
  sendJson(client, res);
}

void sendJson(EthernetClient client, String str) {
  str = "{" + str + "}";
  client.println(str);
}

String createJsonKeyValue(String key, String value, boolean quote) {
  String res = "\"" + key + "\":";
  if (quote) {
    res += "\"";
  }
  res += value;
  if (quote) {
    res += "\"";
  }
  return res;
}

void responseHeader(EthernetClient client) {
  // send a standard http response header
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: application/json");
  client.println("Connection: close");  // the connection will be closed after completion of the response
  //client.println("Refresh: 5");  // refresh the page automatically every 5 sec
  client.println();
}

void defaultResponse(EthernetClient client) {
  client.println("<html>empty</html>");
}

