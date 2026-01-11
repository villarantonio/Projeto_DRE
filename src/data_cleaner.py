"""
Módulo de Limpeza de Dados para Automação DRE.

Este módulo fornece funções para carregar, analisar e limpar
dados de DRE (Demonstração do Resultado do Exercício) de arquivos Excel e CSV.

Funções:
    load_dre_excel: Carrega arquivo Excel DRE com configuração adequada.
    load_dre_csv: Carrega arquivo CSV DRE com configuração adequada (legado).
    load_dre_file: Carrega arquivo DRE detectando formato automaticamente.
    convert_brazilian_currency: Converte strings de moeda brasileira para float.
    convert_month_to_date: Converte abreviações de meses em português para datetime.
"""

import logging
import re
from pathlib import Path
from typing import Union

import pandas as pd

import config

# Configura logger do módulo
logger = logging.getLogger(__name__)


def _validate_dre_dataframe(df: pd.DataFrame, file_path: Path) -> pd.DataFrame:
    """
    Valida o DataFrame carregado de arquivo DRE.

    Args:
        df: DataFrame carregado
        file_path: Caminho do arquivo fonte (para mensagens de erro)

    Returns:
        pd.DataFrame: DataFrame validado

    Raises:
        ValueError: Se o DataFrame estiver vazio ou sem colunas obrigatórias
    """
    # Valida se o DataFrame não está vazio
    if df.empty:
        logger.error("DataFrame carregado está vazio")
        raise ValueError("O arquivo não contém dados após o cabeçalho.")

    # Valida se as colunas obrigatórias existem
    missing_columns = [
        col for col in config.REQUIRED_COLUMNS if col not in df.columns
    ]
    if missing_columns:
        logger.error(f"Colunas obrigatórias ausentes: {missing_columns}")
        raise ValueError(
            f"Colunas obrigatórias ausentes no arquivo: {missing_columns}. "
            f"Colunas disponíveis: {df.columns.tolist()}"
        )

    logger.info(f"Carregados com sucesso {len(df)} registros com {len(df.columns)} colunas")
    return df


