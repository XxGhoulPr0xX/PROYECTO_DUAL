#include <ESP32Servo.h>

// Configuración de pines
#define IR_PIN 1          // Pin del sensor infrarrojo
#define SERVO_PIN 13      // Pin del servo
#define MOTOR_INT1 5      // Puerto para INT1 del L298N

Servo servoMotor;

const byte angulos[6] = {30, 60, 90, 120, 150, 180};
const char comandos[6] = {'B', 'C', 'V', 'M', 'P', 'O'};
const unsigned int motorComandos[6] = {1000, 1100, 1200, 1300, 1400, 1500}; // ms

void setup() {
    Serial.begin(9600);
    servoMotor.attach(SERVO_PIN);
    servoMotor.write(0);  // Posición inicial
    
    pinMode(MOTOR_INT1, OUTPUT);
    pinMode(IR_PIN, INPUT);  // Configurar pin del IR como entrada
    
    detenerMotor();
}

void detenerMotor() {
    digitalWrite(MOTOR_INT1, LOW);
}

void moverMotorAdelante(unsigned int duracion) {
    digitalWrite(MOTOR_INT1, HIGH);
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
    bool objetoInfrarrojo = (digitalRead(SENSOR_IR_PIN) == LOW);
    
    if (objeto_detectado && tiempo_actual - ultima_deteccion > 3000) {
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