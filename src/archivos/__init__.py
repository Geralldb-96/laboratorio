"""
Paquete: archivos
-----------------
Este módulo gestiona la comunicación de transferencia de archivos
entre cliente y servidor mediante sockets TCP.

Incluye:
- servidor_archivos.py → Servidor que envía archivos binarios.
- cliente_archivos.py → Cliente que solicita y recibe archivos.
- variables de entorno leídas desde .env.
"""

from dotenv import load_dotenv
import os

# Cargar variables de entorno del archivo .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Variables globales accesibles por los demás módulos del paquete
ARCHIVOS_HOST = os.getenv("ARCHIVOS_HOST", "localhost")
ARCHIVOS_PORT = int(os.getenv("ARCHIVOS_PORT", 5000))
DIRECTORIO_ARCHIVOS = os.getenv("DIRECTORIO_ARCHIVOS", os.path.join(os.path.dirname(__file__), "data"))

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Crear carpeta de datos si no existe
os.makedirs(DIRECTORIO_ARCHIVOS, exist_ok=True)
