import os
import numpy as np
import pandas as pd
from msft_analytics.logger import get_logger

# Directorio base
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CARPETA_DATOS = os.path.join(BASE_DIR, "static", "data")
CSV_ORIGINAL_DEF = os.getenv(
    "MSFT_CSV_PATH",
    os.path.join(CARPETA_DATOS, "historical.csv")
)
CSV_ENRIQUECIDO_DEF = os.getenv(
    "MSFT_ENRICHED_CSV",
    os.path.join(CARPETA_DATOS, "historical_enriched.csv")
)

class Enricher:
    def __init__(
        self,
        ruta_csv_original: str = None,
        ruta_csv_enriquecido: str = None
    ):
        """
        ruta_csv_original: Ruta al CSV original con columnas año, mes, día, abrir, max, min, cerrar, volumen
        ruta_csv_enriquecido: Ruta al CSV donde se guardarán los datos enriquecidos
        """
        self.logger = get_logger("msft_enricher")
        self.ruta_csv_original = ruta_csv_original or CSV_ORIGINAL_DEF
        self.ruta_csv_enriquecido = ruta_csv_enriquecido or CSV_ENRIQUECIDO_DEF
        os.makedirs(os.path.dirname(self.ruta_csv_enriquecido), exist_ok=True)

    def calcular_kpi(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        # Reconstruimos la columna Fecha a partir de año, mes y día
        df['Fecha'] = pd.to_datetime(
            dict(year=df['año'], month=df['mes'], day=df['día'])
        )
        df = df.sort_values('Fecha').reset_index(drop=True)

        # KPIs
        df['tasa_variacion'] = df['cerrar'].pct_change().fillna(0) * 100
        df['media_movil_7d'] = df['cerrar'].rolling(window=7, min_periods=1).mean()
        df['volatilidad_7d'] = df['tasa_variacion'].rolling(window=7, min_periods=1).std()
        primera_cierre = df.loc[0, 'cerrar']
        df['retorno_acumulado'] = (df['cerrar'] / primera_cierre) - 1
        df['desviacion_estandar_acumulada'] = df['cerrar'].expanding(min_periods=1).std().fillna(0)
        
        # columnas de enriquecimiento
        df['rango_diario'] = df['max'] - df['min']
        df['rango_pct_diario'] = (df['rango_diario'] / df['cerrar']) * 100
        df['dia_semana'] = df['Fecha'].dt.weekday
        df['momentum_7d'] = df['cerrar'] - df['cerrar'].shift(7)
        df['momentum_7d'].fillna(0, inplace=True)
        tr1 = df['max'] - df['min']
        tr2 = (df['max'] - df['cerrar'].shift(1)).abs()
        tr3 = (df['min'] - df['cerrar'].shift(1)).abs()
        df['true_range'] = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        df['atr_14d'] = df['true_range'].rolling(window=14, min_periods=1).mean()
        df.drop(columns=['true_range'], inplace=True)

        self.logger.info("Enricher: KPIs Calculados Correctamente")
        return df

    def run(self):
        """Ejecutamos el proceso de enriquecimiento y guardamos el CSV"""
        try:
            self.logger.info(f"Enricher: Leyendo {self.ruta_csv_original}")
            df = pd.read_csv(self.ruta_csv_original)
        except Exception as e:
            self.logger.error(f"Enricher: error al leer CSV original -> {e}")
            return

        df_enriquecido = self.calcular_kpi(df)

        try:
            df_enriquecido.to_csv(
                self.ruta_csv_enriquecido,
                index=False,
                encoding="utf-8-sig"
            )
            self.logger.info(
                f"Enricher: CSV Enriquecido Guardado En {self.ruta_csv_enriquecido}"
            )
        except Exception as e:
            self.logger.error(
                f"Enricher: error al guardar CSV enriquecido -> {e}"
            )

def run():
    enricher = Enricher()
    enricher.run()

if __name__ == "__main__":
    run()
