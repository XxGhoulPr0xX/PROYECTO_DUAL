import serial  # Activa esto si ya tienes el Arduino conectado
import time

class conexionArduino:
    def __init__(self,puerto):
        self.puerto=puerto
        self.arduino=""

    def establecerConexion(self):
        try:
            self.arduino = serial.Serial(self.puerto, 9600, timeout=1)
            print(f"Conexión establecida en {self.puerto}")
            time.sleep(2) 
        except Exception as e:
            print("No se pudo conectar al Arduino:", e)
            self.arduino = None

    def esperandoMensaje(self):
        if self.arduino and self.arduino.in_waiting > 0:
            mensaje = self.arduino.readline().decode().strip()
            if mensaje:
                print("Arduino dice:", mensaje)
                return mensaje
        return None
    
    def enviarRespuesta(self,clase):
        print(f"Enviando a Arduino: {clase}")
        self.arduino.write(f"{clase}\n".encode())
        return None
    
    def cerrarConexion(self):
        return self.arduino.close()
