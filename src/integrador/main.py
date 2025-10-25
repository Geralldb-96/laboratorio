from flask import Flask, jsonify, request
import socket

CHAT_HOST = "chat"
CHAT_PORT = 6000
ARCHIVOS_HOST = "archivos"
ARCHIVOS_PORT = 5000
BUFFER_SIZE = 1024

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"status": "Integrador activo", "services": ["chat", "archivos"]})

@app.route("/chat", methods=["POST"])
def enviar_mensaje_chat():
    mensaje = request.json.get("mensaje", "Hola desde integrador")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((CHAT_HOST, CHAT_PORT))
        s.sendall(mensaje.encode())
    return jsonify({"status": f"Mensaje enviado al chat: {mensaje}"})

@app.route("/archivo", methods=["POST"])
def enviar_archivo():
    nombre = request.json.get("nombre", "Prueba.txt")
    contenido = request.json.get("contenido", "Archivo de prueba desde integrador")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ARCHIVOS_HOST, ARCHIVOS_PORT))
        s.send(b"ENVIAR")
        s.send(nombre.encode())
        s.sendall(contenido.encode())
    return jsonify({"status": f"Archivo {nombre} cargado correctamente"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
