import logging
import os

def get_logger(nombre: str = "msft_logger") -> logging.Logger:
    """
    Devolvemos un logger que escribe en consola y en un archivo de log.
    - Collector / flujo general: llama a get_logger() o get_logger('msft_analytics')
      y se escribe en src/msft_analytics/static/logs/msft_analytics.log
    - Enricher: llama a get_logger('msft_enricher')
      y se escribe en src/msft_analytics/static/logs/msft_enricher.log
    - Modeller: llama a get_logger('msft_model')
      y se escribe en src/msft_analytics/static/logs/msft_model.log
    - Inference: llama a get_logger('msft_inference')
      y se escribe en src/msft_analytics/static/logs/msft_inference.log

    Cada mensaje incluye fecha, hora, nivel y mensaje.
    """
    logger = logging.getLogger(nombre)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # 1) Formato de los mensajes
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # 2) Handler de consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # 3) Handler de archivo
        base_dir = os.path.abspath(os.path.dirname(__file__))
        log_dir = os.path.join(base_dir, "static", "logs")
        os.makedirs(log_dir, exist_ok=True)

        # Definimos el nombre del archivo según el logger
        if nombre == "msft_enricher":
            filename = "msft_enricher.log"
        elif nombre == "msft_model":
            filename = "msft_model.log"
        elif nombre == "msft_inference":
            filename = "msft_inference.log"
        else:
            filename = "msft_analytics.log"

        log_path = os.path.join(log_dir, filename)
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
