from netmiko import ConnectHandler

# 🔧 Datos de conexión
switch = {
    'device_type': 'cisco_ios',
    'host': '192.168.10.10',
    'username': 'spooky',     # Usuario SSH
    'password': 'cisco',      # Contraseña SSH
    'secret': 'class',        # Contraseña para modo enable
}

# 🎯 Comandos agrupados correctamente
commands = [
    "interface Gi1/0/48",
    "switchport mode access",
    "switchport access vlan 67",
    "no shutdown",
    "exit"
]

# 🔌 Conexión
net_connect = ConnectHandler(**switch)
net_connect.enable()

# 🛠️ Enviar todos los comandos como bloque
print("\n🚀 Enviando configuración completa...")
resultado = net_connect.send_config_set(commands)
print(resultado)

# 🔍 Verificar errores
if "% Invalid input" in resultado or "^" in resultado:
    print("❌ Se detectó un error en la configuración.")
else:
    print("✅ Configuración aplicada correctamente.")

# 🔚 Cerrar sesión
net_connect.disconnect()
print("\n🔚 Conexión cerrada.")