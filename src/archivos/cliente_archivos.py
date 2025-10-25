"""
Cliente de Archivos
-------------------
Permite subir o descargar archivos hacia/desde el servidor de archivos.
Comunicación por sockets TCP, compatible con entorno Docker.
"""

import socket
import os
import logging
from src.archivos import ARCHIVOS_HOST, ARCHIVOS_PORT, DIRECTORIO_ARCHIVOS
from src.utils.logger import log


# ------------------------------------------------
# Configuración
# ------------------------------------------------
ARCHIVOS_HOST = os.getenv("ARCHIVOS_HOST", "localhost")
ARCHIVOS_PORT = int(os.getenv("ARCHIVOS_PORT", 5000))
DIRECTORIO_LOCAL = os.getenv("DIRECTORIO_LOCAL", "./data")

# Crear carpeta local si no existe
os.makedirs(DIRECTORIO_LOCAL, exist_ok=True)

# Configurar logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ------------------------------------------------
# Funciones de conexión
# ------------------------------------------------
def enviar_archivo(nombre_archivo: str):
    """Envía un archivo local al servidor"""
    ruta = os.path.join(DIRECTORIO_LOCAL, nombre_archivo)
    if not os.path.exists(ruta):
        logging.error(f"Archivo '{ruta}' no encontrado.")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ARCHIVOS_HOST, ARCHIVOS_PORT))
        s.sendall(b"1")  # opción: subir archivo
        s.sendall(nombre_archivo.encode())

        with open(ruta, "rb") as f:
            while True:
                datos = f.read(4096)
                if not datos:
                    break
                s.sendall(datos)

    logging.info(f"Archivo '{nombre_archivo}' enviado correctamente al servidor.")


def descargar_archivo(nombre_archivo: str):
    """Solicita un archivo al servidor y lo guarda localmente"""
    ruta_destino = os.path.join(DIRECTORIO_LOCAL, f"descargado_{nombre_archivo}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ARCHIVOS_HOST, ARCHIVOS_PORT))
        s.sendall(b"2")  # opción: descargar archivo
        s.sendall(nombre_archivo.encode())

        with open(ruta_destino, "wb") as f:
            while True:
                datos = s.recv(4096)
                if not datos:
                    break
                if datos.startswith(b"ERROR"):
                    logging.error(datos.decode())
                    os.remove(ruta_destino)
                    return
                f.write(datos)

    logging.info(f"Archivo recibido correctamente y guardado como '{ruta_destino}'.")


# ------------------------------------------------
# Interfaz de consola
# ------------------------------------------------
def menu():
    """Interfaz básica para subir o descargar archivos"""
    print("\n=== CLIENTE DE ARCHIVOS ===")
    print("1. Subir archivo al servidor")
    print("2. Descargar archivo del servidor")
    opcion = input("Seleccione una opción (1/2): ").strip()

    if opcion == "1":
        archivo = input("Nombre del archivo a enviar (debe estar en ./data): ").strip()
        enviar_archivo(archivo)
    elif opcion == "2":
        archivo = input("Nombre del archivo a descargar (debe existir en el servidor): ").strip()
        descargar_archivo(archivo)
    else:
        print("Opción no válida.")


# ------------------------------------------------
# Ejecución principal
# ------------------------------------------------
if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\n[INFO] Cliente cerrado por el usuario.")
    except Exception as e:
        logging.error(f"Error en el cliente: {e}")

