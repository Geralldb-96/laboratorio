# Imagen base
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos dependencias y código
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Puerto del chat (TCP)
EXPOSE 6000

# Comando por defecto
CMD ["python", "chat_servidor.py"]
