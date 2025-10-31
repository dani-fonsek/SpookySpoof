#!/usr/bin/env python3
import os
import subprocess

# -----------------------------------
# Rutas absolutas
# -----------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PCAP_DIR = os.path.join(BASE_DIR, "../capture/pcaps")
CSV_DIR = os.path.join(BASE_DIR, "/home/user/Desktop/SpookySpoof/flowgen/Base")
CICFLOWMETER_JAR = os.path.join(BASE_DIR, "../CICFlowMeter_CLI/build/libs/CICFlowMeter-4.0.jar")
JNETPCAP_JAR = os.path.join(BASE_DIR, "../CICFlowMeter_CLI/jnetpcap/linux/jnetpcap-1.4.r1425/jnetpcap.jar")
JNETPCAP_LIB_DIR = os.path.join(BASE_DIR, "../CICFlowMeter_CLI/jnetpcap/linux/jnetpcap-1.4.r1425")

# Dependencias adicionales (SLF4J, Tika, Commons)
DEPENDENCIES = [
    "/home/user/.m2/repository/org/slf4j/slf4j-api/1.7.5/slf4j-api-1.7.5.jar",
    "/home/user/.m2/repository/org/slf4j/slf4j-simple/1.7.5/slf4j-simple-1.7.5.jar",
    "/home/user/.m2/repository/org/apache/tika/tika-core/1.17/tika-core-1.17.jar",
    "/home/user/.m2/repository/commons-io/commons-io/2.5/commons-io-2.5.jar",
    "/home/user/.m2/repository/org/apache/commons/commons-math3/3.6.1/commons-math3-3.6.1.jar"
]

# Crear carpeta de salida si no existe
os.makedirs(CSV_DIR, exist_ok=True)
os.makedirs(PCAP_DIR, exist_ok=True)

# -----------------------------------
# Función para generar flujos
# -----------------------------------
def generate_flows():
    pcap_files = [f for f in os.listdir(PCAP_DIR) if f.endswith(".pcap")]
    if not pcap_files:
        print("[INFO] No se encontraron archivos .pcap en", PCAP_DIR)
        return

    print(f"[*] Se encontraron {len(pcap_files)} archivos .pcap. Generando flujos...\n")

    for idx, pcap_file in enumerate(pcap_files, start=1):
        input_path = os.path.join(PCAP_DIR, pcap_file)
        output_path = os.path.join(CSV_DIR, pcap_file.replace(".pcap", ".csv"))

        # Armar classpath tal como funciona en bash
        classpath = ":".join([CICFLOWMETER_JAR, JNETPCAP_JAR] + DEPENDENCIES)

        cmd = [
            "java",
            f"-Djava.library.path={JNETPCAP_LIB_DIR}",
            "-cp",
            classpath,
            "cic.cs.unb.ca.ifm.Cmd",
            input_path,
            CSV_DIR
        ]

        print(f"[*] ({idx}/{len(pcap_files)}) Procesando {pcap_file}...")
        try:
            subprocess.run(cmd, check=True)
            print(f"[+] Flujo generado correctamente: {output_path}\n")
        except subprocess.CalledProcessError:
            print(f"[-] Error procesando {pcap_file}\n")

    print("[*] Todos los archivos .pcap han sido procesados.")

# -----------------------------------
# Ejecutar
# -----------------------------------
if __name__ == "__main__":
    generate_flows()
