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
import logging
from dotenv import load_dotenv
from flask import Flask, jsonify

# -------------------------------
# Cargar variables del entorno
# -------------------------------
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# -------------------------------
# Configuración global
# -------------------------------
CHAT_HOST = os.getenv("CHAT_HOST", "chat_service")
CHAT_PORT = int(os.getenv("CHAT_PORT", 6000))

ARCHIVOS_HOST = os.getenv("ARCHIVOS_HOST", "archivos_service")
ARCHIVOS_PORT = int(os.getenv("ARCHIVOS_PORT", 5000))

INTEGRADOR_HOST = os.getenv("INTEGRADOR_HOST", "0.0.0.0")
INTEGRADOR_PORT = int(os.getenv("INTEGRADOR_PORT", 7000))

INTERFAZ_MODE = os.getenv("INTERFAZ_MODE", "API").upper()
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

# -------------------------------
# Logging y aplicación Flask
# -------------------------------
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger("Integrador")

app = Flask(__name__)

@app.route("/status", methods=["GET"])
def status():
    """Devuelve el estado del integrador y sus servicios."""
    logger.info("Verificando estado del Integrador...")
    return jsonify({
        "status": "ok",
        "service": "Integrador",
        "chat": f"{CHAT_HOST}:{CHAT_PORT}",
        "archivos": f"{ARCHIVOS_HOST}:{ARCHIVOS_PORT}",
        "modo": INTERFAZ_MODE
    })

# Solo para pruebas locales (no Docker)
if __name__ == "__main__":
    app.run(host=INTEGRADOR_HOST, port=INTEGRADOR_PORT, debug=True)

