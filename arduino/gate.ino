#include <SoftwareSerial.h>
 
// Nastavení pinů podle cvičení 6
SoftwareSerial xbee(2, 3); // RX = pin 2, TX = pin 3 
const int buttonPin = 4;   // Tlačítko pro vysílání 
const int ledPin = 6;      // LED pro indikaci příjmu
 
int lastState = LOW;       // Minulý stav tlačítka pro detekci hrany 
 
void setup() {
  Serial.begin(9600);      // Sériový monitor pro ladění
  xbee.begin(9600);        // Rychlost komunikace s XBee
 
  pinMode(buttonPin, INPUT); // Nastavení pinu tlačítka
  pinMode(ledPin, OUTPUT);   // Nastavení pinu LED
  digitalWrite(ledPin, LOW); // Výchozí stav LED zhasnut
 
  Serial.println("Gate (Vysilac i Prijimac) spustena");
}
 
void loop() {
  // ---------------------------------------------------------
  // 1. ČÁST: VYSÍLAČ (Čtení tlačítka a odeslání dat)
  // ---------------------------------------------------------
  int currentState = digitalRead(buttonPin);
 
  // Detekce náběžné hrany (stisk) 
  
    String prikaz = Serial.readStringUntil('\n');
    prikaz.trim();
    xbee.println(prikaz);                   // Odeslání zprávy přes XBee
    Serial.println(prikaz);       // Výpis do sériového monitoru
    delay(50);                              // Debouncing (ošetření zákmitů tlačítka)
  
  lastState = currentState;                 // Uložení stavu pro další cyklus
 
  // ---------------------------------------------------------
  // 2. ČÁST: PŘIJÍMAČ (Čtení dat z XBee a reakce)
  // ---------------------------------------------------------
  if (xbee.available()) {                   // Pokud jsou dostupná data z XBee
    String zprava = xbee.readStringUntil('\n');
    zprava.trim();                          // Odstranění bílých znaků
    Serial.print("Prijato: "); 
    Serial.println(zprava); 
  }
}