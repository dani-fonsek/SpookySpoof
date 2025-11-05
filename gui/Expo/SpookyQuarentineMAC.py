from netmiko import ConnectHandler

# 🔧 Datos de conexión
switch = {
    'device_type': 'cisco_ios',
    'host': '192.168.10.10',
    'username': 'spooky',
    'password': 'cisco',
    'secret': 'class',
}

mac_objetivo = "4c20.b8df.74d9"
vlan_id = 67


net_connect = ConnectHandler(**switch)
net_connect.enable()

print(f"\n🔎 Buscando MAC {mac_objetivo} en el switch...")
tabla_mac = net_connect.send_command("show mac address-table")

mac_normalizada = mac_objetivo.lower().replace("-", ".").replace(":", ".")
lineas = tabla_mac.splitlines()
puerto = None

for linea in lineas:
    if mac_normalizada in linea:
        partes = linea.split()
        if len(partes) >= 4:
            puerto = partes[-1]
            break

if puerto:
    print(f"✅ MAC encontrada en el puerto: {puerto}")

    comandos = [
        f"interface {puerto}",
        "switchport mode access",
        f"switchport access vlan {vlan_id}",
        "no shutdown",
        "exit"
    ]

    resultado = net_connect.send_config_set(comandos)
    print("📋 Resultado de configuración:")
    print(resultado)

    if "% Invalid input" in resultado or "^" in resultado:
        print("Se detectó un error en la configuración.")
    else:
        print("Configuración aplicada correctamente.")

else:
    print("No se encontró la MAC en la tabla del switch.")

net_connect.disconnect()
print("\nConexión cerrada. :)")