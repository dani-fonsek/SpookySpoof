#!/usr/bin/env python3
import subprocess
import sys
import os

# -----------------------------------
# Rutas absolutas a scripts
# -----------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAPTURE_DIR = os.path.join(BASE_DIR, "capture")
FLOWGEN_DIR = os.path.join(BASE_DIR, "flowgen")
MODEL_DIR = os.path.join(BASE_DIR, "model")

CAPTURE_SCRIPT = os.path.join(CAPTURE_DIR, "capture.py")
FLOWGEN_SCRIPT = os.path.join(FLOWGEN_DIR, "flowgen.py")
MODEL_SCRIPT = os.path.join(MODEL_DIR, "predictor.py")

# -----------------------------------
# Funciones para ejecutar cada paso
# -----------------------------------
def run_capture():
    print("[*] Ejecutando captura de paquetes...")
    try:
        subprocess.run(
            ["sudo", "-E", sys.executable, "capture.py"],
            cwd=CAPTURE_DIR,
            check=True
        )
        print("[INFO] Captura completada.")
    except subprocess.CalledProcessError:
        print("[ERROR] Falló la captura de paquetes")
        sys.exit(1)

def run_flowgen():
    print("[*] Ejecutando generación de flujos...")
    try:
        subprocess.run(
            [sys.executable, "flowgen.py"],
            cwd=FLOWGEN_DIR,
            check=True
        )
        print("[INFO] Generación de flujos completada.")
    except subprocess.CalledProcessError:
        print("[ERROR] Falló la generación de flujos")
        sys.exit(1)

def run_model():
    print("[*] Ejecutando modelo de detección...")
    try:
        subprocess.run(
            [sys.executable, "predictor.py"],
            cwd=MODEL_DIR,
            check=True
        )
        print("[INFO] Predicción completada.")
    except subprocess.CalledProcessError:
        print("[ERROR] Falló la predicción del modelo")
        sys.exit(1)

# -----------------------------------
# Ejecución principal
# -----------------------------------
if __name__ == "__main__":
    run_capture()
    run_flowgen()
    run_model()
    print("[*] Todos los procesos completados.")
