import socket
import os
from archivos import ARCHIVOS_HOST, ARCHIVOS_PORT, DIRECTORIO_ARCHIVOS
from utils import log

BUFFER_SIZE = 1024


def enviar_archivo(filename):
    """Envía un archivo local al servidor."""
    ruta = os.path.join(DIRECTORIO_ARCHIVOS, filename)
    if not os.path.exists(ruta):
        log(f"No se encontró el archivo {ruta}", "ERROR")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ARCHIVOS_HOST, ARCHIVOS_PORT))
        s.send(b"ENVIAR")
        s.send(filename.encode())

        with open(ruta, "rb") as f:
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                s.sendall(data)
        log(f"Archivo enviado al servidor: {filename}", "INFO")


def descargar_archivo(filename):
    """Solicita un archivo del servidor."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ARCHIVOS_HOST, ARCHIVOS_PORT))
        s.send(b"DESCARGAR")
        s.send(filename.encode())

        estado = s.recv(BUFFER_SIZE)
        if estado == b"ERROR":
            log(f"El servidor no encontró el archivo {filename}", "WARNING")
            return

        ruta_destino = os.path.join(DIRECTORIO_ARCHIVOS, f"descargado_{filename}")
        with open(ruta_destino, "wb") as f:
            while True:
                data = s.recv(BUFFER_SIZE)
                if not data:
                    break
                f.write(data)
        log(f"Archivo descargado: {ruta_destino}", "INFO")


if __name__ == "__main__":
    print("=== Cliente de Archivos ===")
    print("1. Subir archivo al servidor")
    print("2. Descargar archivo del servidor")

    opcion = input("Seleccione una opción (1/2): ").strip()

    if opcion == "1":
        archivo = input("Nombre del archivo a enviar (debe existir en tu carpeta data): ").strip()
        enviar_archivo(archivo)
    elif opcion == "2":
        archivo = input("Nombre del archivo a descargar: ").strip()
        descargar_archivo(archivo)
    else:
        log("Opción inválida", "ERROR")
