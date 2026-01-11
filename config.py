"""
Configuration module for DRE Financial Automation Project.

This module contains all configurable parameters for the project,
including file paths, reference year, and other settings.
"""

from pathlib import Path

# =============================================================================
# File Paths Configuration
# =============================================================================

# Base directory (project root)
BASE_DIR: Path = Path(__file__).parent

# Input file configuration
INPUT_FILE_NAME: str = "DRE_BI(BaseDRE).csv"
INPUT_FILE_PATH: Path = BASE_DIR / INPUT_FILE_NAME

# Output files configuration
OUTPUT_DIR: Path = BASE_DIR / "output"
PROCESSED_PARQUET_PATH: Path = OUTPUT_DIR / "processed_dre.parquet"
CATEGORIES_JSON_PATH: Path = OUTPUT_DIR / "categories.json"
NARRATIVE_CSV_PATH: Path = OUTPUT_DIR / "relatorio_narrativo_ia.csv"

# =============================================================================
# Data Processing Configuration
# =============================================================================

# CSV parsing settings
CSV_SEPARATOR: str = ";"
CSV_ENCODING: str = "latin-1"  # Also known as ISO-8859-1 or Windows-1252
CSV_HEADER_ROW: int = 4  # 0-indexed, actual header is at line 5

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
TEXT_REPLACEMENTS: dict[str, str] = {
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
    "Ã§": "ç",  # UTF-8 mojibake for cedilla
    "Ã£": "ã",  # UTF-8 mojibake for a-tilde
    "Ã©": "é",  # UTF-8 mojibake for e-acute
    "Ã¡": "á",  # UTF-8 mojibake for a-acute
    "Ã³": "ó",  # UTF-8 mojibake for o-acute
    "Ãº": "ú",  # UTF-8 mojibake for u-acute
}

# =============================================================================
# Logging Configuration
# =============================================================================

LOG_LEVEL: str = "INFO"
LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

