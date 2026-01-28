"""
Módulo de configuração para o Projeto de Automação DRE.

Este módulo contém todos os parâmetros configuráveis do projeto,
incluindo caminhos de arquivos, ano de referência e outras configurações.

Suporta arquivos de entrada nos formatos Excel (.xlsx) e CSV (.csv).
"""

from pathlib import Path

# =============================================================================
# Configuração de Caminhos de Arquivos
# =============================================================================

# Diretório base (raiz do projeto)
BASE_DIR: Path = Path(__file__).parent

# Configuração do arquivo de entrada
# Suporta tanto Excel (.xlsx) quanto CSV (.csv)
# O arquivo pode ser baixado do SharePoint da empresa Manda Picanha
INPUT_FILE_NAME: str = "DRE_BI(BaseDRE).csv"
INPUT_FILE_PATH: Path = BASE_DIR / INPUT_FILE_NAME

# Configuração de arquivos de saída
OUTPUT_DIR: Path = BASE_DIR / "output"
PROCESSED_PARQUET_PATH: Path = OUTPUT_DIR / "processed_dre.parquet"
CATEGORIES_JSON_PATH: Path = OUTPUT_DIR / "categories.json"
NARRATIVE_CSV_PATH: Path = OUTPUT_DIR / "relatorio_narrativo_ia.csv"

# =============================================================================
# Configuração de Processamento de Dados
# =============================================================================

# Configurações para arquivos Excel (.xlsx)
# Nota: Para Excel, encoding e separador não são necessários
EXCEL_HEADER_ROW: int = 4  # Índice 0, cabeçalho real está na linha 5
EXCEL_SHEET_NAME: str | int = 0  # Nome ou índice da planilha (0 = primeira)

# Configurações para arquivos CSV (mantidas para compatibilidade)
CSV_SEPARATOR: str = ";"
CSV_ENCODING: str = "latin-1"  # Também conhecido como ISO-8859-1 ou Windows-1252
CSV_HEADER_ROW: int = 4  # Índice 0, cabeçalho real está na linha 5

# Reference year for date conversion
REFERENCE_YEAR: int = 2025

# =============================================================================
# Column Names Configuration
# =============================================================================

# Expected column names in the CSV
COLUMN_NOME_GRUPO: str = "Nome Grupo"
COLUMN_CC_NOME: str = "cc_nome"
COLUMN_MES: str = "Mês"
COLUMN_REALIZADO: str = "Realizado"

# Required columns for processing
REQUIRED_COLUMNS: list[str] = [
    COLUMN_NOME_GRUPO,
    COLUMN_CC_NOME,
    COLUMN_MES,
    COLUMN_REALIZADO,
]

# =============================================================================
# Portuguese Month Mapping
# =============================================================================

MONTH_MAPPING: dict[str, int] = {
    "Jan": 1,
    "Fev": 2,
    "Mar": 3,
    "Abr": 4,
    "Mai": 5,
    "Jun": 6,
    "Jul": 7,
    "Ago": 8,
    "Set": 9,
    "Out": 10,
    "Nov": 11,
    "Dez": 12,
}

# =============================================================================
# Text Cleaning Configuration (for narrative generator)
# =============================================================================

# Common encoding errors in Brazilian CSV exports and their corrections
# Note: The corrupted cedilla character may appear as different bytes depending on encoding
# The ï¿½ character is the Unicode replacement character (U+FFFD) from failed decoding
TEXT_REPLACEMENTS: dict[str, str] = {
    # Specific patterns found in DRE data (ï¿½ = U+FFFD replacement character)
    "VARIï¿½VEIS": "VARIÁVEIS",
    "DEDUï¿½ï¿½ES": "DEDUÇÕES",
    "SERVIï¿½OS": "SERVIÇOS",
    "Sï¿½CIOS": "SÓCIOS",
    "Sï¿½cios": "Sócios",
    # Generic word fixes (missing accents)
    "Vrios": "Vários",
    "Ms": "Mês",
    "VARIVEIS": "VARIÁVEIS",
    "DEDUES": "DEDUÇÕES",
    "SERVIOS": "SERVIÇOS",
    "CACHAA": "CACHAÇA",
    "ALCLICAS": "ALCOÓLICAS",
    "FRIAS": "FÉRIAS",
    "SALRIO": "SALÁRIO",
    "RESCISES": "RESCISÕES",
    # UTF-8 mojibake patterns (double-encoding issues)
    "Ã§": "ç",
    "Ã£": "ã",
    "Ã©": "é",
    "Ã¡": "á",
    "Ã³": "ó",
    "Ãº": "ú",
    "Ã­": "í",
    "Ãµ": "õ",
    # Fallback: remove replacement character if still present
    "ï¿½": "",
}

# =============================================================================
# Logging Configuration
# =============================================================================

LOG_LEVEL: str = "INFO"
LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

