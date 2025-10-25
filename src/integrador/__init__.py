"""
Paquete: integrador
-------------------
Conecta los servicios de Chat y Archivos.
Puede funcionar en modo GUI (PyQt5) o API (Flask),
según el valor de INTERFAZ_MODE en el archivo .env.
"""

from dotenv import load_dotenv
import os

# Cargar variables de entorno
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Configuración global
CHAT_HOST = os.getenv("CHAT_HOST", "chat_service")
CHAT_PORT = int(os.getenv("CHAT_PORT", 6000))
ARCHIVOS_HOST = os.getenv("ARCHIVOS_HOST", "archivos_service")
ARCHIVOS_PORT = int(os.getenv("ARCHIVOS_PORT", 5000))
INTERFAZ_MODE = os.getenv("INTERFAZ_MODE", "GUI").upper()
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
