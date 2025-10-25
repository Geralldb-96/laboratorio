import socket
from colorama import Fore, Style, init
from integrador import CHAT_HOST, CHAT_PORT, ARCHIVOS_HOST, ARCHIVOS_PORT

init(autoreset=True)

BUFFER_SIZE = 1024

def enviar_mensaje_chat(mensaje):
    """Envía un mensaje temporal al servicio de chat."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((CHAT_HOST, CHAT_PORT))
            s.sendall(mensaje.encode())
        print(Fore.GREEN + f"[Chat] Mensaje enviado: {mensaje}")
    except Exception as e:
        print(Fore.RED + f"[Chat] Error: {e}")

def solicitar_archivo(nombre):
    """Solicita un archivo al servidor de archivos y lo guarda."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ARCHIVOS_HOST, ARCHIVOS_PORT))
            s.sendall(nombre.encode())
            estado = s.recv(BUFFER_SIZE)
            if estado.startswith(b"ERROR"):
                print(Fore.RED + estado.decode())
                return
            with open(f"recibido_{nombre}", "wb") as f:
                while True:
                    data = s.recv(BUFFER_SIZE)
                    if not data:
                        break
                    f.write(data)
            print(Fore.GREEN + f"[Archivos] Archivo recibido: recibido_{nombre}")
    except Exception as e:
        print(Fore.RED + f"[Archivos] Error: {e}")
