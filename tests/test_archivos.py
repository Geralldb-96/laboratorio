import os
import socket
import pytest

HOST = "127.0.0.1"
PORT = 5000
ARCHIVO_PRUEBA = "tests/data_test.txt"

@pytest.fixture(scope="module", autouse=True)
def preparar_archivo():
    """Crea un archivo temporal para enviar."""
    os.makedirs("tests", exist_ok=True)
    with open(ARCHIVO_PRUEBA, "w") as f:
        f.write("Contenido de prueba")
    yield
    os.remove(ARCHIVO_PRUEBA)

def test_envio_archivo():
    """Prueba de conexión y envío básico."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.send(b"ENVIAR")
            s.send(os.path.basename(ARCHIVO_PRUEBA).encode())
            with open(ARCHIVO_PRUEBA, "rb") as f:
                for bloque in iter(lambda: f.read(1024), b""):
                    s.sendall(bloque)
        assert True
    except ConnectionRefusedError:
        pytest.skip("Servidor de archivos no está ejecutándose.")
