import time
# import serial  # Descomentar cuando tengas el Arduino
from PruebaDeModelos import *
from conexionArduino import *
#from DetectarPorCamara import *

class PythonToArduino:
    #def __init__(self,path_model,confianza):
    def __init__(self, path,image,confianza,puerto):
        # self.arduino = serial.Serial(puerto, 9600, timeout=1)  # Descomentar cuando uses Arduino
        #self.alpha = ModeloCamara(path_model,confianza)
        self.alpha=pruebaDelModelo(path,image,confianza)
        self.charlie=conexionArduino(puerto)
        self.clases = {
            0: "biodegradable",
            1: "cartón",
            2: "vidrio",
            3: "metal",
            4: "papel",
            5: "plastico"
        }
        self.charlie.establecerConexion()


    def EnviarBytes(self, clase):
        if clase not in self.clases.values():
            print("Objeto no identificado")
        else:
            self.charlie.enviarRespuesta(clase)
            time.sleep(2)  # Espera para asegurar el envío de datos

    def ejecutar(self):
        self.alpha.mostrarResultados()
        while True:
            mensaje = self.charlie.esperandoMensaje()
            if mensaje == "objeto detectado":
                resultado=self.alpha.getLabelObjeto()
                #resultado=self.alpha.obtenerDeteccion()
                self.EnviarBytes(resultado)
                #time.sleep(2)  # Pequeño delay para evitar spam de datos
            else:
                print("No se detectó ningún objeto válido.")
                self.EnviarBytes("no_detectado")

        #self.alpha.cap.release()
        #cv2.destroyAllWindows()

if __name__ == "__main__":
    confianza=0.45
    model_path= "C:\\Users\\Javier Alvarado\\Documents\\Duales\\PROYECTO_DUAL\\Modelos\\Identificacion de objetos\\best.pt"
    img_path = "C:\\Users\\Javier Alvarado\\Documents\\Duales\\Imagenes\\dataset-resized\\metal\\metal303.jpg"
    com="COM3"
    beta=PythonToArduino(model_path,img_path,confianza,com)
    #beta=PythonToArduino(model_path,confianza)
    beta.ejecutar()