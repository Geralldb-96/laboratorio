"""
Paquete: chat
-------------
Define los parámetros globales del servicio de chat.
"""
import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

CHAT_HOST = os.getenv("CHAT_HOST", "localhost")
CHAT_PORT = int(os.getenv("CHAT_PORT", 6000))
