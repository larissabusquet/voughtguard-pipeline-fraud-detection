"""
pipeline.py — Orquestração principal do pipeline VoughtGuard.
"""

import os
from src import config, limpeza, transformacao, qualidade, tabelas_analiticas as ta


def executar_pipeline():
    print("1/5 - Carregando dados brutos...")
    df = limpeza.carregar_dados()

    faltantes = limpeza.validar_schema(df)
    if faltantes:
        raise ValueError(f"Colunas obrigatórias ausentes no dataset: {faltantes}")

    print("2/5 - Limpando e validando dados...")
    df = limpeza.limpar_dados(df)

    print("3/5 - Aplicando transformações...")
    df = transformacao.aplicar_transformacoes(df)

    print("4/5 - Gerando relatório de qualidade...")
    relatorio_qualidade = qualidade.gerar_relatorio_qualidade(df)

    print("5/5 - Gerando tabelas analíticas...")
    tabelas = ta.gerar_tabelas_analiticas(df)

    os.makedirs(config.PROCESSED_DATA_PATH, exist_ok=True)

    relatorio_qualidade.to_csv(
        os.path.join(config.PROCESSED_DATA_PATH, "relatorio_qualidade.csv"),
        index=False,
    )
    tabelas["ranking_tipo_transacao_fraude"].to_csv(
        os.path.join(
            config.PROCESSED_DATA_PATH, "ranking_tipo_transacao_fraude.csv"
        ),
        index=False,
    )
    tabelas["top_merchant_risco"].to_csv(
        os.path.join(config.PROCESSED_DATA_PATH, "top_merchant_risco.csv"),
        index=False,
    )

    print(f"Pipeline concluído. {len(df)} registros processados.")
    print(f"Arquivos salvos em: {config.PROCESSED_DATA_PATH}")


if __name__ == "__main__":
    executar_pipeline()