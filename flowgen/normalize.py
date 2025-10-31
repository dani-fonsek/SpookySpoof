import pandas as pd
import os

CSV_DIR = "/home/user/Desktop/SpookySpoof/flowgen/Base"
BASE_CSV = "/home/user/Desktop/SpookySpoof/model/datasets/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"
OUTPUT_DIR = "/home/user/Desktop/SpookySpoof/flowgen/Processed"

def normalize_csv_dynamic(input_file, output_file, base_csv=BASE_CSV):
    if not os.path.exists(input_file):
        print(f"No se encontró el archivo: {input_file}")
        return

    # Leer CSV base para obtener las columnas de referencia
    df_base = pd.read_csv(base_csv, nrows=0)
    base_columns = list(df_base.columns)

    # Leer CSV a normalizar
    df = pd.read_csv(input_file)
    df.columns = df.columns.str.strip()  # limpiar espacios

    # --- Solo para Fwd Header Length: reemplazar si existe .1 ---
    if 'Fwd Header Length.1' in df.columns:
        df['Fwd Header Length'] = df['Fwd Header Length.1']
        df.drop(columns=['Fwd Header Length.1'], inplace=True)

    # Rellenar columnas faltantes con 0
    for col in base_columns:
        if col not in df.columns:
            df[col] = 0

    # Reordenar columnas según CSV base
    df = df[base_columns]

    # Guardar CSV limpio
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"✅ CSV normalizado guardado en: {output_file}")

def process_all_flows(csv_dir=CSV_DIR, output_dir=OUTPUT_DIR):
    csv_files = [f for f in os.listdir(csv_dir) if f.endswith(".csv")]
    if not csv_files:
        print("[*] No se encontraron CSVs en la carpeta:", csv_dir)
        return

    for csv_file in csv_files:
        input_path = os.path.join(csv_dir, csv_file)
        output_path = os.path.join(output_dir, csv_file.replace(".csv", "_clean.csv"))
        normalize_csv_dynamic(input_path, output_path)

if __name__ == "__main__":
    process_all_flows()
