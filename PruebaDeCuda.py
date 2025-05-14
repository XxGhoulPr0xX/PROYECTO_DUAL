import torch
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU device name: {torch.cuda.get_device_name(0)}")
    print(f"CUDA version: {torch.version.cuda}")
else:
    print("""
    Razones comunes por las que CUDA no está disponible:
    1. No tienes GPU NVIDIA
    2. Los drivers de NVIDIA no están actualizados
    3. Instalaste PyTorch sin soporte CUDA
    4. Tu GPU no es compatible con la versión de CUDA instalada
    """)