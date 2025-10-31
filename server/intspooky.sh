#!/bin/bash
# Crear interfaz macvlan para el honeypot
ip link add intspooky link eth0 type macvlan mode bridge
ip addr add 192.168.10.12/24 dev intspooky
ip link set intspooky up

