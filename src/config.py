"""
config.py — Leitura das variáveis de ambiente e parâmetros do pipeline.
"""

import os
from dotenv import load_dotenv

load_dotenv()

RAW_DATA_PATH = os.getenv("RAW_DATA_PATH", "data/raw/transactions.csv")
STAGING_DATA_PATH = os.getenv("STAGING_DATA_PATH", "data/staging/")
PROCESSED_DATA_PATH = os.getenv("PROCESSED_DATA_PATH", "data/processed/")

VALOR_MINIMO_VALIDO = float(os.getenv("VALOR_MINIMO_VALIDO", 0.0))
LIMITE_OUTLIER_DESVIO = float(os.getenv("LIMITE_OUTLIER_DESVIO", 3))

COLUNAS_ESPERADAS = [
    "step",
    "type",
    "amount",
    "nameOrig",
    "oldbalanceOrg",
    "newbalanceOrig",
    "nameDest",
    "oldbalanceDest",
    "newbalanceDest",
    "isFraud",
    "isFlaggedFraud",
]