# 🚀 Sistema Inteligente de Clasificación de Residuos con ESP32

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![YOLOv8](https://img.shields.io/badge/YOLOv8-8.3.115-red)
![ESP32](https://img.shields.io/badge/ESP32-Arduino-green)
![CUDA](https://img.shields.io/badge/CUDA-11.8-purple)

## 📌 Descripción
Sistema automatizado que clasifica residuos en 6 categorías usando visión por computadora (YOLOv8) y controla un sistema mecánico mediante ESP32

## 🧩 Componentes Principales

### 🔌 `conexionArduino.py`
- Manejo de comunicación serial con ESP32
- Timeout configurable (1s por defecto)
- Envío/recepción con confirmación

### 👁️ `DetectarPorCamaravCUDA.py` (Versión GPU)

- Soporte para NVIDIA CUDA
- 6 categorías de clasificación
- Modo pausa/continuación

### 🖼️ `PruebaDeModelos.py`
- Validación con imágenes estáticas
- Muestra bounding boxes y confianza
- Soporta todos los formatos de imagen

### 🤖 `PythonToArduino.py`
- Lógica de control por tiempo
- Protección contra envíos repetidos
- Manejo de errores de conexión

### ⚙️ `ArduinoToPython.ino`
- Control de servo (6 posiciones)
- Manejo de motor DC (L298N)
- Detección por ultrasonido (HC-SR04)
- Protocolo serial personalizado

## 🛠️ Instalación
1. Clonar repositorio:
   git clone https://github.com/tu_usuario/proyecto-clasificacion.git
2. Instalar dependencias:
   pip install -r requirements.txt
3. Para soporte CUDA:
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

## ⚙️ Configuración Hardware
| Componente       | Conexión ESP32 |
|------------------|----------------|
| Sensor HC-SR04   | TRIG:GPIO1, ECHO:GPIO2 |
| Servo SG90       | GPIO13 |
| Motor L298N      | INT1:GPIO5, INT2:GPIO7 |

## 📊 Modelo YOLOv8
- **Clases**: 6 (biodegradable, cartón, vidrio, metal, papel, plástico)
- **Confianza mínima**: 0.45 (ajustable)
- **Rendimiento**: ~60 FPS en RXT 3050

## 🚀 Uso
1. Iniciar sistema Arduino
2. Ejecutar script principal:
   python PythonToArduino.py
3. Esperar detección del sensor
   "Objeto identificado"
5. Esperar respuesta de esp32
6. Recibir respuesta
7. Accionar el modelo de ia
8. Enviar respuesta
9. Recibe respuesta
10. Acciona el motor
11. Acciona el servomotor
  
## 📌 Notas Técnicas
- **Versión CPU**: Usar `DetectarPorCamara.py` si no hay GPU
- **Latencia**: 500ms entre comandos (configurable)
- **Protocolo Serial**:
  - ESP32 → Python: "objeto detectado"
  - Python → ESP32: 'B','C','V','M','P','O'

---
> 💡 **Tip**: Para calibrar el servo, modificar los valores en `angulos[]` del sketch Arduino
