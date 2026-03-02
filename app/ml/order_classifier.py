from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from app.utils.logger import get_logger

logger = get_logger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "orders_ml.csv"
MODEL_PATH = BASE_DIR / "models" / "order_classifier.joblib"
SCALER_PATH = BASE_DIR / "models" / "scaler.joblib"

FEATURES = ["total", "num_items", "precio_promedio"]
TARGET = "es_cara"


def cargar_y_limpiar_datos() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    logger.info("Datos cargados: %d filas, %d columnas", len(df), len(df.columns))

    # Limpiar
    df = df.dropna()
    df = df[df["total"] > 0]
    df = df[df["num_items"] > 0]
    df = df[df["precio_promedio"] > 0]

    logger.info("Datos limpios: %d filas", len(df))
    return df


def entrenar_modelo() -> None:
    Path(BASE_DIR / "models").mkdir(exist_ok=True)

    df = cargar_y_limpiar_datos()

    X = df[FEATURES].values
    y = df[TARGET].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    logger.info("Accuracy: %.2f", accuracy)
    logger.info("Reporte:\n%s", classification_report(y_test, y_pred, zero_division=0))

    joblib.dump(modelo, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    logger.info("Modelo guardado en %s", MODEL_PATH)


def predecir(total: float, num_items: int, precio_promedio: float) -> dict:
    modelo = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    X = np.array([[total, num_items, precio_promedio]])
    X_scaled = scaler.transform(X)

    prediccion = modelo.predict(X_scaled)[0]
    probabilidad = modelo.predict_proba(X_scaled)[0]

    resultado = {
        "es_cara": bool(prediccion),
        "probabilidad_cara": round(float(probabilidad[1]), 4),
        "probabilidad_barata": round(float(probabilidad[0]), 4),
    }
    logger.debug("Prediccion: %s", resultado)
    return resultado
