#include <NewPing.h>

#define TRIG_PIN 1
#define ECHO_PIN 2
#define MAX_DISTANCE 20

NewPing sonar(TRIG_PIN, ECHO_PIN, MAX_DISTANCE);

void setup() {
  Serial.begin(9600);
}

void loop() {
  delay(1000);
  int distancia = sonar.ping_cm();

  if (distancia > 0 && distancia < 10) {
    Serial.println("objeto detectado");
  }
}
