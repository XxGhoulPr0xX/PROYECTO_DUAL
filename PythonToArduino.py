from conexionArduino import *
from DetectarPorCamara import *

class PythonToArduino:
    def __init__(self, path_model, confianza, puerto, baudrate):
        self.alpha = ModeloCamara(path_model, confianza)
        self.charlie = conexionArduino(puerto, baudrate)
        self.timeDetection=2
        self.lastCommand=None
        self.timeOfLastSend=0
        self.shippingInterval=0.5
        self.bandera=False
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
                if self.bandera is False:
                    mensaje = self.charlie.esperandoMensaje()
                    if mensaje == "objeto detectado":
                        self.bandera = True
                        self.alpha.continuar()
                        print("🔍 Iniciando detección...")
                        tiempo_inicio = time.time()
                        self.lastCommand = None  # Resetear al iniciar nueva detección
                if self.bandera is True:
                    resultado = self.alpha.obtenerDeteccion()
                    if time.time() - tiempo_inicio >= self.timeDetection:
                        self.bandera = False
                        self.alpha.pausar()
                        print("⏸️ Cámara pausada, esperando nuevo objeto...")
                        continue
                    if resultado:
                        comando = self.mapearClaseToComando(resultado)
                        if (comando is not None and comando != self.lastCommand and 
                            (time.time() - self.timeOfLastSend) >= self.shippingInterval):
                            print(f"✅ Enviado comando: {comando}")
                            self.enviarBytes(comando)
                            self.lastCommand = comando
                            self.timeOfLastSend = time.time()
                        else:
                            print("Resultado no enviado, el mismo objeto detectado que el anterior")
        except KeyboardInterrupt:
            self.alpha.pausar()
            self.charlie.cerrarConexion()
            print("\nPrograma terminado")


if __name__ == "__main__":
    confianza=0.75
    model_path = "C:\\Users\\José Luis\\Documents\\PROYECTO_DUAL-main\\PROYECTO_DUAL-main\\Modelos\\Identificacion de objetos\\yoloooo.pt"
    img_path = "C:\\Users\\José Luis\\Documents\\PROYECTO_DUAL-main\\PROYECTO_DUAL-main\\IMG\\vi.webp"
    com="COM3"
    serial=9600
    beta=PythonToArduino(model_path,confianza,com,serial)
    beta.ejecutar()