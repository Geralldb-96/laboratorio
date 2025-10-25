"""
Módulo: logger.py
-----------------
Maneja el sistema de logs centralizado para todos los servicios.
Usa la librería 'logging' de Python y 'colorama' para mostrar
mensajes con formato de color y nivel de severidad.
"""

import logging
from colorama import Fore, Style, init
import os
from datetime import datetime

# Inicializar colorama
init(autoreset=True)

# Carpeta para guardar logs (dentro del proyecto o contenedor)
LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Archivo de log por fecha
log_file = os.path.join(LOG_DIR, f"registro_{datetime.now().strftime('%Y%m%d')}.log")

# Formato base
LOG_FORMAT = "%(asctime)s - [%(levelname)s] - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Configuración del logger
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT
)

# Colores por nivel
COLORES = {
    "INFO": Fore.CYAN,
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.RED,
    "DEBUG": Fore.GREEN
}

def log(mensaje, nivel="INFO"):
    """Imprime y guarda mensajes con formato y color."""
    nivel = nivel.upper()
    color = COLORES.get(nivel, Fore.WHITE)
    texto = f"{color}{Style.BRIGHT}[{nivel}] {mensaje}"
    print(texto)

    if nivel == "INFO":
        logging.info(mensaje)
    elif nivel == "WARNING":
        logging.warning(mensaje)
    elif nivel == "ERROR":
        logging.error(mensaje)
    elif nivel == "DEBUG":
        logging.debug(mensaje)
    else:
        logging.info(mensaje)
