# Proposta de Orquestração

## Situação atual

O pipeline é executado manualmente via `python -m src.pipeline`, lendo o
dataset completo de `data/raw/transactions.csv` (~493MB, 6,3M linhas) e
gerando os artefatos em `data/processed/`.

## Proposta para produção

### Agendamento

Para um cenário real de ingestão contínua de transações, o pipeline rodaria em uma cadência regular (ex: diária ou por hora, dependendo do
SLA do time de risco), orquestrado por uma ferramenta como **Apache Airflow**, com uma DAG simples:

extrair_transacoes >> limpar_dados >> transformar_dados >> [gerar_relatorio_qualidade, gerar_tabelas_analiticas] >> notificar_time_risco


Cada etapa corresponderia a uma task independente, permitindo retry automático em caso de falha e alertas caso o relatório de qualidade aponte queda abrupta de completude ou volume de dados fora do esperado.

### Escalabilidade

Com o volume atual (6,3M linhas, ~493MB), o pipeline em Pandas roda localmente sem problemas. 
Para volumes maiores (ex: 100x, na escala de dezenas de GB por execução):

- Migrar de CSV para **Parquet** (formato colunar, compressão nativa, leitura seletiva de colunas);
- Particionar os dados por `step` (proxy de tempo no PaySim) para permitir processamento incremental, em vez de reprocessar a base inteira a cada execução;
- Considerar **Spark** ou **DuckDB** no lugar do Pandas puro, caso o volume não caiba confortavelmente em memória.

### Monitoramento

- O `relatorio_qualidade.csv` já gerado pelo pipeline serve como base para
  alertas automáticos (ex: taxa de nulos acima de um limite, queda no
  volume de transações processadas)
- Métricas de execução (tempo de processamento, linhas processadas,
  linhas rejeitadas na limpeza) poderiam ser expostas para um dashboard
  de observabilidade do pipeline em si, separado do dashboard de negócio

### Próximos passos técnicos

- Adicionar testes para `qualidade.py` e `tabelas_analiticas.py` (atualmente sem cobertura)
- Avaliar treinamento de um modelo supervisionado (Random Forest ou XGBoost) para detecção de fraude, usando as features já criadas em `transformacao.py`, como evolução natural deste pipeline.