# 📊 Projeto de Automação DRE

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Versão Python">
  <img src="https://img.shields.io/badge/pandas-2.0+-green.svg" alt="Versão Pandas">
  <img src="https://img.shields.io/badge/Licen%C3%A7a-MIT-yellow.svg" alt="Licença">
  <img src="https://img.shields.io/badge/CI-GitHub%20Actions-orange.svg" alt="CI">
</p>

Pipeline ETL automatizado para processamento de demonstrativos financeiros **DRE (Demonstração do Resultado do Exercício)**. Este projeto extrai, limpa, transforma e estrutura dados financeiros brasileiros para análise, relatórios e futuras previsões baseadas em IA.

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Início Rápido](#-início-rápido)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Formato dos Dados de Entrada](#-formato-dos-dados-de-entrada)
- [Arquivos de Saída](#-arquivos-de-saída)
- [Configuração](#%EF%B8%8F-configuração)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Testes](#-testes)
- [GitHub Actions CI/CD](#-github-actions-cicd)
- [Referência da API](#-referência-da-api)
- [Solução de Problemas](#-solução-de-problemas)
- [Roadmap Futuro](#-roadmap-futuro)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

---

## 🎯 Visão Geral

O projeto de Automação DRE é um pipeline Python modular projetado para:

1. **Extrair** dados financeiros de exportações CSV (geralmente de ferramentas de BI)
2. **Transformar** formatos de moeda brasileira e abreviações de datas em português
3. **Carregar** dados processados em formato Parquet otimizado
4. **Gerar** hierarquias de categorias para classificação baseada em LLM

Este pipeline está pronto para produção com integração GitHub Actions CI/CD, testes abrangentes e logging detalhado.

### Por que este Projeto?

- 🇧🇷 **Tratamento de Formato Brasileiro**: Suporte nativo para formato de moeda R$ e nomes de meses em português
- ⚡ **Performance**: Saída em Parquet para leituras 10x mais rápidas comparado ao CSV
- 🤖 **Pronto para IA**: Extração de categorias prepara dados para classificação LLM
- 🔄 **Automatizado**: Workflow GitHub Actions para processamento contínuo
- 🧪 **Testado**: 35+ testes unitários garantindo confiabilidade

---

## ✨ Funcionalidades

| Funcionalidade | Descrição |
|----------------|-----------|
| **Conversão de Moeda** | Converte `R$ 1.234,56` → `1234.56` com suporte a valores negativos |
| **Parsing de Meses** | Mapeia abreviações em português (Jan, Fev, Mar...) para datetime |
| **Extração de Categorias** | Constrói JSON hierárquico de categorias financeiras |
| **Exportação Parquet** | Armazenamento colunar para análises eficientes |
| **Logging Abrangente** | Logging em níveis INFO/ERROR com timestamps |
| **Validação de Entrada** | Verifica colunas obrigatórias e formatos válidos |
| **Pipeline CI/CD** | Processamento automatizado via GitHub Actions |

---

## 📦 Pré-requisitos

### Software Necessário

- **Python**: 3.11 ou superior
- **pip**: Versão mais recente recomendada
- **Git**: Para controle de versão e clonagem

### Requisitos do Sistema

- **SO**: Windows, macOS ou Linux
- **RAM**: Mínimo 4GB (8GB recomendado para arquivos grandes)
- **Disco**: 100MB para dependências + espaço para arquivos de dados

### Verificar Pré-requisitos

```bash
# Verificar versão do Python
python --version  # Deve ser 3.11+

# Verificar pip
pip --version

# Verificar Git
git --version
```

---

## 🚀 Instalação

### Opção 1: Clonar do GitHub

```bash
# Clonar o repositório
git clone https://github.com/villarantonio/Projeto_DRE.git
cd Projeto_DRE

# Criar ambiente virtual (recomendado)
python -m venv venv

# Ativar ambiente virtual
# No Windows:
.\venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### Opção 2: Configuração Manual

```bash
# Criar diretório do projeto
mkdir Projeto_DRE
cd Projeto_DRE

# Instalar dependências manualmente
pip install pandas>=2.0.0 numpy>=1.24.0 pyarrow>=14.0.0 pytest>=7.4.0
```

### Verificar Instalação

```bash
# Executar testes para verificar se tudo está funcionando
python -m pytest tests/ -v

# Saída esperada: 35 passed
```

---

## ⚡ Início Rápido

### 1. Coloque seu Arquivo de Dados

Copie seu arquivo CSV DRE para a raiz do projeto:

```bash
cp /caminho/para/seu/DRE_BI(BaseDRE).csv .
```

### 2. Execute o Pipeline

```bash
python main.py
```

### 3. Verifique a Saída

```bash
# Visualizar arquivos gerados
ls output/
# Saída: categories.json  processed_dre.parquet

# Pré-visualizar categorias
cat output/categories.json
```

### Saída Esperada no Console

```
============================================================
PIPELINE DE AUTOMAÇÃO DRE FINANCEIRO
============================================================

📊 Registros Processados: 560
📅 Ano de Referência: 2025

📁 Estatísticas de Categorias:
   - Categorias Macro (Nome Grupo): 13
   - Categorias Detalhadas (cc_nome): 116

💰 Resumo Financeiro:
   - Valor Total: R$ -3.927.512,00
   - Total Positivo (Receitas): R$ 5.767.098,00
   - Total Negativo (Custos): R$ -9.694.610,00

✅ PIPELINE CONCLUÍDO COM SUCESSO
```

---

## 📁 Estrutura do Projeto

```
Projeto_DRE/
│
├── 📂 .github/
│   └── 📂 workflows/
│       └── 📄 process_dre.yml      # Workflow CI/CD GitHub Actions
│
├── 📂 src/                          # Módulos de código fonte
│   ├── 📄 __init__.py              # Inicialização do pacote
│   ├── 📄 data_cleaner.py          # Funções de limpeza de dados
│   └── 📄 category_engine.py       # Classe de gerenciamento de categorias
│
├── 📂 tests/                        # Testes unitários
│   ├── 📄 __init__.py
│   ├── 📄 test_data_cleaner.py     # Testes para data_cleaner (22 testes)
│   └── 📄 test_category_engine.py  # Testes para category_engine (13 testes)
│
├── 📂 output/                       # Arquivos de saída gerados (ignorados pelo git)
│   ├── 📄 processed_dre.parquet    # Dados financeiros processados
│   └── 📄 categories.json          # Hierarquia de categorias
│
├── 📄 config.py                     # Configuração centralizada
├── 📄 main.py                       # Orquestrador principal do pipeline
├── 📄 requirements.txt              # Dependências Python
├── 📄 .gitignore                    # Regras de ignore do Git
└── 📄 README.md                     # Esta documentação
```

### Descrição dos Módulos

| Módulo | Linhas | Descrição |
|--------|--------|-----------|
| `config.py` | ~70 | Configuração centralizada (caminhos, encodings, mapeamento de colunas) |
| `src/data_cleaner.py` | ~300 | Carregamento CSV, conversão de moeda, parsing de datas |
| `src/category_engine.py` | ~240 | Extração de categorias e persistência JSON |
| `main.py` | ~190 | Orquestração do pipeline com logging e relatórios |

---

## 📊 Formato dos Dados de Entrada

### Especificações do Arquivo

| Propriedade | Valor |
|-------------|-------|
| **Nome do Arquivo** | `DRE_BI(BaseDRE).csv` (configurável) |
| **Encoding** | Latin-1 (ISO-8859-1) ou UTF-8 |
| **Delimitador** | Ponto e vírgula (`;`) |
| **Linha do Cabeçalho** | Linha 5 (linhas 1-4 são metadados) |

### Estrutura do CSV

```csv
Ano Txt;2025;;;;;;                    ← Metadados (ignorados)
situacao;(Vários itens);;;;;;         ← Metadados (ignorados)
GrupoEmpresa;Grupo J+;;;;;;           ← Metadados (ignorados)
;;;;;;;                               ← Metadados (ignorados)
Loja;_key_centro_custo;cc_parent_nome;Nome Grupo;cc_nome;Camada03;Mês;Realizado  ← Cabeçalho
CORPORATIVO J+;01.01.001;01.01;RECEITAS S/ VENDAS;DINHEIRO;DINHEIRO;Ago;R$ 63.713
CORPORATIVO J+;02.01.001.01;02.01.001;( - ) CUSTOS VARIÁVEIS;BOVINOS;PROTEINAS;Nov;-R$ 1.351
```

### Colunas Obrigatórias

| Coluna | Tipo | Descrição | Exemplo |
|--------|------|-----------|---------|
| `Nome Grupo` | string | Categoria financeira macro | `"RECEITAS S/ VENDAS"` |
| `cc_nome` | string | Nome da categoria detalhada | `"DINHEIRO"`, `"BOVINOS"` |
| `Mês` | string | Abreviação do mês em português | `"Ago"`, `"Set"`, `"Dez"` |
| `Realizado` | string | Formato de moeda brasileira | `"R$ 63.713"`, `"-R$ 1.351"` |

### Mapeamento de Abreviações de Meses

| Abreviação | Mês | Número |
|------------|-----|--------|
| Jan | Janeiro | 1 |
| Fev | Fevereiro | 2 |
| Mar | Março | 3 |
| Abr | Abril | 4 |
| Mai | Maio | 5 |
| Jun | Junho | 6 |
| Jul | Julho | 7 |
| Ago | Agosto | 8 |
| Set | Setembro | 9 |
| Out | Outubro | 10 |
| Nov | Novembro | 11 |
| Dez | Dezembro | 12 |

---

## 📤 Arquivos de Saída

### 1. `processed_dre.parquet`

Formato colunar otimizado contendo todos os dados transformados.

**Schema:**

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `Loja` | string | Nome da loja/filial |
| `_key_centro_custo` | string | Chave do centro de custo |
| `cc_parent_nome` | string | Centro de custo pai |
| `Nome Grupo` | string | Categoria macro |
| `cc_nome` | string | Categoria detalhada |
| `Camada03` | string | Classificação camada 3 |
| `Mês` | datetime64 | Data da transação (primeiro dia do mês) |
| `Realizado` | float64 | Valor monetário (convertido) |

**Lendo o Arquivo Parquet:**

```python
import pandas as pd

df = pd.read_parquet("output/processed_dre.parquet")
print(df.head())
print(df.dtypes)
```

### 2. `categories.json`

Mapeamento hierárquico de categorias financeiras para contexto LLM.

**Estrutura:**

```json
{
  "( - ) CUSTOS VARIÁVEIS": [
    "AGUAS",
    "AVES",
    "BOVINOS",
    "CACHAÇA",
    "EMBALAGENS",
    "..."
  ],
  "RECEITAS S/ VENDAS": [
    "DINHEIRO",
    "IFOOD",
    "PIX",
    "TED/DOC"
  ]
}
```

**Uso em Python:**

```python
import json

with open("output/categories.json", "r", encoding="utf-8") as f:
    categories = json.load(f)

# Obter todas as categorias macro
print(list(categories.keys()))

# Obter detalhes de uma categoria específica
print(categories["RECEITAS S/ VENDAS"])
```

---

## ⚙️ Configuração

Toda a configuração está centralizada em `config.py`:

### Caminhos de Arquivos

```python
# Diretório base (raiz do projeto)
BASE_DIR: Path = Path(__file__).parent

# Arquivo de entrada
INPUT_FILE_NAME: str = "DRE_BI(BaseDRE).csv"
INPUT_FILE_PATH: Path = BASE_DIR / INPUT_FILE_NAME

# Diretório e arquivos de saída
OUTPUT_DIR: Path = BASE_DIR / "output"
PROCESSED_PARQUET_PATH: Path = OUTPUT_DIR / "processed_dre.parquet"
CATEGORIES_JSON_PATH: Path = OUTPUT_DIR / "categories.json"
```

### Parsing do CSV

```python
CSV_SEPARATOR: str = ";"           # Delimitador de colunas
CSV_ENCODING: str = "latin-1"      # Encoding do arquivo (latin-1 ou utf-8)
CSV_HEADER_ROW: int = 4            # Posição da linha do cabeçalho (índice 0)
```

### Processamento de Datas

```python
REFERENCE_YEAR: int = 2025         # Ano para conversão de datas

MONTH_MAPPING: dict[str, int] = {
    "Jan": 1, "Fev": 2, "Mar": 3, "Abr": 4,
    "Mai": 5, "Jun": 6, "Jul": 7, "Ago": 8,
    "Set": 9, "Out": 10, "Nov": 11, "Dez": 12,
}
```

### Nomes das Colunas

```python
COLUMN_NOME_GRUPO: str = "Nome Grupo"
COLUMN_CC_NOME: str = "cc_nome"
COLUMN_MES: str = "Mês"
COLUMN_REALIZADO: str = "Realizado"
```

### Logging

```python
LOG_LEVEL: str = "INFO"
LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

---

## 💡 Exemplos de Uso

### Execução Básica do Pipeline

```bash
# Execução padrão
python main.py

# Com saída detalhada (nível DEBUG)
# Edite config.py: LOG_LEVEL = "DEBUG"
python main.py
```

### Usando Módulos Individuais

#### Conversão de Moeda

```python
from src.data_cleaner import convert_brazilian_currency

# Converter vários formatos
print(convert_brazilian_currency("R$ 1.234,56"))    # → 1234.56
print(convert_brazilian_currency("-R$ 19.026"))     # → -19026.0
print(convert_brazilian_currency("R$ 0,00"))        # → 0.0
```

#### Conversão de Mês

```python
from src.data_cleaner import convert_month_to_date

# Converter meses em português para datetime
date = convert_month_to_date("Ago", 2025)
print(date)  # → 2025-08-01 00:00:00
```

#### Carregar e Processar CSV

```python
from src.data_cleaner import (
    load_dre_csv,
    apply_currency_conversion,
    apply_month_conversion,
)

# Carregar CSV
df = load_dre_csv("DRE_BI(BaseDRE).csv")

# Aplicar transformações
df = apply_currency_conversion(df, "Realizado")
df = apply_month_conversion(df, "Mês", 2025)

print(df.info())
```

#### Extrair Categorias

```python
from src.category_engine import CategoryManager

manager = CategoryManager()

# Extrair hierarquia do DataFrame
categories = manager.extract_category_hierarchy(df)

# Salvar em JSON
manager.save_categories_json(categories, "output/categories.json")

# Obter estatísticas resumidas
summary = manager.get_category_summary(categories)
print(f"Total de grupos: {summary['total_groups']}")
print(f"Total de detalhes: {summary['total_details']}")
```

### Analisando Dados de Saída

```python
import pandas as pd

# Carregar dados processados
df = pd.read_parquet("output/processed_dre.parquet")

# Agrupar por categoria
by_group = df.groupby("Nome Grupo")["Realizado"].sum()
print(by_group.sort_values())

# Totais mensais
by_month = df.groupby("Mês")["Realizado"].sum()
print(by_month)

# Filtrar apenas receitas
revenues = df[df["Realizado"] > 0]
print(f"Total de registros de receita: {len(revenues)}")
```

---

## 🧪 Testes

### Executar Todos os Testes

```bash
# Execução básica de testes
python -m pytest tests/ -v

# Com relatório de cobertura
python -m pytest tests/ -v --cov=src --cov-report=html

# Executar arquivo de teste específico
python -m pytest tests/test_data_cleaner.py -v

# Executar classe de teste específica
python -m pytest tests/test_data_cleaner.py::TestConvertBrazilianCurrency -v
```

### Cobertura de Testes

| Módulo | Testes | Cobertura |
|--------|--------|-----------|
| `data_cleaner.py` | 22 | Conversão de moeda, parsing de mês, carregamento CSV |
| `category_engine.py` | 13 | Extração de hierarquia, I/O JSON, resumos |
| **Total** | **35** | Todas as funções críticas |

### Exemplos de Testes

```python
# Testes de conversão de moeda
def test_valor_positivo_com_centavos():
    assert convert_brazilian_currency("R$ 1.234,56") == 1234.56

def test_valor_negativo():
    assert convert_brazilian_currency("-R$ 1.234,56") == -1234.56

# Testes de conversão de mês
def test_agosto():
    result = convert_month_to_date("Ago", 2025)
    assert result == pd.Timestamp("2025-08-01")

# Testes de extração de categorias
def test_extract_category_hierarchy():
    hierarchy = manager.extract_category_hierarchy(df)
    assert "RECEITAS S/ VENDAS" in hierarchy
```

---

## 🔄 GitHub Actions CI/CD

### Visão Geral do Workflow

O pipeline está configurado para executar automaticamente via GitHub Actions.

**Arquivo:** `.github/workflows/process_dre.yml`

### Gatilhos

| Gatilho | Descrição |
|---------|-----------|
| `push` para `main` | Executa em cada push para a branch main |
| `workflow_dispatch` | Gatilho manual com parâmetros opcionais |

### Jobs

1. **process-dre**: Pipeline de processamento principal
   - Checkout do código
   - Configurar Python 3.11
   - Instalar dependências
   - Executar `main.py`
   - Upload de artefatos

2. **validate**: Validação de integridade dos dados
   - Download de artefatos processados
   - Verificar arquivos Parquet e JSON
   - Checar colunas obrigatórias e tipos de dados

### Artefatos

| Artefato | Conteúdo | Retenção |
|----------|----------|----------|
| `dre-processed-data` | Parquet + JSON | 30 dias |
| `processing-logs` | Arquivos de log | 7 dias |

### Gatilho Manual

```bash
# Via GitHub CLI
gh workflow run process_dre.yml

# Com parâmetros
gh workflow run process_dre.yml -f reference_year=2024
```

> **Nota:** O workflow está atualmente desabilitado para configuração inicial. Para habilitar, remova a condição `if: false` do arquivo do workflow.

---

## 📚 Referência da API

### Módulo data_cleaner

#### `load_dre_csv(file_path: str | Path) -> pd.DataFrame`

Carrega arquivo CSV DRE com tratamento de metadados.

**Parâmetros:**
- `file_path`: Caminho para o arquivo CSV

**Retorna:** DataFrame com dados carregados

**Exceções:**
- `FileNotFoundError`: Arquivo não existe
- `ValueError`: Colunas obrigatórias ausentes

---

#### `convert_brazilian_currency(value: str) -> float`

Converte string de moeda brasileira para float.

**Parâmetros:**
- `value`: String de moeda (ex: "R$ 1.234,56")

**Retorna:** Valor float

**Exceções:**
- `ValueError`: Formato inválido
- `TypeError`: Entrada não é string

---

#### `convert_month_to_date(month_str: str, reference_year: int) -> pd.Timestamp`

Converte abreviação de mês em português para Timestamp.

**Parâmetros:**
- `month_str`: Abreviação do mês (ex: "Ago")
- `reference_year`: Ano para a data

**Retorna:** Pandas Timestamp

**Exceções:**
- `ValueError`: Abreviação de mês desconhecida

---

### Módulo category_engine

#### `CategoryManager`

Classe gerenciadora para operações de hierarquia de categorias.

**Métodos:**

| Método | Descrição |
|--------|-----------|
| `extract_category_hierarchy(df)` | Extrai hierarquia de categorias únicas do DataFrame |
| `save_categories_json(categories, path)` | Salva hierarquia em arquivo JSON |
| `load_categories_json(path)` | Carrega hierarquia de arquivo JSON |
| `get_category_summary(categories)` | Gera estatísticas resumidas |

---

## 🔧 Solução de Problemas

### Problemas Comuns

#### 1. Erro de Encoding

```
UnicodeDecodeError: 'utf-8' codec can't decode byte...
```

**Solução:** Altere o encoding em `config.py`:
```python
CSV_ENCODING: str = "latin-1"  # Em vez de "utf-8"
```

#### 2. Colunas Ausentes

```
ValueError: Missing required columns in CSV: ['Mês']
```

**Solução:** Verifique se seu CSV possui as colunas obrigatórias. Confira se os nomes das colunas correspondem exatamente (incluindo acentos).

#### 3. Formato de Moeda Inválido

```
ValueError: Invalid currency format...
```

**Solução:** Certifique-se de que os valores de moeda seguem o padrão `R$ X.XXX,XX` ou `-R$ X.XXX,XX`.

#### 4. Arquivo Não Encontrado

```
FileNotFoundError: DRE file not found...
```

**Solução:** Coloque o arquivo CSV no diretório raiz do projeto ou atualize `INPUT_FILE_PATH` em `config.py`.

### Modo Debug

Habilite logging detalhado:

```python
# Em config.py
LOG_LEVEL: str = "DEBUG"
```

---

## 🔮 Roadmap Futuro

### Fase 1: Previsões (T1 2025)
- [ ] Integrar Facebook Prophet para previsão de séries temporais
- [ ] Previsões de receita mensal
- [ ] Análise de tendência de custos

### Fase 2: Classificação por IA (T2 2025)
- [ ] Integração OpenAI GPT para classificação de categorias
- [ ] Categorização automática de novos itens de despesa
- [ ] Contexto baseado em RAG usando categories.json

### Fase 3: Dashboard (T3 2025)
- [ ] Dashboard interativo Streamlit
- [ ] Visualização de dados em tempo real
- [ ] Exportação para relatórios Excel/PDF

### Fase 4: Suporte Multi-Empresa (T4 2025)
- [ ] Suporte para múltiplos arquivos de empresas
- [ ] Relatórios financeiros consolidados
- [ ] Análise comparativa entre empresas

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, siga estes passos:

1. **Faça um Fork** do repositório
2. **Crie** uma branch de feature (`git checkout -b feature/funcionalidade-incrivel`)
3. **Commit** suas alterações (`git commit -m 'Adiciona funcionalidade incrível'`)
4. **Push** para a branch (`git push origin feature/funcionalidade-incrivel`)
5. **Abra** um Pull Request

### Padrões de Código

- Siga as diretrizes de estilo **PEP 8**
- Adicione **type hints** em todas as funções
- Escreva **docstrings** no estilo Google
- Inclua **testes unitários** para novas funcionalidades
- Atualize o **README** para alterações voltadas ao usuário

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

```
MIT License

Copyright (c) 2025 Antonio Henrique

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/villarantonio/Projeto_DRE/issues)
- **Email**: villar_antonio@discente.ufg.br

---

<p align="center">
  Feito com ❤️ para Automação Financeira Brasileira
</p>

