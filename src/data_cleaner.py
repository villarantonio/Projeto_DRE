"""
Data Cleaning Module for DRE Financial Automation.

This module provides functions for loading, parsing, and cleaning
DRE (Demonstração do Resultado do Exercício) data from CSV files.

Functions:
    load_dre_csv: Load DRE CSV file with proper configuration.
    convert_brazilian_currency: Convert Brazilian currency strings to float.
    convert_month_to_date: Convert Portuguese month abbreviations to datetime.
"""

import logging
import re
from pathlib import Path
from typing import Union

import pandas as pd

import config

# Configure module logger
logger = logging.getLogger(__name__)


def load_dre_csv(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Load DRE CSV file ignoring metadata rows.

    This function reads a CSV file containing DRE data, skipping the first
    4 lines of metadata and using the 5th line as the header.

    Args:
        file_path: Path to the CSV file. Can be a string or Path object.

    Returns:
        pd.DataFrame: DataFrame containing the loaded DRE data with all columns.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If required columns are missing from the CSV.
        pd.errors.EmptyDataError: If the file is empty or contains only metadata.

    Example:
        >>> df = load_dre_csv("DRE_BI(BaseDRE).csv")
        >>> print(df.columns.tolist())
        ['Loja', '_key_centro_custo', 'cc_parent_nome', 'Nome Grupo', ...]
    """
    file_path = Path(file_path)
    
    # Validate file exists
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"DRE file not found: {file_path}")
    
    if not file_path.is_file():
        logger.error(f"Path is not a file: {file_path}")
        raise ValueError(f"Path is not a valid file: {file_path}")
    
    logger.info(f"Loading DRE CSV from: {file_path}")
    
    try:
        df = pd.read_csv(
            file_path,
            sep=config.CSV_SEPARATOR,
            header=config.CSV_HEADER_ROW,
            encoding=config.CSV_ENCODING,
        )
    except pd.errors.EmptyDataError as e:
        logger.error(f"Empty or corrupted file: {file_path}")
        raise pd.errors.EmptyDataError(
            f"The file {file_path} is empty or contains only metadata rows."
        ) from e
    except Exception as e:
        logger.error(f"Error reading CSV file: {e}")
        raise
    
    # Validate DataFrame is not empty
    if df.empty:
        logger.error("Loaded DataFrame is empty")
        raise ValueError("The CSV file contains no data rows after the header.")
    
    # Validate required columns exist
    missing_columns = [
        col for col in config.REQUIRED_COLUMNS if col not in df.columns
    ]
    if missing_columns:
        logger.error(f"Missing required columns: {missing_columns}")
        raise ValueError(
            f"Missing required columns in CSV: {missing_columns}. "
            f"Available columns: {df.columns.tolist()}"
        )
    
    logger.info(f"Successfully loaded {len(df)} records with {len(df.columns)} columns")
    return df


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

