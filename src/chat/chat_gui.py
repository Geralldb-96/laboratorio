"""
Interfaz gráfica del cliente de chat
------------------------------------
Permite conectarse al servidor, enviar y recibir mensajes en tiempo real.
Usa PyQt5 y sockets TCP.
"""

import socket
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QTextEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from colorama import Fore, Style, init
from chat import CHAT_HOST, CHAT_PORT

# Inicializa colorama
init(autoreset=True)


class VentanaChat(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cliente de Chat - PyQt5")
        self.setGeometry(400, 200, 500, 400)

        # Socket del cliente
        self.sock = None

        # Componentes de la interfaz
        layout = QVBoxLayout()

        self.label_titulo = QLabel("💬 Chat Multi-Cliente")
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #00BFFF;")
        layout.addWidget(self.label_titulo)

        self.texto_chat = QTextEdit()
        self.texto_chat.setReadOnly(True)
        self.texto_chat.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        layout.addWidget(self.texto_chat)

        self.entrada_mensaje = QLineEdit()
        self.entrada_mensaje.setPlaceholderText("Escribe tu mensaje...")
        layout.addWidget(self.entrada_mensaje)

        self.boton_enviar = QPushButton("Enviar")
        self.boton_enviar.clicked.connect(self.enviar_mensaje)
        layout.addWidget(self.boton_enviar)

        self.setLayout(layout)

        # Conexión automática al servidor
        self.conectar_servidor()

    def conectar_servidor(self):
        """Crea el socket y se conecta al servidor."""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((CHAT_HOST, CHAT_PORT))
            self.texto_chat.append(f"✅ Conectado al servidor {CHAT_HOST}:{CHAT_PORT}\n")
            hilo = threading.Thread(target=self.recibir_mensajes, daemon=True)
            hilo.start()
        except Exception as e:
            QMessageBox.critical(self, "Error de conexión", f"No se pudo conectar: {e}")
            self.close()

    def recibir_mensajes(self):
        """Hilo que escucha los mensajes entrantes."""
        while True:
            try:
                data = self.sock.recv(1024).decode()
                if not data:
                    break
                self.texto_chat.append(f"{data}")
            except Exception:
                break

    def enviar_mensaje(self):
        """Envía el texto del campo de entrada al servidor."""
        msg = self.entrada_mensaje.text().strip()
        if msg:
            try:
                self.sock.sendall(msg.encode())
                self.texto_chat.append(f"🟢 Tú: {msg}")
                self.entrada_mensaje.clear()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo enviar el mensaje: {e}")
        else:
            QMessageBox.information(self, "Atención", "Escribe un mensaje antes de enviar.")

    def closeEvent(self, event):
        """Cierra la conexión limpia al salir."""
        try:
            if self.sock:
                self.sock.close()
        except:
            pass
        event.accept()


# Punto de entrada principal
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ventana = VentanaChat()
    ventana.show()
    sys.exit(app.exec_())
