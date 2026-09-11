"""
test_limpeza.py — Testes do módulo de limpeza.
"""

import pandas as pd
import pytest
from src import limpeza

CAMINHO_FIXTURE = "tests/fixtures/amostra_transacoes.csv"


@pytest.fixture
def df_bruto():
    return pd.read_csv(CAMINHO_FIXTURE)


def test_carregar_dados_retorna_dataframe():
    df = limpeza.carregar_dados(CAMINHO_FIXTURE)
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_validar_schema_sem_colunas_faltantes(df_bruto):
    faltantes = limpeza.validar_schema(df_bruto)
    assert faltantes == []


def test_validar_schema_detecta_coluna_faltante(df_bruto):
    df_incompleto = df_bruto.drop(columns=["isFraud"])
    faltantes = limpeza.validar_schema(df_incompleto)
    assert "isFraud" in faltantes


def test_remover_duplicatas_remove_linha_repetida(df_bruto):
    total_antes = len(df_bruto)
    df_limpo = limpeza.remover_duplicatas(df_bruto)
    assert len(df_limpo) < total_antes


def test_remover_valores_invalidos_remove_amount_zero(df_bruto):
    df_limpo = limpeza.remover_valores_invalidos(df_bruto)
    assert (df_limpo["amount"] > 0).all()


def test_padronizar_tipos_converte_isfraud_para_int(df_bruto):
    df_padronizado = limpeza.padronizar_tipos(df_bruto)
    assert df_padronizado["isFraud"].dtype == int


def test_limpar_dados_pipeline_completo(df_bruto):
    df_limpo = limpeza.limpar_dados(df_bruto)
    assert df_limpo["amount"].gt(0).all()
    assert df_limpo.duplicated().sum() == 0