"""
DRE Financial Automation Source Package.

This package contains modules for data cleaning, category management,
narrative generation, and financial data processing for DRE
(Demonstração do Resultado do Exercício).
"""

from src.data_cleaner import (
    load_dre_csv,
    convert_brazilian_currency,
    convert_month_to_date,
)
from src.category_engine import CategoryManager
from src.narrative_generator import (
    generate_narratives,
    save_narrative_report,
    get_narrative_summary,
    clean_text,
    create_narrative,
)

__all__ = [
    # Data cleaner
    "load_dre_csv",
    "convert_brazilian_currency",
    "convert_month_to_date",
    # Category engine
    "CategoryManager",
    # Narrative generator
    "generate_narratives",
    "save_narrative_report",
    "get_narrative_summary",
    "clean_text",
    "create_narrative",
]

