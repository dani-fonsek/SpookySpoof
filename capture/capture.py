from scapy.all import sniff, wrpcap

# Parámetros
pcap_file = "capture.pcap"
packet_count = 100  # cantidad de paquetes a capturar (puedes ajustar)
timeout = 60        # segundos máximo para capturar

print(f"Capturando {packet_count} paquetes o durante {timeout} segundos...")

packets = sniff(count=packet_count, timeout=timeout)

print(f"Capturados {len(packets)} paquetes. Guardando en {pcap_file}...")

wrpcap(pcap_file, packets)

print("Captura finalizada.")
