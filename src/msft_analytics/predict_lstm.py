import os
import pickle
import pandas as pd
import numpy as np
from msft_analytics.logger import get_logger

# Logger para inferencia LSTM
default_logger = get_logger("msft_inference")

# Ruta del modelo LSTM
RUTA_MODEL = os.path.join("src", "msft_analytics", "static", "models", "model.pkl")
# Ruta al CSV enriquecido
CSV_PATH   = os.path.join("src", "msft_analytics", "static", "data", "historical_enriched.csv")

def cargar_modelo_lstm(ruta_modelo=RUTA_MODEL, logger=default_logger):
    """Cargamos la tupla (model, scaler, ventana) del LSTM entrenado."""
    try:
        logger.info(f"Cargando LSTM Desde: {ruta_modelo}")
        with open(ruta_modelo, "rb") as f:
            model, scaler, ventana = pickle.load(f)
        logger.info(f"LSTM Cargado Correctamente (Ventana={ventana})")
        return model, scaler, ventana
    except Exception as e:
        logger.error(f"Error Cargando Modelo LSTM: {e}")
        raise

def cargar_datos(ruta_csv=CSV_PATH, logger=default_logger):
    """Leemos el CSV y devolvemos el DataFrame diario con columna 'cerrar'"""
    try:
        logger.info(f"Leyendo Datos Desde: {ruta_csv}")
        df = pd.read_csv(ruta_csv)
        df['fecha'] = pd.to_datetime(df.get("Fecha", df.get("fecha")))
        df.set_index('fecha', inplace=True)
        df = df.asfreq('D')
        df['cerrar'] = df['cerrar'].interpolate(method='time')
        logger.info("Datos Cargados Y Preprocesados Correctamente")
        return df
    except Exception as e:
        logger.error(f"Error leyendo o procesando CSV: {e}")
        raise

def predecir_lstm(model, scaler, ventana, df, pasos=7, logger=default_logger):
    """Generamos predicciones de los próximos `pasos` días sobre la columna 'cerrar'"""
    try:
        logger.info(f"Iniciando Predicción Para {pasos} Días")
        y = df['cerrar'].values.reshape(-1,1)
        y_scaled = scaler.transform(y)
        seq = y_scaled[-ventana:].reshape(1, ventana, 1)

        preds_scaled = []
        for _ in range(pasos):
            p = model.predict(seq)[0][0]
            preds_scaled.append(p)
            seq = np.append(seq[:,1:,:], [[[p]]], axis=1)

        preds = scaler.inverse_transform(np.array(preds_scaled).reshape(-1,1)).flatten()
        fechas = pd.date_range(
            start=df.index.max() + pd.Timedelta(days=1),
            periods=pasos, freq='D'
        )
        df_result = pd.DataFrame({'Fecha_Predicha': fechas, 'Prediccion_Cierre': preds})
        logger.info("Predicción Completada Correctamente")
        return df_result
    except Exception as e:
        logger.error(f"Error Durante La Predicción: {e}")
        return pd.DataFrame()

def run():
    model, scaler, ventana = cargar_modelo_lstm()
    df = cargar_datos()
    df_pred = predecir_lstm(model, scaler, ventana, df, pasos=7)
    print("\n📈 Predicción LSTM Próximos 7 Días (Precio De Cierre):")
    print(df_pred)

if __name__ == "__main__":
    run()
