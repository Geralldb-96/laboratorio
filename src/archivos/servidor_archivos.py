import socket
import os
from archivos import ARCHIVOS_HOST, ARCHIVOS_PORT, DIRECTORIO_ARCHIVOS
from colorama import Fore, Style, init
from utils import log

init(autoreset=True)
BUFFER_SIZE = 1024


def enviar_archivo(conn, filename):
    """Envía un archivo binario al cliente."""
    ruta = os.path.join(DIRECTORIO_ARCHIVOS, filename)
    if not os.path.exists(ruta):
        conn.send(b"ERROR")
        log(f"Archivo no encontrado: {ruta}", "WARNING")
        return

    conn.send(b"OK")
    with open(ruta, "rb") as f:
        while True:
            data = f.read(BUFFER_SIZE)
            if not data:
                break
            conn.sendall(data)
    log(f"Archivo enviado: {filename}", "INFO")


def recibir_archivo(conn, filename):
    """Recibe un archivo desde el cliente y lo guarda en el servidor."""
    ruta = os.path.join(DIRECTORIO_ARCHIVOS, filename)
    with open(ruta, "wb") as f:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            f.write(data)
    log(f"Archivo recibido del cliente: {filename}", "INFO")


def iniciar_servidor():
    """Servidor que permite enviar y recibir archivos."""
    log(f"Servidor de archivos escuchando en {ARCHIVOS_HOST}:{ARCHIVOS_PORT}", "INFO")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ARCHIVOS_HOST, ARCHIVOS_PORT))
        s.listen(1)

        while True:
            conn, addr = s.accept()
            log(f"Conexión establecida con {addr}", "DEBUG")

            opcion = conn.recv(BUFFER_SIZE).decode()

            if opcion == "ENVIAR":
                filename = conn.recv(BUFFER_SIZE).decode()
                log(f"Recibiendo archivo del cliente: {filename}", "INFO")
                recibir_archivo(conn, filename)

            elif opcion == "DESCARGAR":
                filename = conn.recv(BUFFER_SIZE).decode()
                log(f"Cliente solicita archivo: {filename}", "INFO")
                enviar_archivo(conn, filename)

            else:
                log(f"Opción desconocida: {opcion}", "ERROR")

            conn.close()


if __name__ == "__main__":
    iniciar_servidor()
