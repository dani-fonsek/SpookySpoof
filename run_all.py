#!/usr/bin/env python3
import subprocess
import sys
import os

def run_capture():
    print("[*] Ejecutando captura de paquetes...")
    # Ejecutar capture.py con sudo preservando venv
    try:
        subprocess.run(["sudo", "-E", sys.executable, "./capture/capture.py"], check=True)
    except subprocess.CalledProcessError:
        print("[ERROR] Falló la captura de paquetes")
        sys.exit(1)

def run_flowgen():
    print("[*] Ejecutando generación de flujos...")
    try:
        subprocess.run([sys.executable, "./flowgen/flowgen.py"], check=True)
    except subprocess.CalledProcessError:
        print("[ERROR] Falló la generación de flujos")
        sys.exit(1)

def run_model():
    print("[*] Ejecutando modelo de detección...")
    try:
        subprocess.run([sys.executable, "./model/predictor.py"], check=True)
    except subprocess.CalledProcessError:
        print("[ERROR] Falló la predicción del modelo")
        sys.exit(1)

if __name__ == "__main__":
    run_capture()
    run_flowgen()
    run_model()
    print("[*] Todos los procesos completados.")
