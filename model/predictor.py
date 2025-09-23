import joblib
import numpy as np
import os
import pandas as pd

# Ruta del modelo (siempre relativo a este archivo)
model_path = os.path.join(os.path.dirname(__file__), "EXPOT.pkl")

# Cargar el modelo
model_loaded = joblib.load(model_path)

# Si cargó una tupla, usa solo el primer elemento
model = model_loaded[0] if isinstance(model_loaded, tuple) else model_loaded

# Crear un ejemplo de input con las 77 features
# Ajustar los nombres a los que espera el modelo si es necesario
feature_names = model.feature_names_in_ if hasattr(model, "feature_names_in_") else [f"f{i}" for i in range(77)]
input_example = pd.DataFrame(np.random.rand(1, 77), columns=feature_names)

# Predicción
prediction = model.predict(input_example)

print("Predicción:", prediction)
