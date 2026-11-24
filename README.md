# ADS - Análise de Dados: Criminalidade no Paraná

## 1. Sobre o projeto

Este projeto tem como objetivo realizar uma análise de dados sobre a criminalidade nos municípios do estado do Paraná, utilizando informações do ano de 2025.

## 2. Objetivos

- Analisar a distribuição de ocorrências criminais nos municípios do Paraná.
- Apresentar os resultados das observações e análises por meio de visualizações interativas.

## 3. Tecnologias utilizadas

- Python
- Pandas
- Streamlit
- Plotly
- Statsmodels

## 4. Base de dados

O projeto utiliza o arquivo `Crimes_Tabela.csv`, com dados de ocorrências criminais dos municípios do Paraná, de 2025.
Fonte: Portal de Dados Abertos do Paraná.

## 5. Metodologia

O processamento dos dados é realizado pelo Pandas e inclui:

1. Leitura do arquivo CSV.
2. Ajuste dos nomes das colunas.
3. Remoção da linha referente ao total estadual.
4. Remoção de registros duplicados.
5. Tratamento de valores ausentes ou representados por traços.
6. Conversão das colunas numéricas.
7. Padronização dos nomes das colunas.
8. Reorganização dos dados para facilitar as análises.

## 6. Como executar o projeto

### Pré-requisitos

- Python instalado.

### Instalação

Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta:

```bash
cd analise-criminalidade-parana
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual no Windows:

```bash
.venv\Scripts\activate
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a aplicação:

```bash
streamlit run app.py
```

O Streamlit irá disponibilizar o endereço local para acessar a aplicação pelo navegador.

## 7. Produzido por:

Julia Camilly Vieira Rodrigues

Eduarda Nozykowski