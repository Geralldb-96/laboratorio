"""
Paquete: utils
--------------
Contiene utilidades comunes a todos los servicios del sistema.
Actualmente incluye:

- logger.py → Sistema centralizado de registros (logs) con colores y archivos diarios.
"""

from .logger import log

__all__ = ["log"]
