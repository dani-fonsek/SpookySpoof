import pandas as pd

# Ruta a tu archivo
ruta_archivo = '/home/user/Desktop/SpookySpoof/Laboratorio/03-02-2018.csv'

# Cargar el CSV
df = pd.read_csv(ruta_archivo, low_memory=False)

# Reemplazar "benign" por "BENIGN" (ignora mayúsculas/minúsculas)
df['Label'] = df['Label'].replace(r'(?i)^benign$', 'BENIGN', regex=True)

# Guardar el archivo corregido (puedes sobrescribir o guardar nuevo)
df.to_csv(ruta_archivo, index=False)
