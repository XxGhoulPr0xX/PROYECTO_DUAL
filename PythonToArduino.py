import time
# import serial  # Descomentar cuando tengas el Arduino
from inrealtime import *

class PythonToArduino:
    def __init__(self, puerto):
        # self.arduino = serial.Serial(puerto, 9600, timeout=1)  # Descomentar cuando uses Arduino
        self.alpha = ModeloCamara("C:\\Users\\XxGho\\OneDrive\\Documentos\\Escuela\\Proceso Dual\\Proyecto\\Python\\best.pt")
        self.clases = {
            0: "biodegradable",
            1: "cartón",
            2: "vidrio",
            3: "metal",
            4: "papel",
            5: "plastico"
        }

    def EnviarBytes(self, clase):
        if clase not in self.clases.values():
            print("Objeto no identificado")
        else:
            print(f"Enviando: {clase}")
            # self.arduino.write(clase.encode())  # Descomentar cuando uses Arduino
            time.sleep(2)  # Espera para asegurar el envío de datos

    def ejecutar(self):
        while True:
            resultado = self.alpha.obtenerDeteccion()
            
            if resultado == "salir":
                break
                
            if resultado:  # Solo envía si se detecta algo
                self.EnviarBytes(resultado)
                time.sleep(2)  # Pequeño delay para evitar spam de datos
        
        self.alpha.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    beta = PythonToArduino("COM5")
    beta.ejecutar()