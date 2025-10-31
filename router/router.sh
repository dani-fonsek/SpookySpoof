#!/bin/bash
# router.sh
# Configura Debian como router + NAT + DHCP + interfaz promiscuo

# Interfaz LAN y WAN
LAN_IF="eno1"      # cambiar si tu LAN es otra
WAN_IF="wlp2s0"    # cambiar si tu WAN es otra

# Habilitar reenvío de paquetes
echo "Habilitando IP forwarding..."
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward

# Configurar NAT con iptables
echo "Aplicando reglas NAT y FORWARD..."
sudo iptables -t nat -F
sudo iptables -t nat -A POSTROUTING -o $WAN_IF -j MASQUERADE

sudo iptables -F FORWARD
sudo iptables -A FORWARD -i $LAN_IF -o $WAN_IF -j ACCEPT
sudo iptables -A FORWARD -i $WAN_IF -o $LAN_IF -m state --state RELATED,ESTABLISHED -j ACCEPT

# Poner LAN en modo promiscuo
echo "Activando modo promiscuo en $LAN_IF..."
sudo ip link set $LAN_IF promisc on

# Reiniciar DHCP para que tome efecto
echo "Reiniciando servidor DHCP..."
sudo systemctl restart isc-dhcp-server

echo "Configuración completa ✅"
echo "LAN: $LAN_IF, WAN: $WAN_IF"
sudo iptables -A FORWARD -i eno1.67 -d 192.168.10.0/24 -j DROP
sudo iptables -A FORWARD -i eno1.67 -o wlp2s0 -j DROP
sudo ip link add link eno1 name eno1.67 type vlan id 67
