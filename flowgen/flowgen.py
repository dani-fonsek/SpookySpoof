import subprocess
import os

#Rutas absolutas para que funcione y ubique todo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # carpeta flowgen
PCAP_DIR = os.path.join(BASE_DIR, "../capture/pcaps")
CSV_DIR = os.path.join(BASE_DIR, "flows")
LIB_PATH = "/home/user/Desktop/SpookySpoof/CICFlowMeter_CLI/jnetpcap/linux/jnetpcap-1.4.r1425"

#Todos los .jar (dependencias de CICFLowMeter) necesarios
CLASSPATH_JARS = [
    "/home/user/Desktop/SpookySpoof/CICFlowMeter_CLI/build/libs/CICFlowMeter-4.0.jar",
    "/home/user/Desktop/SpookySpoof/CICFlowMeter_CLI/jnetpcap/linux/jnetpcap-1.4.r1425/jnetpcap.jar",
    "/home/user/.m2/repository/org/slf4j/slf4j-api/1.7.5/slf4j-api-1.7.5.jar",
    "/home/user/.m2/repository/org/slf4j/slf4j-simple/1.7.5/slf4j-simple-1.7.5.jar",
    "/home/user/.m2/repository/org/apache/tika/tika-core/1.17/tika-core-1.17.jar",
    "/home/user/.m2/repository/commons-io/commons-io/2.5/commons-io-2.5.jar",
    "/home/user/.m2/repository/org/apache/commons/commons-math3/3.6.1/commons-math3-3.6.1.jar"
]

CLASSPATH = ":".join(CLASSPATH_JARS)

os.makedirs(CSV_DIR, exist_ok=True)
os.makedirs(PCAP_DIR, exist_ok=True)

# Función para generar flujos
def generate_flows():
    pcap_files = [f for f in os.listdir(PCAP_DIR) if f.endswith(".pcap")]
    total_files = len(pcap_files)

    if not pcap_files:
        print("[*] No se encontraron archivos .pcap en", PCAP_DIR)
        return

    print(f"[*] Se encontraron {total_files} archivos .pcap. Iniciando procesamiento...\n")

    for idx, pcap_file in enumerate(pcap_files, start=1):
        input_path = os.path.join(PCAP_DIR, pcap_file)
        output_path = os.path.join(CSV_DIR, pcap_file.replace(".pcap", ".csv"))

        cmd = [
            "java",
            f"-Djava.library.path={LIB_PATH}",
            "-cp",
            CLASSPATH,
            "cic.cs.unb.ca.ifm.Cmd",
            input_path,
            CSV_DIR
        ]

        print(f"[*] ({idx}/{total_files}) Procesando {pcap_file}...")

        try:
            # Redirigir stdout y stderr para que no se vean los logs de CICFlowMeter
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            print(f"[+] Flujo generado correctamente: {output_path}\n")
        except subprocess.CalledProcessError:
            print(f"[-] Error al procesar {pcap_file}\n")

    print("[*] Todos los archivos .pcap han sido procesados.")
    print("[*] Generación de flujos completada.")

#Ejecutar el programa
if __name__ == "__main__":
    print("[*] Ejecutando generación de flujos usando CICFlowMeter...")
    generate_flows()
