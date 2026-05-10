import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime
import sys


def setup_logging(app):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # questo è app/ se setup_logging è in app/logging_config.py
    log_dir = os.path.join(base_dir, 'logs')
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"{datetime.now().strftime('%d-%m-%Y')}.log")

    # Handler per il file
    file_handler = TimedRotatingFileHandler(
        log_file, when="midnight", interval=1, backupCount=7, encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s [in %(pathname)s:%(lineno)d]'
    )
    file_handler.setFormatter(file_formatter)

    # Handler per la console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(levelname)s - %(name)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)

    # Prendi il logger di flask app
    logger = app.logger
    logger.setLevel(logging.INFO)

    # Rimuovi tutti gli handler esistenti per evitare duplicati
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Aggiungi i due handler
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Assicura propagazione (utile se hai altri logger)
    logger.propagate = True

    logger.info("Logging configurato correttamente.")
