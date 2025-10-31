#!/bin/bash
set -e

echo "[*] Iniciando servidor honeypot..."

# ===============================
# CONFIGURACIÓN DE USUARIO
# ===============================
HP_USER="${HP_USER:-spooky}"
HP_PASS="${HP_PASS:-5P00F}"

# Crear usuario si no existe
if ! id -u "$HP_USER" >/dev/null 2>&1; then
  echo "[+] Creando usuario '${HP_USER}'..."
  useradd -m -s /bin/bash "$HP_USER"
else
  echo "[*] Usuario '${HP_USER}' ya existe."
fi

# Establecer contraseña
echo "${HP_USER}:${HP_PASS}" | chpasswd

# ===============================
# CREAR ARCHIVO SEÑUELO
# ===============================
DECOY_FILE="/home/${HP_USER}/secret.txt"
if [ ! -f "$DECOY_FILE" ]; then
  echo "[+] Creando archivo señuelo..."
  echo "Archivo señuelo — no real, propiedad de ${HP_USER}" > "$DECOY_FILE"
  chown ${HP_USER}:${HP_USER} "$DECOY_FILE"
fi

# ===============================
# GUARDAR CREDENCIALES
# ===============================
CREDS_FILE="/run/honeypot_creds.txt"
echo "username: ${HP_USER}" > "$CREDS_FILE"
echo "password: ${HP_PASS}" >> "$CREDS_FILE"
chmod 600 "$CREDS_FILE"

# Si hay carpeta montada desde el host, copiar ahí
if [ -d "/host_creds" ]; then
  cp "$CREDS_FILE" /host_creds/creds.txt 2>/dev/null || true
  chmod 600 /host_creds/creds.txt || true
fi

# ===============================
# CONFIGURAR SSH
# ===============================
if [ ! -f /etc/ssh/sshd_config ]; then
  echo "[+] Configurando SSH..."
  mkdir -p /var/run/sshd
  ssh-keygen -A
  cat <<EOF >/etc/ssh/sshd_config
Port 22
PermitRootLogin no
PasswordAuthentication yes
ChallengeResponseAuthentication no
UsePAM yes
Subsystem sftp /usr/lib/openssh/sftp-server
EOF
fi

# ===============================
# INICIAR SERVICIOS
# ===============================
if command -v rsyslogd >/dev/null 2>&1; then
  echo "[*] Iniciando rsyslog..."
  /usr/sbin/rsyslogd || true
fi

echo "===================================="
echo "   Servidor honeypot listo"
echo "   Usuario: ${HP_USER}"
echo "   Contraseña: ${HP_PASS}"
echo "===================================="

echo "[*] Iniciando servicio SSH..."
exec /usr/sbin/sshd -D -e
