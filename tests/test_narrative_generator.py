"""
Unit tests for the narrative_generator module.

Tests cover text cleaning, narrative creation, and report generation.
"""

import pytest
import pandas as pd
from pathlib import Path
import tempfile
import os

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.narrative_generator import (
    clean_text,
    create_narrative,
    generate_narratives,
    save_narrative_report,
    get_narrative_summary,
)
import config


class TestCleanText:
    """Tests for the clean_text function."""

    def test_clean_varios(self):
        """Test cleaning of 'Vrios' to 'Vários'."""
        assert clean_text("Vrios") == "Vários"

    def test_clean_mes(self):
        """Test cleaning of 'Ms' to 'Mês'."""
        assert clean_text("Ms") == "Mês"

    def test_clean_variveis(self):
        """Test cleaning of 'VARIVEIS' to 'VARIÁVEIS'."""
        assert clean_text("VARIVEIS") == "VARIÁVEIS"

    def test_clean_dedues(self):
        """Test cleaning of 'DEDUES' to 'DEDUÇÕES'."""
        assert clean_text("DEDUES") == "DEDUÇÕES"

    def test_clean_mojibake_cedilla(self):
        """Test cleaning of UTF-8 mojibake cedilla."""
        assert clean_text("Ã§") == "ç"

    def test_non_string_passthrough(self):
        """Test that non-string values pass through unchanged."""
        assert clean_text(123) == 123
        assert clean_text(None) is None
        assert clean_text(45.67) == 45.67

    def test_strip_whitespace(self):
        """Test that whitespace is stripped."""
        assert clean_text("  texto  ") == "texto"

    def test_clean_text_normal_string(self):
        """Test that normal strings are only stripped."""
        assert clean_text("normal text") == "normal text"


class TestCreateNarrative:
    """Tests for the create_narrative function."""

    def test_basic_narrative(self):
        """Test creation of basic narrative."""
        row = pd.Series({
            config.COLUMN_MES: "Agosto",
            config.COLUMN_NOME_GRUPO: "RECEITAS",
            config.COLUMN_CC_NOME: "DINHEIRO",
            config.COLUMN_REALIZADO: 1000.50,
        })
        narrative = create_narrative(row)
        
        assert "Agosto" in narrative
        assert "RECEITAS" in narrative
        assert "DINHEIRO" in narrative
        assert "R$" in narrative

    def test_narrative_with_subcategory(self):
        """Test narrative includes subcategory when different."""
        row = pd.Series({
            config.COLUMN_MES: "Janeiro",
            config.COLUMN_NOME_GRUPO: "CUSTOS",
            config.COLUMN_CC_NOME: "MATERIAL",
            config.COLUMN_REALIZADO: -500.00,
            "Camada03": "LIMPEZA",
        })
        narrative = create_narrative(row)
        
        assert "Subcategoria: LIMPEZA" in narrative

    def test_narrative_without_subcategory(self):
        """Test narrative when subcategory equals item."""
        row = pd.Series({
            config.COLUMN_MES: "Fevereiro",
            config.COLUMN_NOME_GRUPO: "VENDAS",
            config.COLUMN_CC_NOME: "PIX",
            config.COLUMN_REALIZADO: 2000.00,
            "Camada03": "PIX",
        })
        narrative = create_narrative(row)
        
        assert "Subcategoria" not in narrative

    def test_narrative_missing_columns(self):
        """Test narrative handles missing columns gracefully."""
        row = pd.Series({config.COLUMN_MES: "Março"})
        narrative = create_narrative(row)
        
        assert "Março" in narrative
        assert "Categoria Desconhecida" in narrative or narrative != ""


class TestGenerateNarratives:
    """Tests for the generate_narratives function."""

    def test_generate_narratives_adds_column(self):
        """Test that generate_narratives adds Narrativa_IA column."""
        df = pd.DataFrame({
            config.COLUMN_MES: ["Jan", "Fev"],
            config.COLUMN_NOME_GRUPO: ["RECEITAS", "CUSTOS"],
            config.COLUMN_CC_NOME: ["PIX", "SALARIOS"],
            config.COLUMN_REALIZADO: [1000.0, -500.0],
        })
        
        result = generate_narratives(df)
        
        assert "Narrativa_IA" in result.columns
        assert len(result) == 2

    def test_generate_narratives_preserves_original(self):
        """Test that original DataFrame is not modified."""
        df = pd.DataFrame({
            config.COLUMN_MES: ["Jan"],
            config.COLUMN_NOME_GRUPO: ["RECEITAS"],
            config.COLUMN_CC_NOME: ["PIX"],
            config.COLUMN_REALIZADO: [1000.0],
        })
        
        generate_narratives(df)
        
        assert "Narrativa_IA" not in df.columns


class TestGetNarrativeSummary:
    """Tests for the get_narrative_summary function."""

    def test_summary_with_narratives(self):
        """Test summary generation with valid narratives."""
        df = pd.DataFrame({
            config.COLUMN_NOME_GRUPO: ["A", "B", "A"],
            "Narrativa_IA": ["Texto 1", "Texto 2", "Texto 3"],
        })
        
        summary = get_narrative_summary(df)
        
        assert summary["total_records"] == 3
        assert summary["narratives_generated"] == 3
        assert summary["unique_groups"] == 2

    def test_summary_without_narrativa_column(self):
        """Test summary when Narrativa_IA column is missing."""
        df = pd.DataFrame({"col1": [1, 2, 3]})
        
        summary = get_narrative_summary(df)
        
        assert "error" in summary

