import os  
import cv2
from ultralytics import YOLO  

class pruebaDelModelo:
    def __init__(self, path, image, confianza):
        self.path = path
        self.image = image
        self.confianza=confianza
        self.label=""
        self.class_labels = {
            0: "biodegradable",
            1: "carton",
            2: "vidrio",
            3: "metal",
            4: "papel",
            5: "plastico"
        }

    def comprobarSiExisteModel(self):
        if not os.path.exists(self.path):
            print(f"Error: El archivo {self.path} no existe.")
            exit()

    def comprobarSiExisteImagen(self):
        if not os.path.exists(self.image):
            print(f"Error: La imagen {self.image} no existe.")
            exit()  

    def analizarImagenUsandoModelo(self):
        self.comprobarSiExisteImagen()
        self.comprobarSiExisteModel()
        model = YOLO(self.path)
        results = model(self.image, conf=self.confianza)
        return results  

    def mostrarResultados(self):
        results = self.analizarImagenUsandoModelo()
        for result in results:
            classes = result.boxes.cls.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()
            for class_index, confidence in zip(classes, confidences):
                if confidence >= self.confianza:
                    self.label = self.class_labels.get(int(class_index), "Desconocido")
            img_resultado = result.plot()
            cv2.imshow("Resultado de la detección", img_resultado)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def getLabelObjeto(self):
        return self.label
        
    def run(self):
        return self.mostrarResultados()
    
if __name__ == "__main__":
    confianza=0.45
    model_path = "C:\\Users\\José Luis\\Documents\\PROYECTO_DUAL-main\\PROYECTO_DUAL-main\\Modelos\\Identificacion de objetos\\yoloooo.pt"
    img_path = "C:\\Users\\José Luis\\Documents\\PROYECTO_DUAL-main\\PROYECTO_DUAL-main\\IMG\\vi.webp"

    alpha = pruebaDelModelo(model_path, img_path, confianza)
    alpha.run()
