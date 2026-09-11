"""
limpeza.py — Funções de limpeza e validação dos dados brutos.
"""

import pandas as pd
from src import config

"""Carrega o dataset bruto das transações."""
def carregar_dados(caminho: str = None) -> pd.DataFrame:
    caminho = caminho or config.RAW_DATA_PATH
    return pd.read_csv(caminho)

"""Valida se o DataFrame possui todas as colunas esperadas. Retorna uma lista de colunas faltantes."""
def validar_schema(df: pd.DataFrame) -> list:
    return [col for col in config.COLUNAS_ESPERADAS if col not in df.columns]

"""Remove as linhas totalmente duplicadas."""
def remover_duplicatas(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates()

"""Remove as transações com valor menor ou igual ao mínimo válido configurado."""
def remover_valores_invalidos(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["amount"] > config.VALOR_MINIMO_VALIDO].copy()

"""Remove as linhas com nulos nas colunas essenciais para a análise."""
def tratar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    colunas_essenciais = ["amount", "type", "nameOrig", "nameDest", "isFraud"]
    return df.dropna(subset=colunas_essenciais)

"Garante que as colunas tenham os tipos de dados corretos"""
def padronizar_tipos(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["type"] = df["type"].astype("category")
    df["isFraud"] = df["isFraud"].astype(int)
    df["isFlaggedFraud"] = df["isFlaggedFraud"].astype(int)
    return df

"""Executa toda a pipeline de limpeza em sequência."""
def limpar_dados(df: pd.DataFrame) -> pd.DataFrame:
    df = remover_duplicatas(df)
    df = tratar_nulos(df)
    df = remover_valores_invalidos(df)
    df = padronizar_tipos(df)
    return df