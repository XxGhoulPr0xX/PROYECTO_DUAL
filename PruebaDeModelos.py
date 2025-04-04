# Importación de librerías necesarias
import os  # Para trabajar con rutas y archivos del sistema
from ultralytics import YOLO  # Modelo YOLO para detección de objetos

# Ruta al modelo pre-entrenado (archivo .pt)
model_path = "C:\\Users\\XxGho\\Documents\\Escuela\\Proceso Dual\\Proyecto\\Python\\best.pt"

# Verificación de que el modelo existe
if not os.path.exists(model_path):
    print(f"Error: El archivo {model_path} no existe.")
    exit()  # Termina el programa si no encuentra el modelo

# Carga el modelo YOLO desde el archivo especificado
model = YOLO(model_path)

# Ruta a la imagen que queremos analizar
img_path = "C:\\Users\\XxGho\\Documents\\Escuela\\Proceso Dual\\Proyecto\\trashnet-master\\data\\dataset-resized\\metal\\metal19.jpg"

# Verificación de que la imagen existe
if not os.path.exists(img_path):
    print(f"Error: La imagen {img_path} no existe.")
    exit()  # Termina el programa si no encuentra la imagen

# Procesa la imagen con el modelo para detectar objetos
results = model(img_path)

# Procesamiento de los resultados obtenidos
for result in results:
    # Extrae la información de las detecciones:
    classes = result.boxes.cls.cpu().numpy()  # Índices de las clases detectadas
    confidences = result.boxes.conf.cpu().numpy()  # Niveles de confianza (0-1) de cada detección
    
    # Diccionario para traducir índices numéricos a nombres de clases comprensibles
    class_labels = {
        0: "biodegradable",
        1: "cardboard",
        2: "glass",
        3: "metal",
        4: "paper",
        5: "plastic"
    }

    # Muestra en consola cada objeto detectado con su clase y nivel de confianza
    for class_index, confidence in zip(classes, confidences):
        class_label = class_labels.get(int(class_index), "Desconocido")  # Obtiene nombre legible
        print(f"Clase detectada: {class_label}, Confianza: {confidence:.2f}")  # Formatea la salida

    # Muestra la imagen con los objetos detectados marcados (cuadros y etiquetas)
    result.show()