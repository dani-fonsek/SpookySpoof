FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y tcpdump libpcap-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY capture.py .

CMD ["python", "capture.py"]

