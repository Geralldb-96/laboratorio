import socket
import os
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from archivos import ARCHIVOS_PORT, DIRECTORIO_ARCHIVOS
from src.utils.logger import log


BUFFER_SIZE = 4096


def iniciar_servidor():
    """Inicia el servidor de archivos y espera conexiones para upload/download."""
    HOST = "0.0.0.0"  # Escuchar en todas las interfaces dentro del contenedor
    log(f"Servidor de archivos escuchando en {HOST}:{ARCHIVOS_PORT}", "INFO")

    # Crear socket TCP reutilizable
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, ARCHIVOS_PORT))
        s.listen(5)

        while True:
            conn, addr = s.accept()
            log(f"Conexión establecida con {addr}", "INFO")

            with conn:
                data = conn.recv(BUFFER_SIZE).decode("utf-8")
                if not data:
                    continue

                # Espera comandos tipo "UPLOAD:archivo.txt" o "DOWNLOAD:archivo.txt"
                partes = data.split(":", 1)
                if len(partes) != 2:
                    conn.send("ERROR: Comando inválido".encode("utf-8"))
                    continue

                comando, nombre_archivo = partes
                archivo_path = os.path.join(DIRECTORIO_ARCHIVOS, nombre_archivo.strip())

                if comando == "UPLOAD":
                    with open(archivo_path, "wb") as f:
                        while True:
                            chunk = conn.recv(BUFFER_SIZE)
                            if not chunk:
                                break
                            f.write(chunk)
                    log(f"Archivo recibido: {nombre_archivo}", "INFO")

                elif comando == "DOWNLOAD":
                    if os.path.exists(archivo_path):
                        with open(archivo_path, "rb") as f:
                            conn.sendfile(f)
                        log(f"Archivo enviado: {nombre_archivo}", "INFO")
                    else:
                        conn.send("ERROR: Archivo no encontrado.".encode("utf-8"))

                else:
                    conn.send("ERROR: Comando desconocido.".encode("utf-8"))


if __name__ == "__main__":
    iniciar_servidor()
