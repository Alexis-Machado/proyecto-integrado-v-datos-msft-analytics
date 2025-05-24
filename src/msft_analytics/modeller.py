import os
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
from msft_analytics.logger import get_logger

class Modeller:
    def __init__(self):
        self.logger = get_logger("msft_model")
        self.model_path = os.path.join(os.path.dirname(__file__), "static", "models")
        self.model_file = os.path.join(self.model_path, "model.pkl")

        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)
            self.logger.info("Directorio De Modelos Creado.")

    def preparar_datos(self, df: pd.DataFrame):
        df = df.copy()
        df['fecha'] = pd.to_datetime(df['fecha'])
        df.set_index('fecha', inplace=True)
        df = df.asfreq('D')
        df['cerrar'] = df['cerrar'].interpolate(method='time')
        return df

    def crear_secuencias(self, datos, ventana):
        X, y = [], []
        for i in range(len(datos) - ventana):
            X.append(datos[i:i + ventana])
            y.append(datos[i + ventana])
        return np.array(X), np.array(y)

    def entrenar(self, df: pd.DataFrame, pasos: int = 7, ventana=30):
        try:
            self.logger.info("Iniciando Entrenamiento Del Modelo LSTM...")
            df = self.preparar_datos(df)
            y = df['cerrar'].values.reshape(-1, 1)

            scaler = MinMaxScaler()
            y_scaled = scaler.fit_transform(y)

            X, y_seq = self.crear_secuencias(y_scaled, ventana)
            X = X.reshape((X.shape[0], X.shape[1], 1))

            train_size = int(len(X) * 0.85)
            X_train, X_test = X[:train_size], X[train_size:]
            y_train, y_test = y_seq[:train_size], y_seq[train_size:]

            model = Sequential([
                LSTM(50, activation='relu', input_shape=(ventana, 1)),
                Dense(1)
            ])
            model.compile(optimizer='adam', loss='mse')
            model.fit(
                X_train, y_train,
                epochs=50, batch_size=16,
                validation_split=0.1,
                callbacks=[EarlyStopping(patience=5)],
                verbose=0
            )

            # Guardamos el modelo, scaler y ventana
            with open(self.model_file, "wb") as f:
                pickle.dump((model, scaler, ventana), f)

            y_pred = model.predict(X_test)
            y_test_inv = scaler.inverse_transform(y_test.reshape(-1, 1))
            y_pred_inv = scaler.inverse_transform(y_pred)

            rmse = np.sqrt(mean_squared_error(y_test_inv, y_pred_inv))
            mae = mean_absolute_error(y_test_inv, y_pred_inv)
            mape = np.mean(np.abs((y_test_inv - y_pred_inv) / y_test_inv)) * 100
            r2 = r2_score(y_test_inv, y_pred_inv)

            self.logger.info(f"RMSE: {rmse:.4f}")
            self.logger.info(f"MAE: {mae:.4f}")
            self.logger.info(f"MAPE: {mape:.2f}%")
            self.logger.info(f"R²: {r2:.4f}")

            return {
                'rmse': rmse,
                'mae': mae,
                'mape': mape,
                'r2': r2,
                'r2_mayor_85': r2 > 0.85
            }

        except Exception as e:
            self.logger.error(f"Error Al Entrenar El Modelo: {e}")
            return None

    def predecir(self, df: pd.DataFrame, pasos: int = 7):
        try:
            self.logger.info(f"Realizando Predicción A {pasos} Días...")
            df = self.preparar_datos(df)
            y = df['cerrar'].values.reshape(-1, 1)

            with open(self.model_file, "rb") as f:
                model, scaler, ventana = pickle.load(f)

            y_scaled = scaler.transform(y)
            seq = y_scaled[-ventana:].reshape(1, ventana, 1)

            preds_scaled = []
            for _ in range(pasos):
                p = model.predict(seq)[0][0]
                preds_scaled.append(p)
                seq = np.append(seq[:, 1:, :], [[[p]]], axis=1)

            preds = scaler.inverse_transform(np.array(preds_scaled).reshape(-1, 1)).flatten()
            fechas = pd.date_range(
                start=df.index.max() + pd.Timedelta(days=1),
                periods=pasos, freq='D'
            )
            return pd.DataFrame({'Fecha_Predicha': fechas, 'prediccion': preds})

        except Exception as e:
            self.logger.error(f"Error En Predicción: {e}")
            return pd.DataFrame()

def run():
    print("🔄 Cargando Datos Enriquecidos...")
    enriched_csv = os.path.join(
        os.path.dirname(__file__),
        "static", "data", "historical_enriched.csv"
    )
    df = pd.read_csv(enriched_csv)

    if "Fecha" in df.columns:
        df.rename(columns={"Fecha": "fecha"}, inplace=True)

    model = Modeller()
    metrics = model.entrenar(df, pasos=7)

    if metrics is not None:
        print("✅ Modelo entrenado.")
        print(f"RMSE: {metrics['rmse']:.4f}")
        print(f"MAE: {metrics['mae']:.4f}")
        print(f"MAPE: {metrics['mape']:.2f}%")
        print(f"R²: {metrics['r2']:.4f}")
        print(f"¿R² > 0.85?: {'Sí' if metrics['r2_mayor_85'] else 'No'}")
    else:
        print("❌ Error Durante El Entrenamiento.")

    pred = model.predecir(df, pasos=7)
    print("\n📈 Predicción Para Próximos 7 Días (Precio De Cierre):")
    print(pred)

if __name__ == "__main__":
    run()
