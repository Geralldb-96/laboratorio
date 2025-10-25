import socket
import threading
from colorama import Fore, Style, init
from chat import CHAT_HOST, CHAT_PORT

init(autoreset=True)

def recibir(sock):
    """Recibe mensajes del servidor y los muestra."""
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            print(Fore.GREEN + f"\n{data}")
        except:
            print(Fore.RED + "[!] Desconectado del servidor.")
            break

def iniciar_cliente():
    """Inicia el cliente del chat."""
    print(Style.BRIGHT + Fore.CYAN + f"Conectando a {CHAT_HOST}:{CHAT_PORT} ...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((CHAT_HOST, CHAT_PORT))
        threading.Thread(target=recibir, args=(s,), daemon=True).start()

        print(Style.BRIGHT + Fore.YELLOW + "=== Chat activo ===")
        print("Escribe 'salir' para desconectarte.\n")

        while True:
            msg = input("> ")
            if msg.lower() == "salir":
                break
            s.sendall(msg.encode())

if __name__ == "__main__":
    iniciar_cliente()
