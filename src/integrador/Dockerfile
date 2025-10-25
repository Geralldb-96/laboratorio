FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Si usas GUI con PyQt o Tkinter, habilitamos la variable de entorno
ENV PYTHONUNBUFFERED=1

# Puerto de integración (si tienes GUI o API)
EXPOSE 8000

# Ejecuta el integrador que conecta los dos servicios
CMD ["python", "main.py"]
