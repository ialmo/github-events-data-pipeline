GitHub Events Data Pipeline

Pipeline simples de engenharia de dados em Python que coleta eventos públicos da GitHub API, armazena dados brutos, normaliza as informações e carrega os dados em um banco SQLite para análise.

Este projeto foi criado com foco na prática de fundamentos de engenharia de dados.

O que o pipeline faz
Consome eventos da GitHub API
Salva os dados brutos em JSON versionado (RAW)
Normaliza os campos relevantes (SILVER)
Carrega os dados estruturados em SQLite com UPSERT (GOLD)
Executa queries SQL para validação dos dados

Tecnologias utilizadas
Python
requests
SQLite
SQL
virtualenv

Estrutura do projeto
src/
ingest_github.py – ingestão da API
transform.py – normalização dos dados
load_sqlite.py – carga no banco
settings.py – configurações
main.py – orquestração do pipeline

Como executar
Criar um ambiente virtual Python
Ativar o ambiente virtual
Instalar as dependências requests e pydantic
Executar o arquivo main.py

Conceitos praticados
ETL / ELT
Camadas RAW, SILVER e GOLD
Idempotência
Versionamento de dados
SQL para validação
