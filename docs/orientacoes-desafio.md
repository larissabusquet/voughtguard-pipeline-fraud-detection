# Escopo e Objetivos do Desafio

## Contexto

Este projeto foi desenvolvido como exercício de portfólio para a área de dados/engenharia de dados, inspirado na estrutura do repositório
[voughtguard-pipeline-fraud-detection](https://github.com/Starlight-git-project/voughtguard-pipeline-fraud-detection), adaptado para o dataset [PaySim — Synthetic Financial Fraud Dataset](https://www.kaggle.com/datasets/umitka/synthetic-financial-fraud-dataset/data).

## Objetivo

Construir um pipeline de dados que:

1. Processe transações financeiras brutas
2. Aplique limpeza e validação de qualidade
3. Gere tabelas analíticas de apoio ao time de risco
4. Produza um relatório automatizado de Data Quality

## Requisitos técnicos

- Código modularizado em `src/`, com responsabilidades separadas (limpeza, transformação, qualidade, tabelas analíticas, orquestração);
- Testes unitários com `pytest`, usando fixtures de amostra (sem depender do dataset completo);
- Variáveis de configuração externalizadas via `.env`;
- Dados brutos e credenciais nunca versionados no Git;
- Notebooks documentando exploração, validação da limpeza e análise dos padrões de fraude encontrados.

## Adaptações em relação ao repositório de referência

O dataset PaySim não possui coluna de país, presente no projeto de referência. Por isso:

- O `ranking_paises_fraude.csv` foi substituído por `ranking_tipo_transacao_fraude.csv`, dimensão mais relevante neste dataset;
- O `top_merchant_risco.csv` foi mantido, usando o prefixo `M` em `nameDest`, para identificar merchants.

## Critérios de sucesso

- Pipeline executa de ponta a ponta sem erros (`python -m src.pipeline`);
- Testes unitários passam com cobertura completa nos módulos de limpeza e transformação;
- Relatório de qualidade e tabelas analíticas refletem achados reais e documentados (ex: taxa de fraude não sinalizada pelo sistema atual).