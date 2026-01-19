"""
Orquestrador Principal do Projeto de Automação DRE.

Este script coordena o pipeline de limpeza, transformação e extração
de categorias de dados DRE (Demonstração do Resultado do Exercício).

Suporta arquivos de entrada nos formatos Excel (.xlsx) e CSV (.csv).

Etapas executadas:
    1. Carregar arquivo DRE (Excel ou CSV) com configuração adequada
    2. Aplicar conversão de moeda na coluna Realizado
    3. Aplicar conversão de mês na coluna Mês
    4. Exibir informações e estatísticas do DataFrame para validação
    5. Extrair e salvar hierarquia de categorias
    6. Salvar dados processados como arquivo Parquet
    7. Gerar narrativas para treinamento de IA
    8. Imprimir estatísticas resumidas
"""

import logging
import sys
from pathlib import Path

import pandas as pd

import config
from src.data_cleaner import (
    apply_currency_conversion,
    apply_month_conversion,
    load_dre_file,
)
from src.category_engine import CategoryManager
from src.narrative_generator import (
    generate_narratives,
    save_narrative_report,
    get_narrative_summary,
)


def setup_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format=config.LOG_FORMAT,
        datefmt=config.LOG_DATE_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )


def ensure_output_directory() -> None:
    """Create output directory if it doesn't exist."""
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logging.info(f"Output directory ready: {config.OUTPUT_DIR}")


def display_dataframe_info(df: pd.DataFrame, stage: str = "") -> None:
    """
    Display DataFrame information for validation.

    Args:
        df: DataFrame to display information about.
        stage: Description of the current processing stage.
    """
    if stage:
        print(f"\n{'='*60}")
        print(f"DataFrame Info - {stage}")
        print(f"{'='*60}")
    
    print("\n--- DataFrame Info ---")
    df.info()
    
    print("\n--- DataFrame Description ---")
    print(df.describe(include="all"))
    
    print("\n--- First 5 Rows ---")
    print(df.head())


def print_summary(
    df: pd.DataFrame,
    categories: dict,
    category_manager: CategoryManager,
    narrative_summary: dict | None = None,
) -> None:
    """
    Print processing summary statistics.

    Args:
        df: Processed DataFrame.
        categories: Extracted category hierarchy.
        category_manager: CategoryManager instance for summary generation.
        narrative_summary: Optional summary from narrative generator.
    """
    print(f"\n{'='*60}")
    print("RESUMO DO PROCESSAMENTO")
    print(f"{'='*60}")

    print(f"\n[*] Registros Processados: {len(df):,}")
    print(f"[*] Ano de Referencia: {config.REFERENCE_YEAR}")

    # Category summary
    summary = category_manager.get_category_summary(categories)
    print(f"\n[*] Estatisticas de Categorias:")
    print(f"   - Categorias Macro (Nome Grupo): {summary['total_groups']}")
    print(f"   - Categorias Detalhadas (cc_nome): {summary['total_details']}")

    print(f"\n[*] Categorias por Grupo:")
    for group, count in summary["details_per_group"].items():
        print(f"   - {group}: {count} itens")

    # Value statistics
    if config.COLUMN_REALIZADO in df.columns:
        total_value = df[config.COLUMN_REALIZADO].sum()
        positive_sum = df[df[config.COLUMN_REALIZADO] > 0][config.COLUMN_REALIZADO].sum()
        negative_sum = df[df[config.COLUMN_REALIZADO] < 0][config.COLUMN_REALIZADO].sum()

        print(f"\n[*] Resumo Financeiro:")
        print(f"   - Valor Total: R$ {total_value:,.2f}")
        print(f"   - Total Positivo (Receitas): R$ {positive_sum:,.2f}")
        print(f"   - Total Negativo (Custos): R$ {negative_sum:,.2f}")

    # Narrative summary
    if narrative_summary:
        print(f"\n[*] Narrativas para IA:")
        print(f"   - Narrativas Geradas: {narrative_summary.get('narratives_generated', 0)}")
        print(f"   - Tamanho Medio: {narrative_summary.get('avg_narrative_length', 0):.0f} caracteres")

    # Output files
    print(f"\n[*] Arquivos de Saida:")
    print(f"   - Parquet: {config.PROCESSED_PARQUET_PATH}")
    print(f"   - Categorias JSON: {config.CATEGORIES_JSON_PATH}")
    print(f"   - Narrativas CSV: {config.NARRATIVE_CSV_PATH}")


def main() -> int:
    """
    Main entry point for the DRE processing pipeline.

    Returns:
        int: Exit code (0 for success, 1 for failure).
    """
    # Setup
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting DRE Financial Automation Pipeline")
    print(f"\n{'='*60}")
    print("DRE FINANCIAL AUTOMATION PIPELINE")
    print(f"{'='*60}")
    
    try:
        # Step 1: Ensure output directory exists
        ensure_output_directory()

        # Step 2: Load the DRE file (Excel or CSV - auto-detected)
        logger.info(f"Step 1: Loading DRE file from {config.INPUT_FILE_PATH}")
        df = load_dre_file(config.INPUT_FILE_PATH)
        display_dataframe_info(df, "After Loading File")
        
        # Step 3: Apply currency conversion
        logger.info("Step 2: Applying currency conversion to Realizado column")
        df = apply_currency_conversion(df, config.COLUMN_REALIZADO)
        
        # Step 4: Apply month conversion
        logger.info("Step 3: Applying month conversion to Mês column")
        df = apply_month_conversion(df, config.COLUMN_MES, config.REFERENCE_YEAR)
        
        display_dataframe_info(df, "After Data Transformations")
        
        # Step 5: Extract category hierarchy
        logger.info("Step 4: Extracting category hierarchy")
        category_manager = CategoryManager()
        categories = category_manager.extract_category_hierarchy(df)

        # Step 6: Save processed DataFrame as Parquet
        logger.info(f"Step 5: Saving processed data to {config.PROCESSED_PARQUET_PATH}")
        df.to_parquet(config.PROCESSED_PARQUET_PATH, engine="pyarrow", index=False)
        logger.info(f"Parquet file saved: {config.PROCESSED_PARQUET_PATH}")

        # Step 7: Save category hierarchy as JSON
        logger.info(f"Step 6: Saving categories to {config.CATEGORIES_JSON_PATH}")
        category_manager.save_categories_json(categories, config.CATEGORIES_JSON_PATH)

        # Step 8: Generate AI narratives
        logger.info("Step 7: Generating AI narratives")
        df = generate_narratives(df)
        save_narrative_report(df)
        narrative_summary = get_narrative_summary(df)

        # Step 9: Print summary
        print_summary(df, categories, category_manager, narrative_summary)

        logger.info("DRE Processing Pipeline completed successfully!")
        print(f"\n{'='*60}")
        print("[OK] PIPELINE COMPLETED SUCCESSFULLY")
        print(f"{'='*60}\n")

        return 0

    except FileNotFoundError as e:
        logger.error(f"File not found error: {e}")
        print(f"\n[ERROR] {e}")
        return 1
    except ValueError as e:
        logger.error(f"Value error during processing: {e}")
        print(f"\n[ERROR] {e}")
        return 1
    except Exception as e:
        logger.exception(f"Unexpected error during processing: {e}")
        print(f"\n[ERROR] UNEXPECTED: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

