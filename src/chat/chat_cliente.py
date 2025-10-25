"""
Cliente de Chat
---------------
Se conecta al servidor de chat mediante sockets TCP.
Permite enviar y recibir mensajes de forma simultánea.
Compatible con ejecución local y Docker.
"""

import socket
import threading
import sys
import os

# --- Ajuste de ruta para permitir imports desde src ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chat import CHAT_HOST, CHAT_PORT
from src.utils.logger import log

BUFFER_SIZE = 1024


def recibir_mensajes(sock):
    """Hilo que recibe mensajes del servidor y los muestra en pantalla."""
    while True:
        try:
            data = sock.recv(BUFFER_SIZE)
            if not data:
                log("⚠️ Conexión cerrada por el servidor.", "WARNING")
                break
            print(data.decode("utf-8"))
        except ConnectionResetError:
            log("❌ Conexión perdida con el servidor.", "ERROR")
            break
        except Exception as e:
            log(f"Error al recibir mensaje: {e}", "ERROR")
            break


def iniciar_cliente():
    """Inicia el cliente y permite enviar mensajes al servidor."""
    # Si estás en local, usa "localhost"
    # Si estás dentro de Docker, debe coincidir con el nombre del servicio del contenedor (por ejemplo 'chat_service')
    host = CHAT_HOST if CHAT_HOST not in ["0.0.0.0"] else "localhost"
    port = CHAT_PORT

    log(f"🛰️ Conectando al servidor de chat en {host}:{port}...", "INFO")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((host, port))
            log("✅ Conectado al servidor de chat.", "INFO")
        except Exception as e:
            log(f"❌ No se pudo conectar al servidor: {e}", "ERROR")
            return

        # Iniciar hilo para escuchar mensajes entrantes
        threading.Thread(target=recibir_mensajes, args=(sock,), daemon=True).start()

        # Enviar mensajes desde consola
        try:
            while True:
                mensaje = input("Tú: ").strip()
                if not mensaje:
                    continue
                if mensaje.lower() in ["salir", "exit", "quit"]:
                    log("👋 Cerrando conexión...", "INFO")
                    break
                sock.send(mensaje.encode("utf-8"))
        except KeyboardInterrupt:
            log("🛑 Cliente detenido por el usuario.", "WARNING")
        finally:
            sock.close()
            log("🔒 Conexión cerrada.", "INFO")


if __name__ == "__main__":
    iniciar_cliente()
