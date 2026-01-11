"""
Narrative Generator Module for DRE Financial Automation Project.

This module generates natural language narratives from financial data,
transforming structured DRE data into human-readable descriptions
suitable for AI/LLM processing and reporting.

Author: Luccas Jose (original), refactored for integration
"""

import logging
import sys
from pathlib import Path
from typing import Any

import pandas as pd

# Import from parent package when running as module
try:
    import config
except ImportError:
    # Fallback for direct execution
    sys.path.insert(0, str(Path(__file__).parent.parent))
    import config


logger = logging.getLogger(__name__)


def clean_text(text: Any) -> Any:
    """
    Clean corrupted characters common in Brazilian CSV exports.

    Args:
        text: Text to clean, or any other value (passed through unchanged).

    Returns:
        Cleaned text if input was string, otherwise original value.
    """
    if not isinstance(text, str):
        return text

    for error, fix in config.TEXT_REPLACEMENTS.items():
        text = text.replace(error, fix)

    return text.strip()


def create_narrative(row: pd.Series) -> str:
    """
    Transform a data row into a natural language narrative.

    Args:
        row: Pandas Series representing a single row of financial data.

    Returns:
        A natural language description of the financial record.
    """
    try:
        # Get values safely (handles missing columns)
        mes = row.get(config.COLUMN_MES, "N/D")
        grupo = row.get(config.COLUMN_NOME_GRUPO, "Categoria Desconhecida")
        item = row.get(config.COLUMN_CC_NOME, "Item Desconhecido")
        valor = row.get(config.COLUMN_REALIZADO, "0")
        subcat = row.get("Camada03", "")

        # Format value if it's a number
        if isinstance(valor, (int, float)):
            valor_str = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            valor_str = str(valor)

        # Build the narrative
        narrativa = (
            f"Em {mes}, o grupo '{grupo}' registrou um valor de {valor_str} "
            f"referente ao item '{item}'"
        )

        if subcat and subcat != item:
            narrativa += f" (Subcategoria: {subcat})."
        else:
            narrativa += "."

        return narrativa
    except Exception as e:
        logger.warning(f"Error creating narrative for row: {e}")
        return ""


def generate_narratives(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate narratives for all rows in a DataFrame.

    This is the main function to be called from the pipeline.
    It adds a 'Narrativa_IA' column to the DataFrame.

    Args:
        df: DataFrame with financial data (must have required columns).

    Returns:
        DataFrame with added 'Narrativa_IA' column.
    """
    logger.info("Generating narratives for financial data...")

    # Create a copy to avoid modifying the original
    df_with_narratives = df.copy()

    # Generate narratives
    df_with_narratives["Narrativa_IA"] = df_with_narratives.apply(create_narrative, axis=1)

    # Count successful narratives
    successful = df_with_narratives["Narrativa_IA"].str.len() > 0
    logger.info(f"Generated {successful.sum()} narratives from {len(df)} records")

    return df_with_narratives


def save_narrative_report(
    df: pd.DataFrame,
    output_path: Path | str | None = None,
) -> Path:
    """
    Save narrative report to CSV file.

    Args:
        df: DataFrame with 'Narrativa_IA' column.
        output_path: Optional custom output path. Defaults to config.NARRATIVE_CSV_PATH.

    Returns:
        Path to the saved file.

    Raises:
        ValueError: If DataFrame doesn't have 'Narrativa_IA' column.
    """
    if "Narrativa_IA" not in df.columns:
        raise ValueError("DataFrame must have 'Narrativa_IA' column. Run generate_narratives() first.")

    output_path = Path(output_path) if output_path else config.NARRATIVE_CSV_PATH

    # Select columns for the report
    cols_to_keep = [
        "Narrativa_IA",
        config.COLUMN_MES,
        config.COLUMN_NOME_GRUPO,
        config.COLUMN_CC_NOME,
        config.COLUMN_REALIZADO,
    ]
    cols_final = [c for c in cols_to_keep if c in df.columns]

    df_final = df[cols_final]

    # Save with proper encoding for Brazilian Portuguese
    df_final.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig",  # UTF-8 with BOM for Excel compatibility
        sep=config.CSV_SEPARATOR,
    )

    logger.info(f"Narrative report saved to {output_path} ({len(df_final)} records)")

    return output_path


def get_narrative_summary(df: pd.DataFrame) -> dict:
    """
    Generate summary statistics for narrative report.

    Args:
        df: DataFrame with 'Narrativa_IA' column.

    Returns:
        Dictionary with summary statistics.
    """
    if "Narrativa_IA" not in df.columns:
        return {"error": "No narratives generated"}

    narratives = df["Narrativa_IA"]

    return {
        "total_records": len(df),
        "narratives_generated": (narratives.str.len() > 0).sum(),
        "empty_narratives": (narratives.str.len() == 0).sum(),
        "avg_narrative_length": narratives.str.len().mean(),
        "unique_groups": df[config.COLUMN_NOME_GRUPO].nunique() if config.COLUMN_NOME_GRUPO in df.columns else 0,
    }


# Standalone execution support
if __name__ == "__main__":
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format=config.LOG_FORMAT,
    )

    print("--- Iniciando Gerador de Narrativas (Standalone) ---")

    if not config.INPUT_FILE_PATH.exists():
        print(f"ERRO: Arquivo de entrada '{config.INPUT_FILE_PATH}' não encontrado.")
        sys.exit(1)

    try:
        # Load CSV
        df = pd.read_csv(
            config.INPUT_FILE_PATH,
            sep=config.CSV_SEPARATOR,
            header=config.CSV_HEADER_ROW,
            encoding=config.CSV_ENCODING,
        )

        # Clean columns
        df = df.dropna(how="all", axis=1)
        df.columns = [clean_text(col) for col in df.columns]

        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].apply(clean_text)

        # Filter invalid rows
        if "Loja" in df.columns:
            df = df[df["Loja"].notna()]

        # Generate and save
        df = generate_narratives(df)
        output_path = save_narrative_report(df)

        summary = get_narrative_summary(df)
        print(f"\n✅ Sucesso! Arquivo '{output_path}' gerado.")
        print(f"   - Total de registros: {summary['total_records']}")
        print(f"   - Narrativas geradas: {summary['narratives_generated']}")

    except Exception as e:
        print(f"Erro fatal: {e}")
        sys.exit(1)