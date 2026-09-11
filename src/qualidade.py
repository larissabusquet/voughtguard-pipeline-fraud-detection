"""
qualidade.py — Geração do relatório de Data Quality.
"""

import pandas as pd


def calcular_completude(df: pd.DataFrame) -> pd.DataFrame:
    """Percentual de valores não nulos por coluna."""
    completude = (1 - df.isnull().mean()) * 100
    return completude.reset_index().rename(
        columns={"index": "coluna", 0: "completude_pct"}
    )


def calcular_taxa_fraude(df: pd.DataFrame) -> float:
    """Percentual de transações marcadas como fraude."""
    return round(df["isFraud"].mean() * 100, 4)


def calcular_taxa_flagged(df: pd.DataFrame) -> float:
    """Percentual de transações sinalizadas pelo sistema (isFlaggedFraud)."""
    return round(df["isFlaggedFraud"].mean() * 100, 4)


def calcular_divergencia_flag(df: pd.DataFrame) -> dict:
    """
    Compara isFraud (fraude real) com isFlaggedFraud (sistema de alerta),
    mostrando quantas fraudes passaram sem ser sinalizadas.
    """
    fraudes_nao_sinalizadas = df[(df["isFraud"] == 1) & (df["isFlaggedFraud"] == 0)]
    total_fraudes = df[df["isFraud"] == 1]
    return {
        "total_fraudes": len(total_fraudes),
        "fraudes_nao_sinalizadas": len(fraudes_nao_sinalizadas),
        "pct_fraudes_nao_sinalizadas": round(
            len(fraudes_nao_sinalizadas) / max(len(total_fraudes), 1) * 100, 2
        ),
    }


def contar_duplicatas(df: pd.DataFrame) -> int:
    """Conta linhas duplicadas no dataframe."""
    return int(df.duplicated().sum())


def gerar_relatorio_qualidade(df: pd.DataFrame) -> pd.DataFrame:
    """Monta o relatório final de qualidade dos dados em formato tabular."""
    divergencia = calcular_divergencia_flag(df)

    linhas = [
        {"metrica": "total_registros", "valor": len(df)},
        {"metrica": "duplicatas", "valor": contar_duplicatas(df)},
        {"metrica": "taxa_fraude_pct", "valor": calcular_taxa_fraude(df)},
        {"metrica": "taxa_flagged_pct", "valor": calcular_taxa_flagged(df)},
        {"metrica": "total_fraudes", "valor": divergencia["total_fraudes"]},
        {
            "metrica": "fraudes_nao_sinalizadas",
            "valor": divergencia["fraudes_nao_sinalizadas"],
        },
        {
            "metrica": "pct_fraudes_nao_sinalizadas",
            "valor": divergencia["pct_fraudes_nao_sinalizadas"],
        },
    ]

    relatorio = pd.DataFrame(linhas)
    completude = calcular_completude(df)
    completude["metrica"] = "completude_" + completude["coluna"]
    completude = completude.rename(columns={"completude_pct": "valor"})[
        ["metrica", "valor"]
    ]

    return pd.concat([relatorio, completude], ignore_index=True)