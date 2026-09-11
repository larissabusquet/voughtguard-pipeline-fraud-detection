"""
tabelas_analiticas.py — Tabelas analíticas de risco para o time de risco.
"""

import pandas as pd


def ranking_tipo_transacao_fraude(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ranking de tipos de transação (PAYMENT, TRANSFER, CASH_OUT, CASH_IN, DEBIT)
    por volume e taxa de fraude. Substitui o ranking por país, ausente neste dataset.
    """
    ranking = (
        df.groupby("type", observed=True)
        .agg(
            total_transacoes=("amount", "count"),
            total_fraudes=("isFraud", "sum"),
            valor_total_movimentado=("amount", "sum"),
        )
        .reset_index()
    )
    ranking["taxa_fraude_pct"] = round(
        ranking["total_fraudes"] / ranking["total_transacoes"] * 100, 4
    )
    return ranking.sort_values("taxa_fraude_pct", ascending=False).reset_index(
        drop=True
    )


def top_merchant_risco(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """
    Ranking dos merchants (nameDest iniciado com 'M') que mais receberam
    transações fraudulentas.
    """
    merchants = df[df["destino_e_merchant"]]
    ranking = (
        merchants.groupby("nameDest")
        .agg(
            total_transacoes=("amount", "count"),
            total_fraudes=("isFraud", "sum"),
            valor_total_recebido=("amount", "sum"),
        )
        .reset_index()
    )
    ranking = ranking[ranking["total_fraudes"] > 0]
    return ranking.sort_values("total_fraudes", ascending=False).head(top_n)


def gerar_tabelas_analiticas(df: pd.DataFrame) -> dict:
    """Gera todas as tabelas analíticas e retorna em um dicionário."""
    return {
        "ranking_tipo_transacao_fraude": ranking_tipo_transacao_fraude(df),
        "top_merchant_risco": top_merchant_risco(df),
    }