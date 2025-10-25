"""
Paquete: chat
-------------
Gestiona la comunicación de chat multi-cliente basada en sockets TCP.
Incluye:
- chat_servidor.py → Servidor que maneja múltiples clientes.
- chat_cliente.py → Cliente que envía y recibe mensajes.
"""

from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Variables globales del chat
CHAT_HOST = os.getenv("CHAT_HOST", "localhost")
CHAT_PORT = int(os.getenv("CHAT_PORT", 6000))
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
