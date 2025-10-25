"""
Paquete: integrador
-------------------
Conecta los servicios de Chat y Archivos.
Puede funcionar en modo GUI (PyQt5) o API (Flask),
según el valor de INTERFAZ_MODE en el archivo .env.

- INTERFAZ_MODE = "GUI"   → lanza interfaz PyQt5
- INTERFAZ_MODE = "API"   → lanza servidor Flask
"""

import os
from dotenv import load_dotenv

# Ruta absoluta del .env dentro del paquete integrador
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")

# Cargar variables del entorno si el archivo existe
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# -------------------------------
# Configuración global
# -------------------------------
CHAT_HOST = os.getenv("CHAT_HOST", "chat_service")
CHAT_PORT = int(os.getenv("CHAT_PORT", 6000))

ARCHIVOS_HOST = os.getenv("ARCHIVOS_HOST", "archivos_service")
ARCHIVOS_PORT = int(os.getenv("ARCHIVOS_PORT", 5000))

# Puerto del integrador (API o GUI)
INTEGRADOR_HOST = os.getenv("INTEGRADOR_HOST", "0.0.0.0")
INTEGRADOR_PORT = int(os.getenv("INTEGRADOR_PORT", 7000))

# Modo de interfaz: GUI (PyQt5) o API (Flask)
INTERFAZ_MODE = os.getenv("INTERFAZ_MODE", "API").upper()

# Nivel de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
