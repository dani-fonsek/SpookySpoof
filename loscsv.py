import os
import pandas as pd

# Carpeta con los CSV originales del CIC-IDS-2018
input_folder = '/ruta/a/csv_originales_cic_ids_2018'
# Carpeta donde guardar CSV limpios
output_folder = '/ruta/a/csv_limpios_cic_ids_2018'

# Define un mapeo de columnas originales (variantes) a nombres estándar
column_mapping = {
    'Bwd Avg Bytes/Bulk': 'Bwd Byts/b Avg',
    'ACK Flag Count': 'ACK Flag Cnt',
    'Avg Packet Size': 'Pkt Len Avg',
    'Bwd Avg Packets/Bulk': 'Bwd Pkt/b Avg',
    'Bwd Header Length': 'Bwd Header Len',
    'Bwd IAT Total': 'Bwd IAT Tot',
    # Agrega todos los mappings necesarios para unificar nombres
}

# Mapa para etiquetas con caracteres raros o inconsistentes
label_mapping = {
    'Web Attack � Brute Force': 'Web Attack Brute Force',
    'Web Attack � Sql Injection': 'Web Attack Sql Injection',
    'Web Attack � XSS': 'Web Attack XSS',
    'Benign': 'BENIGN',
    'Infilteration': 'Infiltration',
    # Agrega más si encuentras más etiquetas problemáticas
}

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if not filename.endswith('.csv'):
        continue

    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)

    try:
        # Leer CSV, ignorar líneas duplicadas de encabezado
        df = pd.read_csv(input_path, low_memory=False, skip_blank_lines=True)

        # Si el encabezado se repite dentro del archivo, eliminar esas filas
        # Identifica filas que tienen como valor en la columna 'Label' el string 'Label'
        if 'Label' in df.columns:
            df = df[df['Label'] != 'Label']
        else:
            print(f"Advertencia: 'Label' no está en columnas de {filename}")

        # Renombrar columnas según mapeo
        df.rename(columns=column_mapping, inplace=True)

        # Unificar etiquetas en columna Label
        if 'Label' in df.columns:
            df['Label'] = df['Label'].replace(label_mapping)

        # Convertir columnas numéricas, ignorando columna Label
        for col in df.columns:
            if col != 'Label':
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Eliminar filas con datos faltantes o no numéricos
        df.dropna(inplace=True)

        # Guardar CSV limpio
        df.to_csv(output_path, index=False)
        print(f"Limpieza y unificación completada: {filename}")

    except Exception as e:
        print(f"Error procesando {filename}: {e}")
