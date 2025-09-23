from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

loaded = joblib.load("EXPOT.pkl")
print(f"Tipo cargado: {type(loaded)}")
if isinstance(loaded, tuple):
    model = loaded[0]  # Asumiendo que el modelo está en la posición 0
else:
    model = loaded

labels = {
    0: "BENIGN",
    1: "Bot",
    2: "DDoS",
    3: "DoS GoldenEye",
    4: "DoS Hulk",
    5: "DoS Slowhttptest",
    6: "DoS Slowloris",
    7: "FTP-Patator",
    8: "Heartbleed",
    9: "Infiltration",
    10: "PortScan",
    11: "SSH-Patator"
}

class InputData(BaseModel):
    features: list[float]

@app.post("/predict")
def predict(data: InputData):
    if len(data.features) != 77:
        raise HTTPException(status_code=400, detail="Se requieren exactamente 77 características.")

    try:
        input_array = np.array(data.features).reshape(1, -1)
        prediction_num = model.predict(input_array)[0]
        confidence = None
        if hasattr(model, "predict_proba"):
            confidence = max(model.predict_proba(input_array)[0])
        label = labels.get(prediction_num, "Unknown")

        return {
            "prediction_numeric": int(prediction_num),
            "prediction_label": label,
            "confidence": confidence,
            "message": f"La predicción es {label} con una confianza de {confidence:.2f}" if confidence else f"La predicción es {label}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la predicción: {str(e)}")
