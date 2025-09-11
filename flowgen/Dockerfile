# Etapa 1: compilación (opcional si quieres compilar siempre)
# Si ya tienes cicflowmeter.jar listo, esta etapa no hace falta.
# FROM maven:3.8.6-openjdk-11 AS build
# WORKDIR /app
# RUN git clone https://github.com/ahlashkari/CICFlowMeter.git .
# RUN mvn package -DskipTests

# Etapa final: runtime
FROM openjdk:11-jre-slim
WORKDIR /app

# Copiamos el jar ya compilado a la imagen
COPY cicflowmeter.jar /app/cicflowmeter.jar
COPY flowgen.py /app/flowgen.py

# Dependencias de Python si tu wrapper las necesita
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*
RUN pip3 install pandas

ENTRYPOINT ["python3", "flowgen.py"]
