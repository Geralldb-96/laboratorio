from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QLineEdit, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from integrador.comunicacion import enviar_mensaje_chat, solicitar_archivo

class VentanaIntegrador(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Integrador - Chat & Archivos")
        self.setGeometry(400, 200, 500, 400)

        layout = QVBoxLayout()

        self.texto_log = QTextEdit()
        self.texto_log.setReadOnly(True)
        layout.addWidget(QLabel("📡 Integrador"))
        layout.addWidget(self.texto_log)

        self.entrada_mensaje = QLineEdit()
        self.entrada_mensaje.setPlaceholderText("Escribe un mensaje para el chat...")
        layout.addWidget(self.entrada_mensaje)

        btn_enviar = QPushButton("Enviar al Chat")
        btn_enviar.clicked.connect(self.enviar_chat)
        layout.addWidget(btn_enviar)

        self.entrada_archivo = QLineEdit()
        self.entrada_archivo.setPlaceholderText("Nombre del archivo a solicitar...")
        layout.addWidget(self.entrada_archivo)

        btn_archivo = QPushButton("Solicitar Archivo")
        btn_archivo.clicked.connect(self.solicitar_archivo)
        layout.addWidget(btn_archivo)

        self.setLayout(layout)

    def enviar_chat(self):
        mensaje = self.entrada_mensaje.text().strip()
        if mensaje:
            enviar_mensaje_chat(mensaje)
            self.texto_log.append(f"→ Enviado al chat: {mensaje}")
            self.entrada_mensaje.clear()
        else:
            QMessageBox.warning(self, "Atención", "Debe ingresar un mensaje.")

    def solicitar_archivo(self):
        nombre = self.entrada_archivo.text().strip()
        if nombre:
            solicitar_archivo(nombre)
            self.texto_log.append(f"→ Solicitud enviada para '{nombre}'")
            self.entrada_archivo.clear()
        else:
            QMessageBox.warning(self, "Atención", "Debe ingresar el nombre del archivo.")
