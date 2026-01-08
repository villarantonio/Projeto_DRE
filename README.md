# 📊 DRE Financial Automation Project

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/pandas-2.0+-green.svg" alt="Pandas Version">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  <img src="https://img.shields.io/badge/CI-GitHub%20Actions-orange.svg" alt="CI">
</p>

Automated ETL pipeline for processing **DRE (Demonstração do Resultado do Exercício)** financial statements. This project extracts, cleans, transforms, and structures Brazilian financial data for analysis, reporting, and future AI-powered predictions.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Input Data Format](#-input-data-format)
- [Output Files](#-output-files)
- [Configuration](#%EF%B8%8F-configuration)
- [Usage Examples](#-usage-examples)
- [Testing](#-testing)
- [GitHub Actions CI/CD](#-github-actions-cicd)
- [API Reference](#-api-reference)
- [Troubleshooting](#-troubleshooting)
- [Future Roadmap](#-future-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

The DRE Financial Automation project is a modular Python pipeline designed to:

1. **Extract** financial data from CSV exports (typically from BI tools)
2. **Transform** Brazilian currency formats and Portuguese date abbreviations
3. **Load** processed data into optimized Parquet format
4. **Generate** category hierarchies for LLM-based classification

This pipeline is production-ready with GitHub Actions CI/CD integration, comprehensive testing, and detailed logging.

### Why This Project?

- 🇧🇷 **Brazilian Format Handling**: Native support for R$ currency format and Portuguese month names
- ⚡ **Performance**: Parquet output for 10x faster reads compared to CSV
- 🤖 **AI-Ready**: Category extraction prepares data for LLM classification
- 🔄 **Automated**: GitHub Actions workflow for continuous processing
- 🧪 **Tested**: 35+ unit tests ensuring reliability

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Currency Conversion** | Converts `R$ 1.234,56` → `1234.56` with negative value support |
| **Month Parsing** | Maps Portuguese abbreviations (Jan, Fev, Mar...) to datetime |
| **Category Extraction** | Builds hierarchical JSON of financial categories |
| **Parquet Export** | Columnar storage for efficient analytics |
| **Comprehensive Logging** | INFO/ERROR level logging with timestamps |
| **Input Validation** | Checks for required columns and valid formats |
| **CI/CD Pipeline** | Automated processing via GitHub Actions |

---

## 📦 Prerequisites

### Required Software

- **Python**: 3.11 or higher
- **pip**: Latest version recommended
- **Git**: For version control and cloning

### System Requirements

- **OS**: Windows, macOS, or Linux
- **RAM**: 4GB minimum (8GB recommended for large files)
- **Disk**: 100MB for dependencies + space for data files

### Verify Prerequisites

```bash
# Check Python version
python --version  # Should be 3.11+

# Check pip
pip --version

# Check Git
git --version
```

---

## 🚀 Installation

### Option 1: Clone from GitHub

```bash
# Clone the repository
git clone https://github.com/villarantonio/dre-financial-automation.git
cd dre-financial-automation

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Manual Setup

```bash
# Create project directory
mkdir dre-financial-automation
cd dre-financial-automation

# Install dependencies manually
pip install pandas>=2.0.0 numpy>=1.24.0 pyarrow>=14.0.0 pytest>=7.4.0
```

### Verify Installation

```bash
# Run tests to verify everything is working
python -m pytest tests/ -v

# Expected output: 35 passed
```

---

## ⚡ Quick Start

### 1. Place Your Data File

Copy your DRE CSV file to the project root:

```bash
cp /path/to/your/DRE_BI(BaseDRE).csv .
```

### 2. Run the Pipeline

```bash
python main.py
```

### 3. Check Output

```bash
# View generated files
ls output/
# Output: categories.json  processed_dre.parquet

# Preview categories
cat output/categories.json
```

### Expected Console Output

```
============================================================
DRE FINANCIAL AUTOMATION PIPELINE
============================================================

📊 Records Processed: 560
📅 Reference Year: 2025

📁 Category Statistics:
   - Macro Categories (Nome Grupo): 13
   - Detail Categories (cc_nome): 116

💰 Financial Summary:
   - Total Value: R$ -3,927,512.00
   - Total Positive (Receitas): R$ 5,767,098.00
   - Total Negative (Custos): R$ -9,694,610.00

✅ PIPELINE COMPLETED SUCCESSFULLY
```

---

## 📁 Project Structure

```
dre-financial-automation/
│
├── 📂 .github/
│   └── 📂 workflows/
│       └── 📄 process_dre.yml      # GitHub Actions CI/CD workflow
│
├── 📂 src/                          # Source code modules
│   ├── 📄 __init__.py              # Package initialization
│   ├── 📄 data_cleaner.py          # Data cleaning functions
│   └── 📄 category_engine.py       # Category management class
│
├── 📂 tests/                        # Unit tests
│   ├── 📄 __init__.py
│   ├── 📄 test_data_cleaner.py     # Tests for data_cleaner (22 tests)
│   └── 📄 test_category_engine.py  # Tests for category_engine (13 tests)
│
├── 📂 output/                       # Generated output files (git-ignored)
│   ├── 📄 processed_dre.parquet    # Processed financial data
│   └── 📄 categories.json          # Category hierarchy
│
├── 📄 config.py                     # Centralized configuration
├── 📄 main.py                       # Main pipeline orchestrator
├── 📄 requirements.txt              # Python dependencies
├── 📄 .gitignore                    # Git ignore rules
└── 📄 README.md                     # This documentation
```

### Module Descriptions

| Module | Lines | Description |
|--------|-------|-------------|
| `config.py` | ~70 | Centralized configuration (paths, encodings, column mappings) |
| `src/data_cleaner.py` | ~300 | CSV loading, currency conversion, date parsing |
| `src/category_engine.py` | ~240 | Category extraction and JSON persistence |
| `main.py` | ~190 | Pipeline orchestration with logging and reporting |

---

## 📊 Input Data Format

### File Specifications

| Property | Value |
|----------|-------|
| **File Name** | `DRE_BI(BaseDRE).csv` (configurable) |
| **Encoding** | Latin-1 (ISO-8859-1) or UTF-8 |
| **Delimiter** | Semicolon (`;`) |
| **Header Row** | Line 5 (rows 1-4 are metadata) |

### CSV Structure

```csv
Ano Txt;2025;;;;;;                    ← Metadata (ignored)
situacao;(Vários itens);;;;;;         ← Metadata (ignored)
GrupoEmpresa;Grupo J+;;;;;;           ← Metadata (ignored)
;;;;;;;                               ← Metadata (ignored)
Loja;_key_centro_custo;cc_parent_nome;Nome Grupo;cc_nome;Camada03;Mês;Realizado  ← Header
CORPORATIVO J+;01.01.001;01.01;RECEITAS S/ VENDAS;DINHEIRO;DINHEIRO;Ago;R$ 63.713
CORPORATIVO J+;02.01.001.01;02.01.001;( - ) CUSTOS VARIÁVEIS;BOVINOS;PROTEINAS;Nov;-R$ 1.351
```

### Required Columns

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `Nome Grupo` | string | Macro financial category | `"RECEITAS S/ VENDAS"` |
| `cc_nome` | string | Detailed category name | `"DINHEIRO"`, `"BOVINOS"` |
| `Mês` | string | Portuguese month abbreviation | `"Ago"`, `"Set"`, `"Dez"` |
| `Realizado` | string | Brazilian currency format | `"R$ 63.713"`, `"-R$ 1.351"` |

### Month Abbreviation Mapping

| Abbreviation | Month | Number |
|--------------|-------|--------|
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

## 📤 Output Files

### 1. `processed_dre.parquet`

Optimized columnar format containing all transformed data.

**Schema:**

| Column | Type | Description |
|--------|------|-------------|
| `Loja` | string | Store/branch name |
| `_key_centro_custo` | string | Cost center key |
| `cc_parent_nome` | string | Parent cost center |
| `Nome Grupo` | string | Macro category |
| `cc_nome` | string | Detail category |
| `Camada03` | string | Layer 3 classification |
| `Mês` | datetime64 | Transaction date (first of month) |
| `Realizado` | float64 | Monetary value (converted) |

**Reading the Parquet File:**

```python
import pandas as pd

df = pd.read_parquet("output/processed_dre.parquet")
print(df.head())
print(df.dtypes)
```

### 2. `categories.json`

Hierarchical mapping of financial categories for LLM context.

**Structure:**

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

**Usage in Python:**

```python
import json

with open("output/categories.json", "r", encoding="utf-8") as f:
    categories = json.load(f)

# Get all macro categories
print(list(categories.keys()))

# Get details for a specific category
print(categories["RECEITAS S/ VENDAS"])
```

---

## ⚙️ Configuration

All configuration is centralized in `config.py`:

### File Paths

```python
# Base directory (project root)
BASE_DIR: Path = Path(__file__).parent

# Input file
INPUT_FILE_NAME: str = "DRE_BI(BaseDRE).csv"
INPUT_FILE_PATH: Path = BASE_DIR / INPUT_FILE_NAME

# Output directory and files
OUTPUT_DIR: Path = BASE_DIR / "output"
PROCESSED_PARQUET_PATH: Path = OUTPUT_DIR / "processed_dre.parquet"
CATEGORIES_JSON_PATH: Path = OUTPUT_DIR / "categories.json"
```

### CSV Parsing

```python
CSV_SEPARATOR: str = ";"           # Column delimiter
CSV_ENCODING: str = "latin-1"      # File encoding (latin-1 or utf-8)
CSV_HEADER_ROW: int = 4            # 0-indexed header row position
```

### Date Processing

```python
REFERENCE_YEAR: int = 2025         # Year for date conversion

MONTH_MAPPING: dict[str, int] = {
    "Jan": 1, "Fev": 2, "Mar": 3, "Abr": 4,
    "Mai": 5, "Jun": 6, "Jul": 7, "Ago": 8,
    "Set": 9, "Out": 10, "Nov": 11, "Dez": 12,
}
```

### Column Names

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

## 💡 Usage Examples

### Basic Pipeline Execution

```bash
# Standard execution
python main.py

# With verbose output (DEBUG level)
# Edit config.py: LOG_LEVEL = "DEBUG"
python main.py
```

### Using Individual Modules

#### Currency Conversion

```python
from src.data_cleaner import convert_brazilian_currency

# Convert various formats
print(convert_brazilian_currency("R$ 1.234,56"))    # → 1234.56
print(convert_brazilian_currency("-R$ 19.026"))     # → -19026.0
print(convert_brazilian_currency("R$ 0,00"))        # → 0.0
```

#### Month Conversion

```python
from src.data_cleaner import convert_month_to_date

# Convert Portuguese months to datetime
date = convert_month_to_date("Ago", 2025)
print(date)  # → 2025-08-01 00:00:00
```

#### Load and Process CSV

```python
from src.data_cleaner import (
    load_dre_csv,
    apply_currency_conversion,
    apply_month_conversion,
)

# Load CSV
df = load_dre_csv("DRE_BI(BaseDRE).csv")

# Apply transformations
df = apply_currency_conversion(df, "Realizado")
df = apply_month_conversion(df, "Mês", 2025)

print(df.info())
```

#### Extract Categories

```python
from src.category_engine import CategoryManager

manager = CategoryManager()

# Extract hierarchy from DataFrame
categories = manager.extract_category_hierarchy(df)

# Save to JSON
manager.save_categories_json(categories, "output/categories.json")

# Get summary statistics
summary = manager.get_category_summary(categories)
print(f"Total groups: {summary['total_groups']}")
print(f"Total details: {summary['total_details']}")
```

### Analyzing Output Data

```python
import pandas as pd

# Load processed data
df = pd.read_parquet("output/processed_dre.parquet")

# Group by category
by_group = df.groupby("Nome Grupo")["Realizado"].sum()
print(by_group.sort_values())

# Monthly totals
by_month = df.groupby("Mês")["Realizado"].sum()
print(by_month)

# Filter revenues only
revenues = df[df["Realizado"] > 0]
print(f"Total revenue records: {len(revenues)}")
```

---

## 🧪 Testing

### Run All Tests

```bash
# Basic test run
python -m pytest tests/ -v

# With coverage report
python -m pytest tests/ -v --cov=src --cov-report=html

# Run specific test file
python -m pytest tests/test_data_cleaner.py -v

# Run specific test class
python -m pytest tests/test_data_cleaner.py::TestConvertBrazilianCurrency -v
```

### Test Coverage

| Module | Tests | Coverage |
|--------|-------|----------|
| `data_cleaner.py` | 22 | Currency conversion, month parsing, CSV loading |
| `category_engine.py` | 13 | Hierarchy extraction, JSON I/O, summaries |
| **Total** | **35** | All critical functions |

### Test Examples

```python
# Currency conversion tests
def test_positive_value_with_cents():
    assert convert_brazilian_currency("R$ 1.234,56") == 1234.56

def test_negative_value():
    assert convert_brazilian_currency("-R$ 1.234,56") == -1234.56

# Month conversion tests
def test_agosto():
    result = convert_month_to_date("Ago", 2025)
    assert result == pd.Timestamp("2025-08-01")

# Category extraction tests
def test_extract_category_hierarchy():
    hierarchy = manager.extract_category_hierarchy(df)
    assert "RECEITAS S/ VENDAS" in hierarchy
```

---

## 🔄 GitHub Actions CI/CD

### Workflow Overview

The pipeline is configured to run automatically via GitHub Actions.

**File:** `.github/workflows/process_dre.yml`

### Triggers

| Trigger | Description |
|---------|-------------|
| `push` to `main` | Runs on every push to main branch |
| `workflow_dispatch` | Manual trigger with optional parameters |

### Jobs

1. **process-dre**: Main processing pipeline
   - Checkout code
   - Setup Python 3.11
   - Install dependencies
   - Run `main.py`
   - Upload artifacts

2. **validate**: Data integrity validation
   - Download processed artifacts
   - Verify Parquet and JSON files
   - Check required columns and data types

### Artifacts

| Artifact | Contents | Retention |
|----------|----------|-----------|
| `dre-processed-data` | Parquet + JSON | 30 days |
| `processing-logs` | Log files | 7 days |

### Manual Trigger

```bash
# Via GitHub CLI
gh workflow run process_dre.yml

# With parameters
gh workflow run process_dre.yml -f reference_year=2024
```

> **Note:** The workflow is currently disabled for initial setup. To enable, remove the `if: false` condition from the workflow file.

---

## 📚 API Reference

### data_cleaner Module

#### `load_dre_csv(file_path: str | Path) -> pd.DataFrame`

Load DRE CSV file with metadata handling.

**Parameters:**
- `file_path`: Path to CSV file

**Returns:** DataFrame with loaded data

**Raises:**
- `FileNotFoundError`: File doesn't exist
- `ValueError`: Missing required columns

---

#### `convert_brazilian_currency(value: str) -> float`

Convert Brazilian currency string to float.

**Parameters:**
- `value`: Currency string (e.g., "R$ 1.234,56")

**Returns:** Float value

**Raises:**
- `ValueError`: Invalid format
- `TypeError`: Non-string input

---

#### `convert_month_to_date(month_str: str, reference_year: int) -> pd.Timestamp`

Convert Portuguese month abbreviation to Timestamp.

**Parameters:**
- `month_str`: Month abbreviation (e.g., "Ago")
- `reference_year`: Year for the date

**Returns:** Pandas Timestamp

**Raises:**
- `ValueError`: Unknown month abbreviation

---

### category_engine Module

#### `CategoryManager`

Manager class for category hierarchy operations.

**Methods:**

| Method | Description |
|--------|-------------|
| `extract_category_hierarchy(df)` | Extract unique category hierarchy from DataFrame |
| `save_categories_json(categories, path)` | Save hierarchy to JSON file |
| `load_categories_json(path)` | Load hierarchy from JSON file |
| `get_category_summary(categories)` | Generate summary statistics |

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Encoding Error

```
UnicodeDecodeError: 'utf-8' codec can't decode byte...
```

**Solution:** Change encoding in `config.py`:
```python
CSV_ENCODING: str = "latin-1"  # Instead of "utf-8"
```

#### 2. Missing Columns

```
ValueError: Missing required columns in CSV: ['Mês']
```

**Solution:** Verify your CSV has the required columns. Check if column names match exactly (including accents).

#### 3. Invalid Currency Format

```
ValueError: Invalid currency format...
```

**Solution:** Ensure currency values follow the pattern `R$ X.XXX,XX` or `-R$ X.XXX,XX`.

#### 4. File Not Found

```
FileNotFoundError: DRE file not found...
```

**Solution:** Place the CSV file in the project root directory or update `INPUT_FILE_PATH` in `config.py`.

### Debug Mode

Enable detailed logging:

```python
# In config.py
LOG_LEVEL: str = "DEBUG"
```

---

## 🔮 Future Roadmap

### Phase 1: Forecasting (Q1 2025)
- [ ] Integrate Facebook Prophet for time series forecasting
- [ ] Monthly revenue predictions
- [ ] Cost trend analysis

### Phase 2: AI Classification (Q2 2025)
- [ ] OpenAI GPT integration for category classification
- [ ] Automatic categorization of new expense items
- [ ] RAG-based context using categories.json

### Phase 3: Dashboard (Q3 2025)
- [ ] Streamlit interactive dashboard
- [ ] Real-time data visualization
- [ ] Export to Excel/PDF reports

### Phase 4: Multi-Company Support (Q4 2025)
- [ ] Support for multiple company files
- [ ] Consolidated financial reporting
- [ ] Company comparison analytics

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Code Standards

- Follow **PEP 8** style guidelines
- Add **type hints** to all functions
- Write **docstrings** in Google style
- Include **unit tests** for new features
- Update **README** for user-facing changes

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

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

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/villarantonio/dre-financial-automation/issues)
- **Email**: villar_antonio@discente.ufg.br

---

<p align="center">
  Made with ❤️ for Brazilian Financial Automation
</p>

