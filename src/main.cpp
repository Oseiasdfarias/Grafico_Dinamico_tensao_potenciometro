#include <Arduino.h>
#define LED 2

void setup() {
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
}

void loop() {

  // Lê a entrada no analógico ADC1_0:
  int potenciometro = analogRead(A0);
  Serial.println(potenciometro);

  digitalWrite(LED, HIGH);
  delay(20);
  digitalWrite(LED, LOW);
  delay(20);
}
