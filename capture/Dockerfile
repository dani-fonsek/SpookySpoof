FROM python:3.11-slim

# Instalar dependencias necesarias para Scapy
RUN apt-get update && apt-get install -y tcpdump && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY capture.py .

CMD ["python", "capture.py"]



