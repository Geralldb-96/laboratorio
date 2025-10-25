import socket
import threading
from __init__ import CHAT_HOST, CHAT_PORT  # ✅ import directo del mismo paquete

clientes = []

def manejar_cliente(conn, addr):
    print(f"[CHAT] Nueva conexión: {addr}")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            mensaje = data.decode()
            print(f"[{addr}] {mensaje}")
            for c in clientes:
                if c != conn:
                    c.sendall(f"{addr}: {mensaje}".encode())
        except:
            break
    conn.close()
    clientes.remove(conn)
    print(f"[CHAT] Conexión cerrada: {addr}")

def iniciar_chat():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((CHAT_HOST, CHAT_PORT))
        s.listen()
        print(f"[CHAT] Servidor escuchando en {CHAT_HOST}:{CHAT_PORT}")
        while True:
            conn, addr = s.accept()
            clientes.append(conn)
            threading.Thread(target=manejar_cliente, args=(conn, addr)).start()

if __name__ == "__main__":
    iniciar_chat()
