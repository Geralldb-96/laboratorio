import socket
import pytest

HOST = "127.0.0.1"
PORT = 6000

def test_servidor_chat_responde():
    """Verifica que el servidor de chat está activo y responde."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            s.connect((HOST, PORT))
            s.sendall(b"Ping desde test")
            data = s.recv(1024)
        assert data, "El servidor no respondió al mensaje."
    except ConnectionRefusedError:
        pytest.skip("Servidor de chat no está ejecutándose actualmente.")
