import os
import sqlite3
import argparse
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from msft_analytics.logger import get_logger # Importamos nuestro logger personalizado

logger = get_logger() # Inicializamos el logger

# Directorio base del paquete (src/msft_analytics)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Directorio data dentro de static
DEFAULT_DATA_DIR = os.path.join(BASE_DIR, "static", "data")

class MSFTCollector:
    def __init__(self, db_path, csv_path):
        """
        Inicializamos la clase con la ruta de la base de datos y el archivo CSV.
        """
        self.db_path = db_path
        self.csv_path = csv_path
        self.table_name = "msft_data"

        # Aseguramos la existencia de los directorios
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)

    def fetch_data(self):
        """
        Descargamos los datos históricos desde Yahoo Finanzas,
        solicitando hasta mañana para garantizar el cierre de hoy.
        """
        logger.info("Descargando Datos Desde Yahoo Finanzas...")
        tomorrow = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")

        df = yf.download(
            "MSFT",
            start="1986-03-13",
            end=tomorrow,
            auto_adjust=False,
            progress=False
        )

        df = df.reset_index().rename(columns={
            "Date": "Fecha", "Open": "Abrir", "High": "Máx.",
            "Low": "Mín.", "Close": "Cerrar", "Volume": "Volumen"
        })[["Fecha", "Abrir", "Máx.", "Mín.", "Cerrar", "Volumen"]]
        
        df["Fecha"] = pd.to_datetime(df["Fecha"]).dt.date

        # Agregamos columnas año, mes, día
        df["año"] = df["Fecha"].apply(lambda x: x.year)
        df["mes"] = df["Fecha"].apply(lambda x: x.month)
        df["día"] = df["Fecha"].apply(lambda x: x.day)

        # Reorganizamos las columnas y renombramos a minúsculas
        df = df[["año", "mes", "día", "Abrir", "Máx.", "Mín.", "Cerrar", "Volumen"]]
        df.columns = ["año", "mes", "día", "abrir", "max", "min", "cerrar", "volumen"]

        return df

    def save_to_db(self, df):
        """
        Guardamos datos en SQLite, insertando solo nuevos registros.
        """
        logger.info("Guardando Datos En SQLite...")
        conn = sqlite3.connect(self.db_path)

        if self.table_exists(conn):
            df_existing = pd.read_sql(f"SELECT * FROM {self.table_name}", conn)
            # Validamos la existencia de columna año, mes y día
            if all(col in df_existing.columns for col in ["año", "mes", "día"]):
                # Renombramos temporalmente para usar pd.to_datetime por mapping
                cols_exist = df_existing[["año", "mes", "día"]].rename(
                    columns={"año": "year", "mes": "month", "día": "day"}
                )
                df_existing["Fecha"] = pd.to_datetime(cols_exist)

                cols_new = df[["año", "mes", "día"]].rename(
                    columns={"año": "year", "mes": "month", "día": "day"}
                )
                df["Fecha"] = pd.to_datetime(cols_new)
            else:
                logger.warning("Columnas de Fecha No Existen En La Tabla. Realizando Carga Completa.")
                df_existing = pd.DataFrame()
        else:
            df_existing = pd.DataFrame()

        if df_existing.empty:
            df.to_sql(self.table_name, conn, if_exists="replace", index=False)
            logger.info(f"Tabla {self.table_name} Creada Con {len(df)} Registros.")
        else:
            nuevos = df[~df["Fecha"].isin(df_existing["Fecha"])].copy()
            if not nuevos.empty:
                df_combined = pd.concat(
                    [df_existing.drop(columns="Fecha"), nuevos.drop(columns="Fecha")],
                    ignore_index=True
                )
                df_combined = df_combined.sort_values(["año", "mes", "día"])
                df_combined.to_sql(self.table_name, conn, if_exists="replace", index=False)
                logger.info(f"Insertados {len(nuevos)} Nuevos Registros. Total: {len(df_combined)}.")
            else:
                logger.info("No Hay Datos Nuevos Para Insertar.")

        conn.close()
        logger.info(f"Base De Datos SQLite Generada En: {os.path.abspath(self.db_path)}")

    def table_exists(self, conn):
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}'"
        )
        return cursor.fetchone() is not None

    def save_to_csv(self, df):
        """
        Guardamos los datos en CSV.
        """
        logger.info("Guardando Datos En CSV...")
        df.to_csv(self.csv_path, index=False, encoding="utf-8-sig", float_format="%.2f")
        logger.info(f"Archivo CSV Generado En: {os.path.abspath(self.csv_path)}")

    def run(self):
        """
        Flujo completo: descarga, guarda en DB y CSV.
        """
        df = self.fetch_data()
        self.save_to_db(df)

        # Leemos histórico completo para exportar a CSV
        conn = sqlite3.connect(self.db_path)
        df_all = pd.read_sql(f"SELECT * FROM {self.table_name}", conn)
        conn.close()

        self.save_to_csv(df_all)
        logger.info("Proceso Completado Con Éxito.")

def run():
    parser = argparse.ArgumentParser(
        description="Descarga MSFT y guarda en static/data"
    )
    parser.add_argument(
        "--db",
        default=os.getenv("MSFT_DB_PATH", os.path.join(DEFAULT_DATA_DIR, "historical.db")),
        help="Ruta al SQLite (default: static/data/historical.db)"
    )
    parser.add_argument(
        "--csv",
        default=os.getenv("MSFT_CSV_PATH", os.path.join(DEFAULT_DATA_DIR, "historical.csv")),
        help="Ruta al CSV (default: static/data/historical.csv)"
    )
    args = parser.parse_args()

    collector = MSFTCollector(db_path=args.db, csv_path=args.csv)
    collector.run()

if __name__ == "__main__":
    run()