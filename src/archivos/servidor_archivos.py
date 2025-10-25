import socket
import os
from __init__ import ARCHIVOS_HOST, ARCHIVOS_PORT, DIRECTORIO_ARCHIVOS  # ✅ import directo

BUFFER_SIZE = 1024
os.makedirs(DIRECTORIO_ARCHIVOS, exist_ok=True)

def manejar_cliente(conn, addr):
    print(f"[ARCHIVOS] Conexión de {addr}")
    comando = conn.recv(BUFFER_SIZE).decode()
    nombre = conn.recv(BUFFER_SIZE).decode()

    if comando == "ENVIAR":
        ruta = os.path.join(DIRECTORIO_ARCHIVOS, nombre)
        with open(ruta, "wb") as f:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                f.write(data)
        print(f"[ARCHIVOS] Archivo recibido: {ruta}")

    elif comando == "DESCARGAR":
        ruta = os.path.join(DIRECTORIO_ARCHIVOS, nombre)
        if not os.path.exists(ruta):
            conn.send(b"ERROR")
            print(f"[ARCHIVOS] Archivo no encontrado: {ruta}")
            return
        conn.send(b"OK")
        with open(ruta, "rb") as f:
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                conn.sendall(data)
        print(f"[ARCHIVOS] Archivo enviado: {nombre}")

    conn.close()

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ARCHIVOS_HOST, ARCHIVOS_PORT))
        s.listen(5)
        print(f"[ARCHIVOS] Servidor escuchando en {ARCHIVOS_HOST}:{ARCHIVOS_PORT}")
        while True:
            conn, addr = s.accept()
            manejar_cliente(conn, addr)

if __name__ == "__main__":
    iniciar_servidor()
