#!/usr/bin/env python3
import time
import os
import joblib
import pandas as pd
from datetime import datetime
import json

# Configuración de rutas
MODEL_PATH = "/home/user/Desktop/SpookySpoof/model/EXPOT.pkl"
CSV_PATH = "/home/user/Desktop/SpookySpoof/flowgen/Processed"
OUTPUT_JSON = "datos.json"  # <- nombre solicitado

# Simulación de carga de modelo
print("\nCargando modelo de deteccion de trafico\n")
time.sleep(1.2)

if os.path.exists(MODEL_PATH):
    try:
        modelo = joblib.load(MODEL_PATH)
        print(f"Modelo cargado desde: {MODEL_PATH}")
    except Exception as e:
        print(f"Error al cargar el modelo: {e}")
else:
    print("Modelo no encontrado, usando simulación de predicción...")

time.sleep(1.5)

# Carga del dataset CSV
print(f"\nLeyendo flujos desde: {CSV_PATH}\n")
time.sleep(1.2)

if os.path.exists(CSV_PATH):
    try:
        if os.path.isdir(CSV_PATH):
            archivos_csv = [f for f in os.listdir(CSV_PATH) if f.endswith(".csv")]
            if archivos_csv:
                archivo = os.path.join(CSV_PATH, archivos_csv[0])
                df = pd.read_csv(archivo)
                print(f"Archivo de flujo leído: {archivo} ({len(df)} registros)")
            else:
                print("No se encontraron archivos CSV en la carpeta Processed.")
        else:
            df = pd.read_csv(CSV_PATH)
            print(f"Archivo de flujo leído: {CSV_PATH} ({len(df)} registros)")
    except Exception as e:
        print(f"Error al leer el CSV: {e}")
else:
    print("Carpeta o archivo CSV no encontrado, continuando con simulación...")

time.sleep(1.5)

# Analisis (simulado)
print("\nIniciando analisis de trafico...\n")
time.sleep(1.5)
print("Analizando paquetes capturados...")
time.sleep(1.2)
print("Aplicando modelo de clasificación...")
time.sleep(1.3)
print("Procesando resultados...\n")
time.sleep(1.8)

# Datos simulados (valores que pediste)
mac_raw = "4c20.b8df.74d9"
# convertir a formato XX:XX:XX:XX:XX:XX y mayúsculas
mac = mac_raw.replace('.', '')            # 4c20b8df74d9
mac = ":".join(mac[i:i+2] for i in range(0, len(mac), 2)).upper()  # 4C:20:B8:DF:74:D9

ip = "192.168.10.50"
paquetes = 300
# Hora en formato ISO 8601 como en tu ejemplo (sin zona)
hora_iso = datetime.now().replace(microsecond=0).isoformat()
# Confianza en porcentaje original (90.6) convertida a decimal (0.906)
confianza_pct = 90.6
confianza_decimal = round(confianza_pct / 100.0, 3)

clasificacion = "BENIGN"

# Mostrar resultados por consola (simulación)
print("───────────────────────────────────────────────")
print(f"  El tráfico analizado ha sido clasificado como:  {clasificacion}")
print("───────────────────────────────────────────────")
print(f"  Dirección MAC:        {mac}")
print(f"  Dirección IP:         {ip}")
print(f"  Paquetes analizados:  {paquetes}")
print(f"  Hora del análisis:    {hora_iso}")
print(f"  Nivel de confianza:   {confianza_pct}%")
print("───────────────────────────────────────────────")
print("\nAnálisis completado con éxito.\n")

# Construir estructura JSON exactamente como pediste (lista con un solo objeto)
datos = [
    {
        "mac": mac,
        "ip": ip,
        "paquetes": paquetes,
        "hora": hora_iso,
        "confianza": confianza_decimal
    }
]

# Guardar en datos.json
with open(OUTPUT_JSON, "w", encoding="utf-8") as archivo:
    json.dump(datos, archivo, ensure_ascii=False, indent=2)

print(f"Archivo '{OUTPUT_JSON}' generado con éxito en {os.getcwd()}")
