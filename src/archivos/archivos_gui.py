"""
Interfaz gráfica para transferencia de archivos
-----------------------------------------------
Permite subir y descargar archivos al servidor desde una GUI con PyQt5.
"""

import socket
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QLineEdit, QTextEdit, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from archivos import ARCHIVOS_HOST, ARCHIVOS_PORT, DIRECTORIO_ARCHIVOS
from utils import log


BUFFER_SIZE = 1024


class VentanaArchivos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cliente de Archivos - PyQt5")
        self.setGeometry(500, 250, 550, 400)

        layout = QVBoxLayout()

        titulo = QLabel("📁 Cliente de Archivos")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #00BFFF;")
        layout.addWidget(titulo)

        self.texto_estado = QTextEdit()
        self.texto_estado.setReadOnly(True)
        self.texto_estado.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        layout.addWidget(self.texto_estado)

        self.entrada_archivo = QLineEdit()
        self.entrada_archivo.setPlaceholderText("Nombre del archivo o selecciónalo con el botón...")
        layout.addWidget(self.entrada_archivo)

        btn_seleccionar = QPushButton("📂 Seleccionar archivo local")
        btn_seleccionar.clicked.connect(self.seleccionar_archivo)
        layout.addWidget(btn_seleccionar)

        btn_subir = QPushButton("⬆️ Subir al servidor")
        btn_subir.clicked.connect(self.subir_archivo)
        layout.addWidget(btn_subir)

        btn_descargar = QPushButton("⬇️ Descargar del servidor")
        btn_descargar.clicked.connect(self.descargar_archivo)
        layout.addWidget(btn_descargar)

        self.setLayout(layout)

    def seleccionar_archivo(self):
        """Abre un diálogo para seleccionar un archivo desde el sistema local."""
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "", "Todos los archivos (*)")
        if archivo:
            self.entrada_archivo.setText(archivo)
            self.texto_estado.append(f"✅ Archivo seleccionado: {archivo}")

    def subir_archivo(self):
        """Envía un archivo al servidor."""
        ruta = self.entrada_archivo.text().strip()
        if not ruta or not os.path.exists(ruta):
            QMessageBox.warning(self, "Error", "Selecciona un archivo válido para enviar.")
            return

        filename = os.path.basename(ruta)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ARCHIVOS_HOST, ARCHIVOS_PORT))
                s.send(b"ENVIAR")
                s.send(filename.encode())

                with open(ruta, "rb") as f:
                    while True:
                        data = f.read(BUFFER_SIZE)
                        if not data:
                            break
                        s.sendall(data)

            msg = f"✅ Archivo '{filename}' enviado correctamente."
            self.texto_estado.append(msg)
            log(msg, "INFO")

        except Exception as e:
            QMessageBox.critical(self, "Error de conexión", str(e))
            log(f"Error al enviar archivo: {e}", "ERROR")

    def descargar_archivo(self):
        """Descarga un archivo del servidor."""
        entrada_usuario = self.entrada_archivo.text().strip()
        if not entrada_usuario:
            QMessageBox.warning(self, "Error", "Ingresa el nombre del archivo a descargar.")
            return

        # Aseguramos que solo quede el nombre, sin rutas absolutas
        nombre_archivo = os.path.basename(entrada_usuario)
        ruta_destino = os.path.normpath(os.path.join(DIRECTORIO_ARCHIVOS, f"descargado_{nombre_archivo}"))

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ARCHIVOS_HOST, ARCHIVOS_PORT))
                s.send(b"DESCARGAR")
                s.send(nombre_archivo.encode())

                estado = s.recv(BUFFER_SIZE)
                if estado == b"ERROR":
                    self.texto_estado.append(f"❌ El servidor no encontró '{nombre_archivo}'.")
                    return

                # Guardar archivo recibido
                with open(ruta_destino, "wb") as f:
                    while True:
                        data = s.recv(BUFFER_SIZE)
                        if not data:
                            break
                        f.write(data)

            msg = f"✅ Archivo '{nombre_archivo}' descargado en {ruta_destino}"
            self.texto_estado.append(msg)
            log(msg, "INFO")

        except Exception as e:
            QMessageBox.critical(self, "Error de conexión", str(e))
            log(f"Error al descargar archivo: {e}", "ERROR")

