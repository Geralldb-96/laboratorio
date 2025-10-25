"""
Servidor de Chat
----------------
Gestiona múltiples clientes mediante sockets TCP y threads.
Los mensajes recibidos de un cliente se retransmiten a todos los demás.
Compatible con entorno local y Docker.
"""

import socket
import threading
import sys
import os

# --- Ajuste de ruta para permitir imports desde src ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chat import CHAT_HOST, CHAT_PORT
from src.utils.logger import log


clientes_conectados = []  # Lista de sockets activos
BUFFER_SIZE = 1024


def manejar_cliente(conn, addr):
    """Atiende a cada cliente conectado."""
    log(f"Cliente conectado desde {addr}", "INFO")
    conn.send("👋 Bienvenido al servidor de chat!\n".encode("utf-8"))

    while True:
        try:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break  # cliente se desconectó

            mensaje = data.decode("utf-8").strip()
            log(f"Mensaje recibido de {addr}: {mensaje}", "INFO")

            # reenviar mensaje a todos los demás
            for cliente in clientes_conectados:
                if cliente != conn:
                    try:
                        cliente.send(f"[{addr[0]}]: {mensaje}".encode("utf-8"))
                    except Exception:
                        pass  # ignorar errores al enviar a clientes desconectados

        except ConnectionResetError:
            log(f"Cliente {addr} se desconectó abruptamente.", "WARNING")
            break

    conn.close()
    if conn in clientes_conectados:
        clientes_conectados.remove(conn)
    log(f"Cliente {addr} desconectado.", "INFO")


def iniciar_servidor():
    """Inicia el servidor de chat y acepta múltiples clientes."""
    # Si estás en local, el host puede ser '0.0.0.0'
    # Si estás en Docker, este valor lo puedes cambiar en el .env o __init__.py
    HOST = CHAT_HOST if CHAT_HOST not in ["localhost", "127.0.0.1"] else "0.0.0.0"
    PORT = CHAT_PORT

    log(f"🚀 Iniciando servidor de chat en {HOST}:{PORT}", "INFO")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        log("💬 Servidor de chat esperando conexiones...", "INFO")

        while True:
            conn, addr = s.accept()
            clientes_conectados.append(conn)
            threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    try:
        iniciar_servidor()
    except KeyboardInterrupt:
        log("🛑 Servidor detenido por el usuario.", "WARNING")

