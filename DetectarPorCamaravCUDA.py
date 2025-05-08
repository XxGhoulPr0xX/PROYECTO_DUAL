import cv2
import torch
from ultralytics import YOLO

class ModeloCamara:
    def __init__(self, model_path, conf_threshold=0.45):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Usando dispositivo: {self.device}")
        self.modelo = YOLO(model_path).to(self.device)
        self.modelo.fuse()
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("No se pudo abrir la cámara")
            
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
            0: (0, 0, 255),    # Rojo
            1: (0, 255, 0),    # Verde
            2: (255, 0, 0),    # Azul
            3: (0, 255, 255),  # Amarillo
            4: (255, 0, 255),  # Magenta
            5: (255, 255, 0)   # Cian
        }
        self.label = ""
        self.pausado = False
        self.frame_pausa = None

    def frameGpuAnalizador(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_tensor = torch.from_numpy(frame_rgb).float() / 255.0
        frame_tensor = frame_tensor.permute(2, 0, 1).unsqueeze(0)
        return frame_tensor.to(self.device)

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
            return []
        frame_tensor = self.frameGpuAnalizador(frame)
        with torch.no_grad():
            resultados = self.modelo(frame_tensor, conf=self.conf_threshold)
        detecciones = []
        for resultado in resultados:
            boxes = resultado.boxes.xyxy.cpu().numpy()
            class_indices = resultado.boxes.cls.cpu().numpy()
            confidences = resultado.boxes.conf.cpu().numpy()
            
            for box, class_index, confidence in zip(boxes, class_indices, confidences):
                if confidence > self.conf_threshold:
                    label = self.class_labels.get(int(class_index), "Desconocido")
                    self.label = label
                    deteccion = {
                        "box": list(map(int, box)),  # Ya están en coordenadas correctas
                        "label": label,
                        "color": self.class_colors.get(int(class_index), (0, 255, 0)),
                        "confidence": float(confidence)
                    }
                    detecciones.append(deteccion)
        
        return detecciones

    def dibujarDetecciones(self, frame, detecciones):
        for det in detecciones:
            x1, y1, x2, y2 = det["box"]
            label = det["label"]
            color = det["color"]
            confidence = det.get("confidence", 0)
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f"{label} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
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

if __name__ == "__main__":
    confianza = 0.55
    model_path = "C:\\Users\\XxGho\\OneDrive\\Documentos\\Escuela\\Proceso Dual\\Proyecto\\Python\\Modelos\\Identificacion de objetos\\yoloooo.pt"
    alpha = ModeloCamara(model_path, confianza)
    try:
        while True:
            result = alpha.obtenerDeteccion()
            if result == "salir":
                break
    finally:
        del alpha