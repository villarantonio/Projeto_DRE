"""
DRE Financial Automation Source Package.

This package contains modules for data cleaning, category management,
and financial data processing for DRE (Demonstração do Resultado do Exercício).
"""

from src.data_cleaner import (
    load_dre_csv,
    convert_brazilian_currency,
    convert_month_to_date,
)
from src.category_engine import CategoryManager

__all__ = [
    "load_dre_csv",
    "convert_brazilian_currency",
    "convert_month_to_date",
    "CategoryManager",
]

