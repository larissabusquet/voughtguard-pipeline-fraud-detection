# VoughtGuard — Pipeline de Detecção de Fraude Financeira

Pipeline de dados para processar transações financeiras, aplicar limpeza e validação de qualidade, gerar tabelas analíticas para o time de risco e produzir um relatório automatizado de Data Quality.

## Sobre o projeto

O dataset utilizado ([PaySim — Synthetic Financial Fraud Dataset](https://www.kaggle.com/datasets/umitka/synthetic-financial-fraud-dataset/data)) simula transações de mobile money e contém uma coluna `isFraud` (fraude real) e `isFlaggedFraud` (sinalização automática de um sistema de alerta simples).

Um dos principais achados do pipeline: das 8.197 transações fraudulentas do dataset, **99,8% não foram sinalizadas** pelo sistema de alerta existente, evidenciando a necessidade de um pipeline de detecção mais robusto.

Outros achados:
- Fraude está 100% concentrada em transações do tipo `TRANSFER` (0,77% de taxa de fraude) e `CASH_OUT` (0,18%). Os tipos `PAYMENT`, `CASH_IN` e `DEBIT` não apresentam nenhum caso de fraude na base.
- Diferente do repositório de referência que inspirou este projeto, este dataset não possui coluna de país, por isso, o ranking analítico por país foi substituído por um **ranking por tipo de transação**, que se mostrou mais relevante para o problema.

## Estrutura do repositório

```
voughtguard-pipeline-fraud-detection/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── Contributing.md
│
├── data/
│   ├── raw/              # dataset original — não commitado
│   ├── staging/          # dados intermediários — não commitado
│   └── processed/
│       ├── ranking_tipo_transacao_fraude.csv
│       ├── top_merchant_risco.csv
│       └── relatorio_qualidade.csv
│
├── src/
│   ├── config.py
│   ├── pipeline.py
│   ├── limpeza.py
│   ├── transformacao.py
│   ├── qualidade.py
│   └── tabelas_analiticas.py
│
├── tests/
│   ├── fixtures/
│   ├── test_limpeza.py
│   └── test_transformacao.py
│
├── notebooks/
│   ├── exploracao.ipynb
│   ├── exploracao_limpeza.ipynb
│   └── analise_fraude.ipynb
│
└── docs/
    ├── orquestracao.md
    └── orientacoes-desafio.md
```


## Como rodar o projeto

1. Clone este repositório
2. Crie um ambiente virtual: `python -m venv .venv`
3. Ative o ambiente virtual:
   - Linux/Mac: `source .venv/bin/activate`
   - Windows: `.venv\Scripts\activate`
4. Instale as dependências: `pip install -r requirements.txt`
5. Copie `.env.example` para `.env` e ajuste os valores se necessário
6. Baixe o dataset ([Kaggle — Synthetic Financial Fraud Dataset](https://www.kaggle.com/datasets/umitka/synthetic-financial-fraud-dataset/data))
   e salve em `data/raw/transactions.csv`
7. Execute o pipeline: `python -m src.pipeline`
8. Rode os testes com cobertura: `pytest --cov=src tests/`

## Resultados gerados

Após rodar o pipeline, três arquivos são gerados em `data/processed/`:

- **`relatorio_qualidade.csv`** — completude das colunas, duplicatas, taxa de fraude e taxa de sinalização automática
- **`ranking_tipo_transacao_fraude.csv`** — volume, valor movimentado e taxa de fraude por tipo de transação
- **`top_merchant_risco.csv`** — merchants com maior número de transações fraudulentas recebidas (vazio nesta base, já que fraude nunca tem merchant como destino — ver seção "Sobre o projeto")

## Tecnologias

Python · Pandas · Pytest · Jupyter