def load_dre_excel(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Carrega arquivo Excel DRE ignorando linhas de metadados.

    Esta função lê um arquivo Excel contendo dados DRE, pulando as primeiras
    4 linhas de metadados e usando a 5ª linha como cabeçalho.

    Args:
        file_path: Caminho para o arquivo Excel. Pode ser string ou objeto Path.

    Returns:
        pd.DataFrame: DataFrame contendo os dados DRE carregados.

    Raises:
        FileNotFoundError: Se o arquivo especificado não existir.
        ValueError: Se colunas obrigatórias estiverem ausentes.

    Exemplo:
        >>> df = load_dre_excel("DRE_BI.xlsx")
        >>> print(df.columns.tolist())
        ['Loja', '_key_centro_custo', 'cc_parent_nome', 'Nome Grupo', ...]
    """
    file_path = Path(file_path)

    # Valida se o arquivo existe
    if not file_path.exists():
        logger.error(f"Arquivo não encontrado: {file_path}")
        raise FileNotFoundError(f"Arquivo DRE não encontrado: {file_path}")

    if not file_path.is_file():
        logger.error(f"Caminho não é um arquivo: {file_path}")
        raise ValueError(f"Caminho não é um arquivo válido: {file_path}")

    logger.info(f"Carregando DRE Excel de: {file_path}")

    try:
        df = pd.read_excel(
            file_path,
            sheet_name=config.EXCEL_SHEET_NAME,
            header=config.EXCEL_HEADER_ROW,
            engine='openpyxl',  # Motor para arquivos .xlsx
        )
    except Exception as e:
        logger.error(f"Erro ao ler arquivo Excel: {e}")
        raise

    return _validate_dre_dataframe(df, file_path)


def load_dre_file(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Carrega arquivo DRE detectando o formato automaticamente.

    Suporta arquivos Excel (.xlsx, .xls) e CSV (.csv).
    Detecta o formato baseado na extensão do arquivo.

    Args:
        file_path: Caminho para o arquivo DRE.

    Returns:
        pd.DataFrame: DataFrame contendo os dados DRE carregados.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
        ValueError: Se o formato não for suportado ou colunas ausentes.

    Exemplo:
        >>> df = load_dre_file("DRE_BI.xlsx")  # Carrega Excel
        >>> df = load_dre_file("DRE_BI.csv")   # Carrega CSV
    """
    file_path = Path(file_path)
    extension = file_path.suffix.lower()

    if extension in ['.xlsx', '.xls']:
        logger.info(f"Formato Excel detectado: {extension}")
        return load_dre_excel(file_path)
    elif extension == '.csv':
        logger.info("Formato CSV detectado")
        return load_dre_csv(file_path)
    else:
        raise ValueError(
            f"Formato de arquivo não suportado: '{extension}'. "
            f"Use .xlsx, .xls ou .csv"
        )


def load_dre_csv(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Carrega arquivo CSV DRE ignorando linhas de metadados.

    Esta função lê um arquivo CSV contendo dados DRE, pulando as primeiras
    4 linhas de metadados e usando a 5ª linha como cabeçalho.

    Nota: Para novos projetos, prefira usar load_dre_excel() ou load_dre_file().

    Args:
        file_path: Caminho para o arquivo CSV. Pode ser string ou objeto Path.

    Returns:
        pd.DataFrame: DataFrame contendo os dados DRE carregados.

    Raises:
        FileNotFoundError: Se o arquivo especificado não existir.
        ValueError: Se colunas obrigatórias estiverem ausentes no CSV.
        pd.errors.EmptyDataError: Se o arquivo estiver vazio ou só com metadados.

    Exemplo:
        >>> df = load_dre_csv("DRE_BI(BaseDRE).csv")
        >>> print(df.columns.tolist())
        ['Loja', '_key_centro_custo', 'cc_parent_nome', 'Nome Grupo', ...]
    """
    file_path = Path(file_path)

    # Valida se o arquivo existe
    if not file_path.exists():
        logger.error(f"Arquivo não encontrado: {file_path}")
        raise FileNotFoundError(f"Arquivo DRE não encontrado: {file_path}")

    if not file_path.is_file():
        logger.error(f"Caminho não é um arquivo: {file_path}")
        raise ValueError(f"Caminho não é um arquivo válido: {file_path}")

    logger.info(f"Carregando DRE CSV de: {file_path}")

    try:
        df = pd.read_csv(
            file_path,
            sep=config.CSV_SEPARATOR,
            header=config.CSV_HEADER_ROW,
            encoding=config.CSV_ENCODING,
        )
    except pd.errors.EmptyDataError as e:
        logger.error(f"Arquivo vazio ou corrompido: {file_path}")
        raise pd.errors.EmptyDataError(
            f"O arquivo {file_path} está vazio ou contém apenas linhas de metadados."
        ) from e
    except Exception as e:
        logger.error(f"Erro ao ler arquivo CSV: {e}")
        raise

    return _validate_dre_dataframe(df, file_path)


def convert_brazilian_currency(value: str) -> float:
    """
    Convert Brazilian Portuguese currency string to float.

    This function handles the Brazilian currency format conversion,
    including handling of negative values, thousand separators (dots),
    and decimal separators (commas).

    Args:
        value: Currency string in Brazilian format (e.g., "R$ 1.234,56",
               "-R$ 1.234,56", "R$ 0,00").

    Returns:
        float: The numeric value as a Python float.

    Raises:
        ValueError: If the input is not a valid Brazilian currency format.
        TypeError: If the input is not a string.

    Examples:
        >>> convert_brazilian_currency("R$ 1.234,56")
        1234.56
        >>> convert_brazilian_currency("-R$ 1.234,56")
        -1234.56
        >>> convert_brazilian_currency("R$ 0,00")
        0.0
        >>> convert_brazilian_currency("R$ 63.713")
        63713.0
    """
    # Handle non-string types
    if not isinstance(value, str):
        if pd.isna(value):
            logger.warning("Received NaN/None value, returning 0.0")
            return 0.0
        raise TypeError(
            f"Expected string for currency conversion, got {type(value).__name__}: {value}"
        )
    
    # Strip whitespace
    value = value.strip()
    
    if not value:
        logger.warning("Received empty string, returning 0.0")
        return 0.0

    # Determine if value is negative
    is_negative = False
    if value.startswith("-"):
        is_negative = True
        value = value[1:].strip()

    # Remove "R$" prefix and any surrounding whitespace
    value = value.replace("R$", "").strip()

    # Check if value starts with "-" after removing R$ (alternative format)
    if value.startswith("-"):
        is_negative = True
        value = value[1:].strip()

    # Validate the remaining string contains only valid characters
    # Valid: digits, dots (thousand separator), comma (decimal separator)
    if not re.match(r'^[\d.,]+$', value):
        raise ValueError(
            f"Invalid currency format. Value contains invalid characters: '{value}'. "
            "Expected format: 'R$ 1.234,56' or '-R$ 1.234,56'"
        )

    # Remove thousand separators (dots)
    value = value.replace(".", "")

    # Replace decimal separator (comma) with dot
    value = value.replace(",", ".")

    try:
        result = float(value)
    except ValueError as e:
        raise ValueError(
            f"Could not convert '{value}' to float after formatting. "
            "Check if the currency format is correct."
        ) from e

    # Apply negative sign if needed
    if is_negative:
        result = -result

    return result


def convert_month_to_date(
    month_str: str,
    reference_year: int = config.REFERENCE_YEAR
) -> pd.Timestamp:
    """
    Convert Portuguese month abbreviation to a pandas Timestamp.

    This function converts Portuguese month abbreviations (e.g., "Jan", "Fev")
    to pandas Timestamp objects using the first day of the specified month
    and reference year.

    Args:
        month_str: Portuguese month abbreviation (e.g., "Jan", "Ago", "Dez").
        reference_year: Year to use for the date. Defaults to config.REFERENCE_YEAR.

    Returns:
        pd.Timestamp: Timestamp representing the first day of the specified month.

    Raises:
        ValueError: If the month abbreviation is not recognized.
        TypeError: If month_str is not a string.

    Examples:
        >>> convert_month_to_date("Ago", 2025)
        Timestamp('2025-08-01 00:00:00')
        >>> convert_month_to_date("Dez")
        Timestamp('2025-12-01 00:00:00')
    """
    if not isinstance(month_str, str):
        if pd.isna(month_str):
            logger.warning("Received NaN/None month value")
            raise ValueError("Month value cannot be NaN or None")
        raise TypeError(
            f"Expected string for month conversion, got {type(month_str).__name__}: {month_str}"
        )

    month_str = month_str.strip()

    if not month_str:
        raise ValueError("Month string cannot be empty")

    # Try to find the month in the mapping (case-sensitive first)
    month_num = config.MONTH_MAPPING.get(month_str)

    # If not found, try case-insensitive match
    if month_num is None:
        for key, value in config.MONTH_MAPPING.items():
            if key.lower() == month_str.lower():
                month_num = value
                break

    if month_num is None:
        valid_months = list(config.MONTH_MAPPING.keys())
        raise ValueError(
            f"Unknown month abbreviation: '{month_str}'. "
            f"Valid abbreviations are: {valid_months}"
        )

    try:
        timestamp = pd.Timestamp(year=reference_year, month=month_num, day=1)
    except Exception as e:
        raise ValueError(
            f"Could not create timestamp for month '{month_str}' and year {reference_year}: {e}"
        ) from e

    return timestamp


def apply_currency_conversion(df: pd.DataFrame, column: str = config.COLUMN_REALIZADO) -> pd.DataFrame:
    """
    Apply currency conversion to a DataFrame column.

    Args:
        df: DataFrame containing the column to convert.
        column: Name of the column containing Brazilian currency strings.

    Returns:
        pd.DataFrame: DataFrame with the converted column as float.

    Raises:
        KeyError: If the specified column does not exist.
        ValueError: If conversion fails for any value.
    """
    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found in DataFrame")

    logger.info(f"Converting currency values in column: {column}")
    df = df.copy()
    df[column] = df[column].apply(convert_brazilian_currency)
    logger.info(f"Successfully converted {len(df)} currency values")
    return df


def apply_month_conversion(
    df: pd.DataFrame,
    column: str = config.COLUMN_MES,
    reference_year: int = config.REFERENCE_YEAR
) -> pd.DataFrame:
    """
    Apply month conversion to a DataFrame column.

    Args:
        df: DataFrame containing the column to convert.
        column: Name of the column containing Portuguese month abbreviations.
        reference_year: Year to use for the date conversion.

    Returns:
        pd.DataFrame: DataFrame with the converted column as Timestamp.

    Raises:
        KeyError: If the specified column does not exist.
        ValueError: If conversion fails for any value.
    """
    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found in DataFrame")

    logger.info(f"Converting month values in column: {column}")
    df = df.copy()
    df[column] = df[column].apply(lambda x: convert_month_to_date(x, reference_year))
    logger.info(f"Successfully converted {len(df)} month values")
    return df

