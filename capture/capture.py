from scapy.all import sniff, wrpcap
from datetime import datetime
import os

#Carpeta donde guardar los .pcap
pcap_dir = "pcaps"
os.makedirs(pcap_dir, exist_ok=True)

#Nombre del archivo con fecha/hora
pcap_file = os.path.join(pcap_dir, f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pcap")

#Interfaz de red (LAN cableada)
interface = "wlp2s0"
print(f"[INFO] Capturando en interfaz: {interface}")

#Captura paquetes como prueba
packets = sniff(iface=interface, count=300)

# uardar en archivo pcap
wrpcap(pcap_file, packets)

print(f"[INFO] Guardando en: {pcap_file}")
print("[INFO] Captura completada.")
