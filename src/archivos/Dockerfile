FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /app/data
EXPOSE 5000
CMD ["python", "servidor_archivos.py"]

