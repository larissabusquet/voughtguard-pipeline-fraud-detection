"""
transformacao.py — Criação de colunas derivadas para análise de fraude.
"""

import pandas as pd

"""Marca as transações cujo destino é um merchant (comercial) com base no prefixo do nome do destino."""
def flag_merchant_destino(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["destino_e_merchant"] = df["nameDest"].str.startswith("M")
    return df

"""
Calcula a diferença entre o valor esperado (pela movimentação de saldo) e o valor real da transação. 
Grandes divergências são um sinal forte de fraude.
"""
def calcular_erro_saldo(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["erro_saldo_origem"] = (
        df["newbalanceOrig"] + df["amount"] - df["oldbalanceOrg"]
    )
    df["erro_saldo_destino"] = (
        df["oldbalanceDest"] + df["amount"] - df["newbalanceDest"]
    )
    return df

"""Marca transações suspeitas onde o saldo de origem e destino é zero, mas o valor da transação é positivo."""
def flag_saldo_zerado_suspeito(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["saldo_origem_zerado_suspeito"] = (
        (df["oldbalanceOrg"] == 0) & (df["newbalanceOrig"] == 0) & (df["amount"] > 0)
    )
    return df

"""Classifica o valor da transação em faixas: baixo, médio, alto e muito alto."""
def classificar_faixa_valor(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    bins = [0, 1000, 10000, 100000, float("inf")]
    labels = ["baixo", "medio", "alto", "muito_alto"]
    df["faixa_valor"] = pd.cut(df["amount"], bins=bins, labels=labels, right=False)
    return df

"""Executa todas as transformações em sequência."""
def aplicar_transformacoes(df: pd.DataFrame) -> pd.DataFrame:
    df = flag_merchant_destino(df)
    df = calcular_erro_saldo(df)
    df = flag_saldo_zerado_suspeito(df)
    df = classificar_faixa_valor(df)
    return df