from netmiko import ConnectHandler

switch = {
    'device_type': 'cisco_ios',
    'host': '192.168.10.10',
    'username': 'spooky',
    'password': 'cisco',
    'secret': 'class',
}

puerto = "Gi1/0/48"  # 👈 usa el nombre exacto del puerto
vlan_id = 67

net_connect = ConnectHandler(**switch)
net_connect.enable()

# Comandos a enviar
commands = [
    f"interface {puerto}",
    "switchport mode access",
    f"switchport access vlan {vlan_id}",
    "no shutdown",
    "exit"
]

# Enviar comando por comando y mostrar resultado
for cmd in commands:
    print(f"\n➡️ Enviando: {cmd}")
    result = net_connect.send_config_set([cmd])
    print(result)

net_connect.disconnect()