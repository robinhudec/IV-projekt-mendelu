#include <SoftwareSerial.h>
 
SoftwareSerial xbee(2, 3);
const int sensorPin = A0;
 
void setup() {
  Serial.begin(9600);
  xbee.begin(9600);
  Serial.println("Senzor svetla pripraven");
}
 
void loop() {
  if (xbee.available()) {
    String request = xbee.readStringUntil('\n');
    request.trim();
 
    if (request == "GET_LIGHT") {
      int lightValue = analogRead(sensorPin);
      xbee.print("LIGHT ");
      xbee.println(lightValue);
      Serial.print("LIGHT:");
      Serial.println(lightValue);
    }
  }
}