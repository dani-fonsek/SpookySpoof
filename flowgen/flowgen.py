#!/usr/bin/env python3
import os
import subprocess
import pickle
import pandas as pd

# -----------------------------------
# Rutas absolutas
# -----------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # carpeta flowgen
PCAP_DIR = os.path.join(BASE_DIR, "../capture/pcaps")
CSV_DIR = os.path.join(BASE_DIR, "flows")
JAR_PATH = os.path.join(BASE_DIR, "../CICFlowMeter_CLI/build/libs/CICFlowMeter-4.0.jar")
MODEL_PATH = os.path.join("/home/user/Desktop/SpookySpoof/model/EXPOT.pkl")  # tu modelo entrenado

os.makedirs(CSV_DIR, exist_ok=True)
os.makedirs(PCAP_DIR, exist_ok=True)

# -----------------------------------
# Función de generación de flujos
# -----------------------------------
def generate_flows():
    pcap_files = [f for f in os.listdir(PCAP_DIR) if f.endswith(".pcap")]
    if not pcap_files:
        print("[INFO] No se encontraron archivos .pcap en", PCAP_DIR)
        return []

    csv_files = []

    print(f"[*] Se encontraron {len(pcap_files)} archivos .pcap. Iniciando procesamiento...\n")
    for idx, pcap_file in enumerate(pcap_files, start=1):
        input_path = os.path.join(PCAP_DIR, pcap_file)
        output_path = os.path.join(CSV_DIR, pcap_file.replace(".pcap", ".csv"))
        csv_files.append(output_path)

        cmd = [
            "java",
            "-Djava.library.path=/home/user/Desktop/SpookySpoof/CICFlowMeter_CLI/jnetpcap/linux/jnetpcap-1.4.r1425",
            "-cp",
            ":".join([
                JAR_PATH,
                "/home/user/Desktop/SpookySpoof/CICFlowMeter_CLI/jnetpcap/linux/jnetpcap-1.4.r1425/jnetpcap.jar",
                "/home/user/.m2/repository/org/slf4j/slf4j-api/1.7.5/slf4j-api-1.7.5.jar",
                "/home/user/.m2/repository/org/slf4j/slf4j-simple/1.7.5/slf4j-simple-1.7.5.jar",
                "/home/user/.m2/repository/org/apache/tika/tika-core/1.17/tika-core-1.17.jar",
                "/home/user/.m2/repository/commons-io/commons-io/2.5/commons-io-2.5.jar",
                "/home/user/.m2/repository/org/apache/commons/commons-math3/3.6.1/commons-math3-3.6.1.jar"
            ]),
            "cic.cs.unb.ca.ifm.Cmd",
            input_path,
            os.path.join(CSV_DIR)
        ]

        print(f"[*] ({idx}/{len(pcap_files)}) Procesando {pcap_file}...")
        subprocess.run(cmd, check=True)
        print(f"[+] Flujo generado correctamente: {output_path}\n")

    return csv_files

# -----------------------------------
# Función de clasificación con .pkl
# -----------------------------------
def classify_flows(csv_files):
    if not os.path.exists(MODEL_PATH):
        print("[!] Modelo .pkl no encontrado en", MODEL_PATH)
        return

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    for csv_file in csv_files:
        df = pd.read_csv(csv_file)

        if df.empty:
            print(f"[!] CSV vacío: {csv_file}")
            continue

        # Predicción
        df["Label"] = model.predict(df)

        # Guardar CSV con label
        labeled_csv = csv_file.replace(".csv", "_labeled.csv")
        df.to_csv(labeled_csv, index=False)
        print(f"[+] CSV clasificado guardado: {labeled_csv}")

# -----------------------------------
# Ejecutar
# -----------------------------------
if __name__ == "__main__":
    print("[*] Ejecutando generación de flujos usando CICFlowMeter...\n")
    csv_files = generate_flows()
    if csv_files:
        print("[*] Todos los archivos .pcap han sido procesados.\n")
        print("[*] Ejecutando clasificación con modelo .pkl...\n")
        classify_flows(csv_files)
        print("\n[*] Generación y clasificación de flujos completada.")
