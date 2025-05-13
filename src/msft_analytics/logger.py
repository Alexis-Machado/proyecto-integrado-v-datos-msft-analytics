import logging
import os

def get_logger(nombre: str = "msft_logger") -> logging.Logger:
    """
    Devolvemos un logger que escribe en consola y en el archivo msft_analytics.log.
    Incluye fecha, hora, nivel y mensaje.
    """
    logger = logging.getLogger(nombre)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Formato del mensaje
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Ruta para el archivo de log
        log_dir = os.path.join(os.path.dirname(__file__), "static", "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, "msft_analytics.log")

        # Handler para archivo
        file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger