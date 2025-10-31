FROM debian:latest

# Actualizar e instalar dependencias básicas y SSH
RUN apt-get update && apt-get install -y \
    openssh-server \
    rsyslog \
    bash \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Copiar script de inicialización
COPY server.sh /app/server.sh
RUN chmod +x /app/server.sh

# Crear carpeta para credenciales en caso de montaje
RUN mkdir -p /host_creds /var/run/sshd

# Exponer el puerto SSH
EXPOSE 22

# Ejecutar el script al iniciar el contenedor
ENTRYPOINT ["/app/server.sh"]
