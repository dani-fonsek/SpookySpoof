import os
import pandas as pd
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib
from glob import glob
from collections import defaultdict

carpeta_csv = '/home/user/Desktop/SpookySpoof/model/datasets'
modelo_path = 'EXPOT.pkl'
csv_files = sorted(glob(os.path.join(carpeta_csv, '*.csv')))

#Detectar todas las clases
todas_las_etiquetas = []
for archivo in csv_files:
    try:
        df_temp = pd.read_csv(archivo, low_memory=False)
        df_temp.columns = df_temp.columns.str.strip()
        if 'Label' in df_temp.columns:
            todas_las_etiquetas.extend(df_temp['Label'].dropna().unique())
    except Exception as e:
        print(f"Error leyendo etiquetas en {archivo}: {e}")
todas_las_etiquetas = list(set(todas_las_etiquetas))  #sin duplicados

#Cargar o crear modelo
if os.path.exists(modelo_path):
    print("Cargando modelo existente...")
    model, le = joblib.load(modelo_path)
    clases_posibles = np.arange(len(le.classes_))
    print(f"Clases conocidas: {list(le.classes_)}")
else:
    print("Entrenando modelo nuevo desde cero...")
    model = SGDClassifier(loss='log_loss', max_iter=1000, tol=1e-3, random_state=42)
    le = LabelEncoder()
    le.fit(todas_las_etiquetas)
    clases_posibles = np.arange(len(le.classes_))
    print(f"Clases detectadas para entrenamiento: {list(le.classes_)}")

#Mapa de etiquetas mal codificadas
mapa_labels = {
    'Web Attack � Brute Force': 'Web Attack Brute Force',
    'Web Attack � Sql Injection': 'Web Attack Sql Injection',
    'Web Attack � XSS': 'Web Attack XSS',
}

#Alias de nombres de columnas inconsistentes
alias_columnas = {
    'Avg Packet Size': 'Average Packet Size',
    'Bwd Byts/b Avg': 'Bwd Avg Bytes/Bulk',
    'Bwd Header Len': 'Bwd Header Length',
    'Bwd IAT Tot': 'Bwd IAT Total',
    'Fwd Seg Size Avg': 'Avg Fwd Segment Size',
    'Bwd Seg Size Avg': 'Avg Bwd Segment Size',
    'ACK Flag Cnt': 'ACK Flag Count',
    'Fwd Pkts/s': 'Fwd Packets/s',
    'Bwd Pkts/s': 'Bwd Packets/s'
}

#Variables para resumen global
y_true_global = []
y_pred_global = []
columnas_base = None  #Se fijará con el primer archivo válido

#Entrenamiento incremental
for idx, archivo in enumerate(csv_files, start=1):
    print(f"\n [{idx}/{len(csv_files)}] Procesando: {os.path.basename(archivo)}")

    try:
        df = pd.read_csv(archivo, low_memory=False)
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.dropna(inplace=True)
        df.columns = df.columns.str.strip()
        df.rename(columns=alias_columnas, inplace=True)
        df.drop(['Flow ID', 'Source IP', 'Destination IP', 'Timestamp'], axis=1, inplace=True, errors='ignore')

        if 'Label' not in df.columns:
            print(f"El archivo {archivo} no tiene columna 'Label'. Saltando...")
            continue
        
        df['Label'] = df['Label'].replace(mapa_labels)
        df['Label'] = df['Label'].replace({'Benign': 'BENIGN'})
        y = df['Label']
        X = df.drop('Label', axis=1)

        #Filtrar solo etiquetas conocidas
        validos = y.isin(le.classes_)
        y = y[validos]
        X = X.loc[validos]
        y_encoded = le.transform(y)

        #Filtrar columnas numéricas
        X = X.select_dtypes(include=[np.number])
        X = X.iloc[:len(y_encoded)]

        #Establecer columnas base para mantener consistencia
        if columnas_base is None:
            columnas_base = X.columns
        else:
            #Agregar columnas faltantes
            columnas_faltantes = set(columnas_base) - set(X.columns)
            for col in columnas_faltantes:
                X[col] = 0
            #Reordenar columnas
            X = X[columnas_base]

        #Entrenamiento
        X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
        model.partial_fit(X_train, y_train, classes=clases_posibles)

        y_pred = model.predict(X_test)
        y_true_global.extend(y_test)
        y_pred_global.extend(y_pred)

    except Exception as e:
        print(f"Error procesando {archivo}: {e}")

#Reporte global corregido
print("\n=== Reporte final global para todos los datos combinados ===")
if y_true_global and y_pred_global:
    import numpy as np

    #Determinar las clases presentes realmente en los datos
    clases_presentes = sorted(np.unique(np.concatenate([y_true_global, y_pred_global])))

    print(classification_report(
        y_true_global,
        y_pred_global,
        labels=clases_presentes,
        target_names=le.inverse_transform(clases_presentes),
        zero_division=0
    ))
else:
    print("No se generó un reporte global porque no se logró entrenar ningún archivo correctamente.")


joblib.dump((model, le), modelo_path)
print("\nEntrenamiento incremental completo. Modelo guardado como EXPOT.pkl")
