#include <NewPing.h>
#include <ESP32Servo.h>

// Configuración de pines
#define TRIG_PIN 1
#define ECHO_PIN 2
#define MAX_DISTANCE 20
#define SERVO_PIN 13
#define MOTOR_INT1 5  // Puerto para INT1 del L298N
#define MOTOR_INT2 7  // Puerto para INT2 del L298N

NewPing sonar(TRIG_PIN, ECHO_PIN, MAX_DISTANCE);
Servo servoMotor;

const byte angulos[6] = {30, 60, 90, 120, 150, 180};
const char comandos[6] = {'B', 'C', 'V', 'M', 'P', 'O'};
const unsigned int motorComandos[6] = {1000, 1100, 1200, 1300, 1400, 1500}; // ms

void setup() {
  Serial.begin(9600);
  servoMotor.attach(SERVO_PIN);
  servoMotor.write(0);  // Posición inicial
  
  // Configurar pines del motor como salidas
  pinMode(MOTOR_INT1, OUTPUT);
  pinMode(MOTOR_INT2, OUTPUT);
  
  // Asegurar que el motor está detenido al inicio
  detenerMotor();
}

void detenerMotor() {
  digitalWrite(MOTOR_INT1, LOW);
  digitalWrite(MOTOR_INT2, LOW);
}

void moverMotorAdelante(unsigned int duracion) {
  digitalWrite(MOTOR_INT1, HIGH);
  digitalWrite(MOTOR_INT2, LOW);
  delay(duracion);
  detenerMotor(); // Siempre detener después de mover
}

void procesarComando(byte cmd) {
  for (int i = 0; i < 6; i++) {
    if (cmd == comandos[i] || cmd == tolower(comandos[i])) {
      servoMotor.write(angulos[i]);
      moverMotorAdelante(motorComandos[i]);
      delay(500); // Pequeña pausa antes de resetear servo
      servoMotor.write(0);
      Serial.println("recibido");  // Confirmación
      return;
    }
  }
  Serial.println("comando_invalido");
}

void loop() {
  static unsigned long ultima_deteccion = 0;
  unsigned long tiempo_actual = millis();
  
  int distancia = sonar.ping_cm();
  
  if (distancia > 0 && distancia < 10 && tiempo_actual - ultima_deteccion > 3000) {
    ultima_deteccion = tiempo_actual;
    Serial.println("objeto detectado");
    
    unsigned long inicio_espera = tiempo_actual;
    while (millis() - inicio_espera < 2000) {
      if (Serial.available() > 0) {
        byte entrada = Serial.read();
        procesarComando(entrada);
        break;
      }
      delay(50); // Pequeña pausa para no saturar
    }
  }
  delay(100);
}