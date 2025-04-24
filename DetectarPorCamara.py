import cv2
from ultralytics import YOLO

class ModeloCamara:
    def __init__(self, model_path, conf_threshold=0.45):
        self.modelo = YOLO(model_path)
        self.cap = cv2.VideoCapture(0)
        self.conf_threshold = conf_threshold
        self.class_labels = {
            0: "biodegradable",
            1: "cartón",
            2: "vidrio",
            3: "metal",
            4: "papel",
            5: "plastico"
        }
        
        self.class_colors = {
            0: (0, 0, 255),    
            1: (0, 255, 0),    
            2: (255, 0, 0),    
            3: (0, 255, 255),  
            4: (255, 0, 255),  
            5: (255, 255, 0)   
        }
        self.label = ""
        self.pausado = False  # Nuevo estado para controlar pausa
        self.frame_pausa = None  # Frame congelado cuando está pausado

    def capturarFrame(self):
        if self.pausado:
            return self.frame_pausa if self.frame_pausa is not None else None
        
        ret, frame = self.cap.read()
        if not ret:
            print("Error: No se pudo capturar el frame.")
            return None
        return frame

    def procesarFrame(self, frame):
        if self.pausado:
            return []  # No procesar cuando está pausado
        resultados = self.modelo(frame, conf=self.conf_threshold)
        detecciones = []
        
        for resultado in resultados:
            for box, class_index, confidence in zip(
                resultado.boxes.xyxy.cpu().numpy(),
                resultado.boxes.cls.cpu().numpy(),
                resultado.boxes.conf.cpu().numpy()
            ):
                if confidence > self.conf_threshold:
                    label = self.class_labels.get(int(class_index), "Desconocido")
                    self.label = label  # Actualizar la etiqueta
                    deteccion = {
                        "box": list(map(int, box)),
                        "label": label,
                        "color": self.class_colors.get(int(class_index), (0, 255, 0))
                    }
                    detecciones.append(deteccion)
        
        return detecciones

    def dibujarDetecciones(self, frame, detecciones):
        for det in detecciones:
            x1, y1, x2, y2 = det["box"]
            label = det["label"]
            color = det["color"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        return frame

    def pausar(self):
        if not self.pausado:
            self.pausado = True
            self.frame_pausa = self.capturarFrame()
            print("Cámara pausada")

    def continuar(self):
        if self.pausado:
            self.pausado = False
            self.frame_pausa = None
            print("Cámara continuada")

    def obtenerDeteccion(self):
        frame = self.capturarFrame()
        if frame is None:
            return "Error: No se pudo capturar el frame."
        
        detecciones = self.procesarFrame(frame)
        frame = self.dibujarDetecciones(frame, detecciones)

        cv2.imshow("Cámara", frame)
        
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            return "salir"
        
        return self.label
