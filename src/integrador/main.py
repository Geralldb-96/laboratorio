"""
Módulo: main.py
Servicio integrador — Conecta Chat y Archivos
-------------------------------------------------
Expone una API REST con Flask para verificar el estado
y probar la comunicación entre contenedores Docker.
"""

from flask import Flask, jsonify
import socket
import logging
import os

# Configuración de logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Configuración general
app = Flask(__name__)

CHAT_HOST = os.getenv("CHAT_HOST", "chat_service")
CHAT_PORT = int(os.getenv("CHAT_PORT", 6000))
ARCHIVOS_HOST = os.getenv("ARCHIVOS_HOST", "archivos_service")
ARCHIVOS_PORT = int(os.getenv("ARCHIVOS_PORT", 5000))
INTEGRADOR_HOST = os.getenv("INTEGRADOR_HOST", "0.0.0.0")
INTEGRADOR_PORT = int(os.getenv("INTEGRADOR_PORT", 7000))


# ---------------------------------------------
# Funciones auxiliares
# ---------------------------------------------
def probar_conexion(host, port, servicio):
    """Prueba la conexión TCP con un servicio"""
    try:
        with socket.create_connection((host, port), timeout=3):
            logger.info(f"Conexión exitosa con {servicio} en {host}:{port}")
            return {"status": "ok", "service": servicio}
    except Exception as e:
        logger.error(f"Error conectando con {servicio}: {e}")
        return {"status": "error", "service": servicio, "message": str(e)}


# ---------------------------------------------
# Rutas de la API
# ---------------------------------------------
@app.route("/")
def home():
    return jsonify({"message": "Servicio Integrador activo", "status": "ok"})


@app.route("/status")
def status():
    return jsonify({
        "integrador": "online",
        "chat_service": f"{CHAT_HOST}:{CHAT_PORT}",
        "archivos_service": f"{ARCHIVOS_HOST}:{ARCHIVOS_PORT}"
    })


@app.route("/test/chat")
def test_chat():
    result = probar_conexion(CHAT_HOST, CHAT_PORT, "chat_service")
    return jsonify(result), 200 if result["status"] == "ok" else 500



@app.route("/test/archivos", methods=["GET"])
def test_archivos():
    """Prueba de conexión con el servicio de archivos"""
    try:
        logging.info(f"Intentando conectar con {ARCHIVOS_HOST}:{ARCHIVOS_PORT} ...")
        with socket.create_connection((ARCHIVOS_HOST, ARCHIVOS_PORT), timeout=3):
            return jsonify({"message": f"Conectado a {ARCHIVOS_HOST}", "status": "ok"})
    except Exception as e:
        logging.error(f"Error conectando con archivos_service: {e}")
        return jsonify({
            "message": str(e),
            "service": "archivos_service",
            "status": "error"
        }), 500

# ---------------------------------------------
# Ejecución principal
# ---------------------------------------------
if __name__ == "__main__":
    from waitress import serve
    logger.info(f"Iniciando Integrador (modo producción) en {INTEGRADOR_HOST}:{INTEGRADOR_PORT}")
    serve(app, host=INTEGRADOR_HOST, port=INTEGRADOR_PORT)

