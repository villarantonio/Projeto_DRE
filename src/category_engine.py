"""
Category Engine Module for DRE Financial Automation.

This module provides a CategoryManager class for extracting and managing
the hierarchy of financial categories from DRE data. The extracted hierarchy
can be used as context for future LLM-based classification.

Classes:
    CategoryManager: Manages extraction and persistence of category hierarchies.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Union

import pandas as pd

import config

# Configure module logger
logger = logging.getLogger(__name__)


class CategoryManager:
    """
    Manager class for DRE category hierarchy extraction and persistence.

    This class provides methods to extract unique category hierarchies from
    DRE DataFrames and save them as JSON for future use in LLM classification.

    Attributes:
        group_column: Name of the column containing macro categories (Nome Grupo).
        detail_column: Name of the column containing detailed categories (cc_nome).

    Example:
        >>> manager = CategoryManager()
        >>> df = load_dre_csv("DRE_BI(BaseDRE).csv")
        >>> categories = manager.extract_category_hierarchy(df)
        >>> manager.save_categories_json(categories, "categories.json")
    """

    def __init__(
        self,
        group_column: str = config.COLUMN_NOME_GRUPO,
        detail_column: str = config.COLUMN_CC_NOME,
    ) -> None:
        """
        Initialize the CategoryManager.

        Args:
            group_column: Name of the column containing macro categories.
                         Defaults to config.COLUMN_NOME_GRUPO.
            detail_column: Name of the column containing detailed categories.
                          Defaults to config.COLUMN_CC_NOME.
        """
        self.group_column = group_column
        self.detail_column = detail_column
        logger.info(
            f"CategoryManager initialized with group_column='{group_column}', "
            f"detail_column='{detail_column}'"
        )

    def extract_category_hierarchy(
        self, df: pd.DataFrame
    ) -> Dict[str, List[str]]:
        """
        Extract unique category hierarchy from a DRE DataFrame.

        This method reads the DataFrame and creates a dictionary where keys
        are the macro categories (Nome Grupo) and values are lists of unique
        detailed categories (cc_nome) belonging to each group.

        Args:
            df: DataFrame containing DRE data with group and detail columns.

        Returns:
            Dict[str, List[str]]: Dictionary mapping macro categories to lists
                of unique detailed categories. Example:
                {
                    "RECEITAS S/ VENDAS": ["DINHEIRO", "IFOOD", "PIX"],
                    "CUSTOS VARIÁVEIS": ["AÇOUGUE", "CARVÃO"]
                }

        Raises:
            ValueError: If required columns are missing from the DataFrame.
            TypeError: If df is not a pandas DataFrame.

        Example:
            >>> categories = manager.extract_category_hierarchy(df)
            >>> print(categories["RECEITAS S/ VENDAS"])
            ['DINHEIRO', 'IFOOD', 'PIX', 'TED/DOC', ...]
        """
        # Validate input type
        if not isinstance(df, pd.DataFrame):
            raise TypeError(
                f"Expected pandas DataFrame, got {type(df).__name__}"
            )

        # Validate required columns exist
        missing_columns = []
        if self.group_column not in df.columns:
            missing_columns.append(self.group_column)
        if self.detail_column not in df.columns:
            missing_columns.append(self.detail_column)

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {missing_columns}. "
                f"Available columns: {df.columns.tolist()}"
            )

        logger.info("Extracting category hierarchy from DataFrame")

        # Extract unique hierarchy
        hierarchy: Dict[str, List[str]] = {}

        # Group by macro category and get unique detailed categories
        grouped = df.groupby(self.group_column)[self.detail_column].unique()

        for group_name, detail_values in grouped.items():
            # Convert numpy array to sorted list and ensure all values are strings
            unique_details = sorted([
                str(val) for val in detail_values if pd.notna(val)
            ])
            hierarchy[str(group_name)] = unique_details

        # Sort by group name for consistent output
        hierarchy = dict(sorted(hierarchy.items()))

        logger.info(
            f"Extracted {len(hierarchy)} macro categories with "
            f"{sum(len(v) for v in hierarchy.values())} unique detail categories"
        )

        return hierarchy

    def save_categories_json(
        self,
        categories: Dict[str, List[str]],
        output_path: Union[str, Path],
    ) -> None:
        """
        Save category hierarchy to a JSON file.

        This method saves the extracted category hierarchy as a formatted JSON
        file, which can be used as context for future LLM classification.

        Args:
            categories: Dictionary mapping macro categories to detail lists.
            output_path: Path where the JSON file will be saved.

        Raises:
            ValueError: If categories is empty or invalid.
            TypeError: If categories is not a dictionary.
            IOError: If the file cannot be written.
        """
        # Validate input
        if not isinstance(categories, dict):
            raise TypeError(
                f"Expected dictionary for categories, got {type(categories).__name__}"
            )

        if not categories:
            raise ValueError("Categories dictionary cannot be empty")

        output_path = Path(output_path)

        # Create parent directories if they don't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Saving categories to: {output_path}")

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(
                    categories,
                    f,
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
        except IOError as e:
            logger.error(f"Failed to write categories file: {e}")
            raise IOError(f"Could not write categories to {output_path}: {e}") from e

        logger.info(
            f"Successfully saved {len(categories)} categories to {output_path}"
        )

    def load_categories_json(
        self, input_path: Union[str, Path]
    ) -> Dict[str, List[str]]:
        """
        Load category hierarchy from a JSON file.

        Args:
            input_path: Path to the JSON file containing categories.

        Returns:
            Dict[str, List[str]]: Dictionary mapping macro categories to detail lists.

        Raises:
            FileNotFoundError: If the file does not exist.
            json.JSONDecodeError: If the file contains invalid JSON.
        """
        input_path = Path(input_path)

        if not input_path.exists():
            raise FileNotFoundError(f"Categories file not found: {input_path}")

        logger.info(f"Loading categories from: {input_path}")

        with open(input_path, "r", encoding="utf-8") as f:
            categories = json.load(f)

        logger.info(f"Loaded {len(categories)} categories from {input_path}")
        return categories

    def get_category_summary(
        self, categories: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Generate a summary of the category hierarchy.

        Args:
            categories: Dictionary mapping macro categories to detail lists.

        Returns:
            Dict[str, Any]: Summary statistics including:
                - total_groups: Number of macro categories
                - total_details: Total number of detail categories
                - groups: List of macro category names
                - details_per_group: Dict mapping group names to detail count
        """
        summary = {
            "total_groups": len(categories),
            "total_details": sum(len(v) for v in categories.values()),
            "groups": list(categories.keys()),
            "details_per_group": {k: len(v) for k, v in categories.items()},
        }
        return summary

