from integrador import INTERFAZ_MODE, LOG_LEVEL
from colorama import Fore, Style, init

init(autoreset=True)

if INTERFAZ_MODE == "GUI":
    from PyQt5.QtWidgets import QApplication
    from integrador.gui import VentanaIntegrador
    import sys

    print(Style.BRIGHT + Fore.CYAN + "Iniciando en modo GUI...")
    app = QApplication([])
    ventana = VentanaIntegrador()
    ventana.show()
    sys.exit(app.exec_())

elif INTERFAZ_MODE == "API":
    from flask import Flask, jsonify, request
    from integrador.comunicacion import enviar_mensaje_chat, solicitar_archivo

    app = Flask(__name__)

    @app.route("/chat", methods=["POST"])
    def chat():
        data = request.json
        mensaje = data.get("mensaje", "")
        enviar_mensaje_chat(mensaje)
        return jsonify({"status": "Mensaje enviado"})

    @app.route("/archivo", methods=["GET"])
    def archivo():
        nombre = request.args.get("nombre")
        solicitar_archivo(nombre)
        return jsonify({"status": f"Arch
