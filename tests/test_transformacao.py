"""
test_transformacao.py — Testes do módulo de transformação.
"""

import pandas as pd
import pytest
from src import transformacao

CAMINHO_FIXTURE = "tests/fixtures/amostra_transacoes.csv"


@pytest.fixture
def df_amostra():
    return pd.read_csv(CAMINHO_FIXTURE)


def test_flag_merchant_destino_identifica_prefixo_m(df_amostra):
    df = transformacao.flag_merchant_destino(df_amostra)
    esperado = df_amostra["nameDest"].str.startswith("M")
    assert (df["destino_e_merchant"] == esperado).all()


def test_calcular_erro_saldo_cria_colunas(df_amostra):
    df = transformacao.calcular_erro_saldo(df_amostra)
    assert "erro_saldo_origem" in df.columns
    assert "erro_saldo_destino" in df.columns


def test_flag_saldo_zerado_suspeito_detecta_padrao(df_amostra):
    df = transformacao.flag_saldo_zerado_suspeito(df_amostra)
    linha_suspeita = df[
        (df["oldbalanceOrg"] == 0) & (df["newbalanceOrig"] == 0) & (df["amount"] > 0)
    ]
    assert linha_suspeita["saldo_origem_zerado_suspeito"].all()


def test_classificar_faixa_valor_atribui_categoria(df_amostra):
    df = transformacao.classificar_faixa_valor(df_amostra)
    assert "faixa_valor" in df.columns
    assert not df["faixa_valor"].isnull().any() or (df_amostra["amount"] == 0).any()


def test_aplicar_transformacoes_executa_sem_erro(df_amostra):
    df = transformacao.aplicar_transformacoes(df_amostra)
    colunas_esperadas = {
        "destino_e_merchant",
        "erro_saldo_origem",
        "erro_saldo_destino",
        "saldo_origem_zerado_suspeito",
        "faixa_valor",
    }
    assert colunas_esperadas.issubset(df.columns)