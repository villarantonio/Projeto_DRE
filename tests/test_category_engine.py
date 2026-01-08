"""
Unit tests for the category_engine module.

Tests cover CategoryManager class functionality for hierarchy extraction
and JSON persistence.
"""

import json
import os
import tempfile
from pathlib import Path

import pandas as pd
import pytest

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.category_engine import CategoryManager


class TestCategoryManager:
    """Tests for the CategoryManager class."""

    @pytest.fixture
    def sample_dataframe(self) -> pd.DataFrame:
        """Create a sample DataFrame for testing."""
        return pd.DataFrame({
            "Nome Grupo": [
                "RECEITAS S/ VENDAS",
                "RECEITAS S/ VENDAS",
                "RECEITAS S/ VENDAS",
                "( - ) CUSTOS VARIÁVEIS",
                "( - ) CUSTOS VARIÁVEIS",
            ],
            "cc_nome": [
                "DINHEIRO",
                "IFOOD",
                "PIX",
                "BOVINOS",
                "AVES",
            ],
            "Mês": ["Ago", "Set", "Out", "Nov", "Dez"],
            "Realizado": [1000.0, 2000.0, 1500.0, -500.0, -300.0],
        })

    @pytest.fixture
    def category_manager(self) -> CategoryManager:
        """Create a CategoryManager instance for testing."""
        return CategoryManager()

    def test_extract_category_hierarchy(
        self, category_manager: CategoryManager, sample_dataframe: pd.DataFrame
    ):
        """Test extraction of category hierarchy."""
        hierarchy = category_manager.extract_category_hierarchy(sample_dataframe)

        assert len(hierarchy) == 2
        assert "RECEITAS S/ VENDAS" in hierarchy
        assert "( - ) CUSTOS VARIÁVEIS" in hierarchy
        assert sorted(hierarchy["RECEITAS S/ VENDAS"]) == ["DINHEIRO", "IFOOD", "PIX"]
        assert sorted(hierarchy["( - ) CUSTOS VARIÁVEIS"]) == ["AVES", "BOVINOS"]

    def test_extract_hierarchy_empty_dataframe(self, category_manager: CategoryManager):
        """Test extraction from empty DataFrame."""
        empty_df = pd.DataFrame(columns=["Nome Grupo", "cc_nome"])
        hierarchy = category_manager.extract_category_hierarchy(empty_df)
        assert hierarchy == {}

    def test_extract_hierarchy_missing_column_raises_error(
        self, category_manager: CategoryManager
    ):
        """Test that missing columns raise ValueError."""
        df = pd.DataFrame({"Nome Grupo": ["A", "B"]})
        with pytest.raises(ValueError, match="Missing required columns"):
            category_manager.extract_category_hierarchy(df)

    def test_extract_hierarchy_invalid_input_type(
        self, category_manager: CategoryManager
    ):
        """Test that non-DataFrame input raises TypeError."""
        with pytest.raises(TypeError, match="Expected pandas DataFrame"):
            category_manager.extract_category_hierarchy("not a dataframe")

    def test_save_categories_json(
        self, category_manager: CategoryManager, sample_dataframe: pd.DataFrame
    ):
        """Test saving categories to JSON file."""
        hierarchy = category_manager.extract_category_hierarchy(sample_dataframe)

        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.json', delete=False
        ) as f:
            temp_path = f.name

        try:
            category_manager.save_categories_json(hierarchy, temp_path)

            # Verify file was created and contains valid JSON
            with open(temp_path, 'r', encoding='utf-8') as f:
                loaded = json.load(f)

            assert loaded == hierarchy
        finally:
            os.unlink(temp_path)

    def test_save_empty_categories_raises_error(
        self, category_manager: CategoryManager
    ):
        """Test that saving empty categories raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            category_manager.save_categories_json({}, "output.json")

    def test_save_invalid_type_raises_error(
        self, category_manager: CategoryManager
    ):
        """Test that saving non-dict raises TypeError."""
        with pytest.raises(TypeError, match="Expected dictionary"):
            category_manager.save_categories_json(["not", "a", "dict"], "output.json")

    def test_load_categories_json(
        self, category_manager: CategoryManager, sample_dataframe: pd.DataFrame
    ):
        """Test loading categories from JSON file."""
        hierarchy = category_manager.extract_category_hierarchy(sample_dataframe)

        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.json', delete=False
        ) as f:
            json.dump(hierarchy, f)
            temp_path = f.name

        try:
            loaded = category_manager.load_categories_json(temp_path)
            assert loaded == hierarchy
        finally:
            os.unlink(temp_path)

    def test_load_nonexistent_file_raises_error(
        self, category_manager: CategoryManager
    ):
        """Test that loading nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            category_manager.load_categories_json("nonexistent.json")

    def test_get_category_summary(
        self, category_manager: CategoryManager, sample_dataframe: pd.DataFrame
    ):
        """Test category summary generation."""
        hierarchy = category_manager.extract_category_hierarchy(sample_dataframe)
        summary = category_manager.get_category_summary(hierarchy)

        assert summary["total_groups"] == 2
        assert summary["total_details"] == 5
        assert "RECEITAS S/ VENDAS" in summary["groups"]
        assert summary["details_per_group"]["RECEITAS S/ VENDAS"] == 3
        assert summary["details_per_group"]["( - ) CUSTOS VARIÁVEIS"] == 2

    def test_duplicate_values_are_deduplicated(self, category_manager: CategoryManager):
        """Test that duplicate cc_nome values are deduplicated."""
        df = pd.DataFrame({
            "Nome Grupo": ["GROUP_A", "GROUP_A", "GROUP_A"],
            "cc_nome": ["ITEM_1", "ITEM_1", "ITEM_2"],
        })
        hierarchy = category_manager.extract_category_hierarchy(df)
        assert hierarchy["GROUP_A"] == ["ITEM_1", "ITEM_2"]

