import time
from datetime import datetime

print("\n[INICIANDO ANÁLISIS DE TRÁFICO...]\n")
time.sleep(1.5)

print("Analizando paquetes capturados...")
time.sleep(1.2)
print("Aplicando modelo de clasificación...")
time.sleep(1.3)
print("Procesando resultados...\n")
time.sleep(1.8)

# Datos simulados
mac = "00:1A:92:5F:3C:7B"
ip = "192.168.0.105"
paquetes = 300
hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
confianza = 90.6

# Resultado final
print("───────────────────────────────────────────────")
print("  El tráfico analizado ha sido clasificado como:  BENIGNO")
print("───────────────────────────────────────────────")
print(f"  Dirección MAC:        {mac}")
print(f"  Dirección IP:         {ip}")
print(f"  Paquetes analizados:  {paquetes}")
print(f"  Hora del análisis:    {hora}")
print(f"  Nivel de confianza:   {confianza}%")
print("───────────────────────────────────────────────")
print("\nAnálisis completado con éxito.\n")
