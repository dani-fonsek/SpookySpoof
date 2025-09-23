import subprocess
import os

# Ruta a CICFlowMeter.jar
CICFLOWMETER_JAR = "/home/user/Downloads/CICFlowMeter-4.0.jar"

# Carpeta donde está el .pcap
PCAP_INPUT = "../capture/capture.pcap"

# Carpeta de salida para los CSV
CSV_OUTPUT = "./flows"

# Crear carpeta de salida si no existe
os.makedirs(CSV_OUTPUT, exist_ok=True)

def generate_flows(pcap_file, output_folder):
    """
    Ejecuta CICFlowMeter para generar flujos a partir de un .pcap
    """
    try:
        cmd = [
            "java", "-jar", CICFLOWMETER_JAR,
            "-f", pcap_file,
            "-o", output_folder
        ]
        subprocess.run(cmd, check=True)
        print(f"[+] Flujos generados en {output_folder}")
    except subprocess.CalledProcessError as e:
        print("[-] Error al ejecutar CICFlowMeter:", e)

if __name__ == "__main__":
    generate_flows(PCAP_INPUT, CSV_OUTPUT)
