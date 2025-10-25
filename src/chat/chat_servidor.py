import socket
import threading
from colorama import Fore, Style, init
from chat import CHAT_HOST, CHAT_PORT

# Inicializa colorama para colores
init(autoreset=True)

clientes = []

def manejar_cliente(conn, addr):
    """Atiende a un cliente y reenvía sus mensajes."""
    print(Fore.YELLOW + f"[+] Cliente conectado: {addr}")
    try:
        while True:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            print(Fore.BLUE + f"{addr} dice: {msg}")
            broadcast(msg, conn)
    except Exception as e:
        print(Fore.RED + f"[!] Error con {addr}: {e}")
    finally:
        conn.close()
        if conn in clientes:
            clientes.remove(conn)
        print(Fore.MAGENTA + f"[-] Cliente desconectado: {addr}")

def broadcast(mensaje, remitente):
    """Envía el mensaje a todos los clientes excepto al remitente."""
    for c in clientes:
        if c != remitente:
            try:
                c.sendall(mensaje.encode())
            except:
                clientes.remove(c)

def iniciar_servidor():
    """Inicia el servidor TCP de chat."""
    print(Style.BRIGHT + Fore.CYAN +
          f"Servidor de chat activo en {CHAT_HOST}:{CHAT_PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((CHAT_HOST, CHAT_PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            clientes.append(conn)
            hilo = threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True)
            hilo.start()

if __name__ == "__main__":
    iniciar_servidor()
