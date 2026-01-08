"""
Main Orchestrator for DRE Financial Automation Project.

This script coordinates the data cleaning, transformation, and category
extraction pipeline for DRE (Demonstração do Resultado do Exercício) data.

Steps performed:
    1. Load the DRE CSV file with proper configuration
    2. Apply currency conversion to the Realizado column
    3. Apply month conversion to the Mês column
    4. Display DataFrame info and statistics for validation
    5. Extract and save category hierarchy
    6. Save processed data as Parquet file
    7. Print summary statistics
"""

import logging
import sys
from pathlib import Path

import pandas as pd

import config
from src.data_cleaner import (
    apply_currency_conversion,
    apply_month_conversion,
    load_dre_csv,
)
from src.category_engine import CategoryManager


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
) -> None:
    """
    Print processing summary statistics.

    Args:
        df: Processed DataFrame.
        categories: Extracted category hierarchy.
        category_manager: CategoryManager instance for summary generation.
    """
    print(f"\n{'='*60}")
    print("PROCESSING SUMMARY")
    print(f"{'='*60}")
    
    print(f"\n📊 Records Processed: {len(df):,}")
    print(f"📅 Reference Year: {config.REFERENCE_YEAR}")
    
    # Category summary
    summary = category_manager.get_category_summary(categories)
    print(f"\n📁 Category Statistics:")
    print(f"   - Macro Categories (Nome Grupo): {summary['total_groups']}")
    print(f"   - Detail Categories (cc_nome): {summary['total_details']}")
    
    print(f"\n📁 Categories by Group:")
    for group, count in summary["details_per_group"].items():
        print(f"   - {group}: {count} items")
    
    # Value statistics
    if config.COLUMN_REALIZADO in df.columns:
        total_value = df[config.COLUMN_REALIZADO].sum()
        positive_sum = df[df[config.COLUMN_REALIZADO] > 0][config.COLUMN_REALIZADO].sum()
        negative_sum = df[df[config.COLUMN_REALIZADO] < 0][config.COLUMN_REALIZADO].sum()
        
        print(f"\n💰 Financial Summary:")
        print(f"   - Total Value: R$ {total_value:,.2f}")
        print(f"   - Total Positive (Receitas): R$ {positive_sum:,.2f}")
        print(f"   - Total Negative (Custos): R$ {negative_sum:,.2f}")
    
    # Output files
    print(f"\n📄 Output Files:")
    print(f"   - Parquet: {config.PROCESSED_PARQUET_PATH}")
    print(f"   - Categories JSON: {config.CATEGORIES_JSON_PATH}")


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
        
        # Step 2: Load the DRE CSV file
        logger.info(f"Step 1: Loading DRE CSV from {config.INPUT_FILE_PATH}")
        df = load_dre_csv(config.INPUT_FILE_PATH)
        display_dataframe_info(df, "After Loading CSV")
        
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

        # Step 8: Print summary
        print_summary(df, categories, category_manager)

        logger.info("DRE Processing Pipeline completed successfully!")
        print(f"\n{'='*60}")
        print("✅ PIPELINE COMPLETED SUCCESSFULLY")
        print(f"{'='*60}\n")

        return 0

    except FileNotFoundError as e:
        logger.error(f"File not found error: {e}")
        print(f"\n❌ ERROR: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Value error during processing: {e}")
        print(f"\n❌ ERROR: {e}")
        return 1
    except Exception as e:
        logger.exception(f"Unexpected error during processing: {e}")
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

