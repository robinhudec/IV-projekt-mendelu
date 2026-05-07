#include <SoftwareSerial.h>
 
SoftwareSerial xbee(2, 3);
  
void setup() {
  Serial.begin(9600);
  xbee.begin(9600);
  Serial.println("Gate pripraven");
}
 
void loop() {
  // -------------------
  // PŘÍKAZY Z BACKENDU
  // -------------------
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
 
    if (cmd == "TEMP") {
      xbee.println("GET_TEMP");
    }
    else if (cmd == "LIGHT") {
      xbee.println("GET_LIGHT");
    }
    else if (cmd.startsWith("RGB ")) {
      xbee.println(cmd); 
      Serial.println("Odeslano do LED: " + cmd);
    }
  }
 
  // ----------------------------
  // PŘÍJEM ODPOVĚDÍ ZE SENSORŮ
  // ----------------------------
  if (xbee.available()) {
    String response = xbee.readStringUntil('\n');
    response.trim();
 
    if (response.startsWith("LIGHT ")) {
      int val = response.substring(6).toInt();
      Serial.print("LIGHT:"); Serial.println(val);
    }
    else if (response.startsWith("TEMP ")) {
      String val = response.substring(5);
      Serial.print("teplota: "); Serial.println(val);    
    }
    else if (response.length() > 0) {
      Serial.println("XBee Info: " + response);
    }
  }
}