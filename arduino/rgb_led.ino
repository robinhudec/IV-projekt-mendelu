#include <SoftwareSerial.h>

// Definice pinů
const int redPin = 11;
const int greenPin = 10;
const int bluePin = 9;

// Nastavení XBee (RX pin 2, TX pin 3)
SoftwareSerial xbee(2, 3); 

void setup() {
  Serial.begin(9600);
  xbee.begin(9600);
  
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);

  setColor(0, 0, 0);
  Serial.println("RGB READY");
}

void loop() {
  if (xbee.available()) {
    String command = xbee.readStringUntil('\n');
    command.trim();

    if (command.startsWith("RGB ")) {
      String numbers = command.substring(4);
      numbers.trim();
      
      int firstSpace = numbers.indexOf(' ');
      int secondSpace = numbers.indexOf(' ', firstSpace + 1);

      if (firstSpace > 0 && secondSpace > 0) {
        int r = numbers.substring(0, firstSpace).toInt();
        int g = numbers.substring(firstSpace + 1, secondSpace).toInt();
        int b = numbers.substring(secondSpace + 1).toInt();

        r = constrain(r, 0, 255);
        g = constrain(g, 0, 255);
        b = constrain(b, 0, 255);

        setColor(r, g, b);
        xbee.println("RGB OK"); // Odpověď posíláme zpět do XBee
        Serial.println("RGB OK");
      } else {
        xbee.println("RGB ERROR");
        Serial.println("RGB ERROR");
      }
    } else {
      xbee.println("UNKNOWN");
      Serial.println("UNKNOWN COMMAND");
    }
  }
}

void setColor(int r, int g, int b) {
  analogWrite(redPin, r);
  analogWrite(greenPin, g);
  analogWrite(bluePin, b);
}