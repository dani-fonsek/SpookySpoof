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

carpeta_csv = '/home/user/Downloads/laboratorio'
modelo_path = 'EXPOT.pkl'

csv_files = sorted(glob(os.path.join(carpeta_csv, '*.csv')))

#Detectar todas las clases
todas_las_etiquetas = []
for archivo in csv_files:
    try:
        df_temp = pd.read_csv(archivo, usecols=['Label'], low_memory=False)
        df_temp.columns = df_temp.columns.str.strip()
        if 'Label' in df_temp.columns:
            todas_las_etiquetas.extend(df_temp['Label'].dropna().unique())
    except Exception as e:
        print(f"Error leyendo etiquetas en {archivo}: {e}")
todas_las_etiquetas = list(set(todas_las_etiquetas))  # sin duplicados

#Cargar o crear modelo
if os.path.exists(modelo_path):
    print("Cargando modelo existente...")
    model, le = joblib.load(modelo_path)
    if hasattr(le, 'classes_'):
        clases_posibles = np.arange(len(le.classes_))
        print(f"Clases conocidas: {list(le.classes_)}")
    else:
        print("El LabelEncoder cargado no tiene clases. ¿Estás seguro de que fue entrenado?")
        clases_posibles = None
else:
    print("Entrenando modelo nuevo desde cero...")
    model = SGDClassifier(loss='log_loss', max_iter=1000, tol=1e-3, random_state=42)
    le = LabelEncoder()
    le.fit(todas_las_etiquetas)
    clases_posibles = np.arange(len(le.classes_))
    print(f"Clases detectadas para entrenamiento: {list(le.classes_)}")

#Diccionario para acumular resultados
metrics_acumuladas = defaultdict(lambda: {'precision': [], 'recall': [], 'f1-score': [], 'support': 0})

#Datos para resumen global
y_true_global = []
y_pred_global = []

#Entrenamiento incremental
for idx, archivo in enumerate(csv_files, start=1):
    print(f"\n [{idx}/{len(csv_files)}] Procesando: {os.path.basename(archivo)}")

    try:
        df = pd.read_csv(archivo, low_memory=False)
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.dropna(inplace=True)
        df.drop(['Flow ID', 'Source IP', 'Destination IP', 'Timestamp'], axis=1, inplace=True, errors='ignore')
        df.columns = df.columns.str.strip()

        if 'Label' not in df.columns:
            print(f"El archivo {archivo} no tiene columna 'Label'. Saltando...")
            continue

        #Unificar etiquetas con caracteres raros si existen
        mapa_labels = {
            'Web Attack � Brute Force': 'Web Attack Brute Force',
            'Web Attack � Sql Injection': 'Web Attack Sql Injection',
            'Web Attack � XSS': 'Web Attack XSS',
        }
        df['Label'] = df['Label'].replace(mapa_labels)

        X = df.drop('Label', axis=1)
        y = df['Label']

        #Asegurar que solo entrenamos con etiquetas conocidas
        y = y[y.isin(le.classes_)]
        y_encoded = le.transform(y)
        X = X.iloc[:len(y_encoded)]

        X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

        model.partial_fit(X_train, y_train, classes=clases_posibles)

        y_pred = model.predict(X_test)

        #Acumular resultados globales para reporte al final
        y_true_global.extend(y_test)
        y_pred_global.extend(y_pred)

    except Exception as e:
        print(f"Error procesando {archivo}: {e}")

#Reporte global al final
print("\n=== Reporte final global para todos los datos combinados ===")
print(classification_report(y_true_global, y_pred_global, target_names=le.classes_, zero_division=0))

joblib.dump((model, le), modelo_path)
print("\nEntrenamiento incremental completo. Modelo guardado como EXPOT.pkl")
