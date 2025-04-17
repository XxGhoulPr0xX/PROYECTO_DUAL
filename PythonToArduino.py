from conexionArduino import *
from DetectarPorCamara import *

class PythonToArduino:
    def __init__(self, path_model, confianza, puerto, baudrate):
        self.alpha = ModeloCamara(path_model, confianza)
        self.charlie = conexionArduino(puerto, baudrate)
        if not self.charlie.establecerConexion():
            raise RuntimeError("No se pudo conectar al Arduino")

    def mapearClaseToComando(self, clase):
        clases = {
            "biodegradable": ord('B'),  # 'B'
            "carton": ord('C'),
            "vidrio": ord('V'),
            "metal": ord('M'),
            "papel": ord('P'),
            "plastico": ord('O')
        }
        return clases.get(clase.lower())

    def enviarBytes(self, comando):
        if not self.charlie.enviarRespuesta(comando, esperar_confirmacion=True):
            print("⚠️ Fallo en la comunicación con Arduino")
        else:
            print("Comunicación exitosa, envio correcto de datos")

    def ejecutar(self):
        try:
            while True:
                mensaje = self.charlie.esperandoMensaje()
                if mensaje == "objeto detectado":
                    resultado = input("Dame una clase: ").strip()
                    comando = self.mapearClaseToComando(resultado)
                    if comando is not None:
                        self.enviarBytes(comando)
                    else:
                        print("❌ Clase no reconocida")
        except KeyboardInterrupt:
            self.charlie.cerrarConexion()
            print("\nPrograma terminado")


if __name__ == "__main__":
    confianza=0.45
    model_path= "C:\\Users\\XxGho\\OneDrive\\Documentos\\Escuela\\Proceso Dual\\Proyecto\\Python\\Modelos\\Identificacion de objetos\\yoloooo.pt"
    com="COM3"
    serial=9600
    beta=PythonToArduino(model_path,confianza,com,serial)
    beta.ejecutar()