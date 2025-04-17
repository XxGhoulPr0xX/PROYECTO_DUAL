#include <NewPing.h>
#include <ESP32Servo.h>

// Configuración Hardware, como alimentar varios servomotores y como activar el modulo del puente:
#define TRIG_PIN 1
#define ECHO_PIN 2
#define MAX_DISTANCE 20
#define SERVO_PIN 13

NewPing sonar(TRIG_PIN, ECHO_PIN, MAX_DISTANCE);
Servo servoMotor;

const byte angulos[6] = {30, 60, 90, 120, 150, 180};
const char comandos[6] = {'B', 'C', 'V', 'M', 'P', 'O'};

void setup() {
  Serial.begin(9600);
  servoMotor.attach(SERVO_PIN);
  servoMotor.write(0);  // Posición inicial
}

void procesarComando(byte cmd) {
  for (int i = 0; i < 6; i++) {
    if (cmd == comandos[i] || cmd == tolower(comandos[i])) {
      servoMotor.write(angulos[i]);
      Serial.println("recibido");  // Confirmación
      delay(1500);
      servoMotor.write(0);
      return;
    }
  }
  Serial.println("comando_invalido");
}

void loop() {
  static unsigned long ultima_deteccion = 0;
  int distancia = sonar.ping_cm();
  if (distancia > 0 && distancia < 10 && millis() - ultima_deteccion > 3000) {
    ultima_deteccion = millis();
    Serial.println("objeto detectado");
    unsigned long inicio_espera = millis();
    while (millis() - inicio_espera < 2000) {
      if (Serial.available() > 0) {
        byte entrada = Serial.read();
        procesarComando(entrada);
        break;
      }
    }
  }
  delay(100);  // Evita saturación
}