"""
Testes unitários para o módulo data_cleaner.

Testes cobrem conversão de moeda, parsing de mês e carregamento de arquivos CSV/Excel.
"""

import pytest
import pandas as pd
from pathlib import Path
import tempfile
import os

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_cleaner import (
    convert_brazilian_currency,
    convert_month_to_date,
    load_dre_csv,
    load_dre_excel,
    load_dre_file,
)


class TestConvertBrazilianCurrency:
    """Tests for the convert_brazilian_currency function."""

    def test_positive_value_with_cents(self):
        """Test conversion of positive value with cents."""
        assert convert_brazilian_currency("R$ 1.234,56") == 1234.56

    def test_positive_value_without_cents(self):
        """Test conversion of positive value without decimal part."""
        assert convert_brazilian_currency("R$ 63.713") == 63713.0

    def test_negative_value_with_prefix_minus(self):
        """Test conversion of negative value with minus before R$."""
        assert convert_brazilian_currency("-R$ 1.234,56") == -1234.56

    def test_negative_value_simple(self):
        """Test conversion of negative value without thousands separator."""
        assert convert_brazilian_currency("-R$ 19.026") == -19026.0

    def test_zero_value(self):
        """Test conversion of zero value."""
        assert convert_brazilian_currency("R$ 0,00") == 0.0

    def test_value_with_spaces(self):
        """Test conversion handles extra whitespace."""
        assert convert_brazilian_currency("  R$ 1.234,56  ") == 1234.56

    def test_large_value(self):
        """Test conversion of large values with multiple thousand separators."""
        assert convert_brazilian_currency("R$ 1.234.567,89") == 1234567.89

    def test_small_value(self):
        """Test conversion of small value without thousand separator."""
        assert convert_brazilian_currency("R$ 5") == 5.0

    def test_empty_string_returns_zero(self):
        """Test that empty string returns 0.0."""
        assert convert_brazilian_currency("") == 0.0

    def test_none_value_returns_zero(self):
        """Test that None returns 0.0."""
        assert convert_brazilian_currency(None) == 0.0

    def test_invalid_format_raises_error(self):
        """Test that invalid format raises ValueError."""
        with pytest.raises(ValueError):
            convert_brazilian_currency("invalid")

    def test_non_string_raises_error(self):
        """Test that non-string input raises TypeError."""
        with pytest.raises(TypeError):
            convert_brazilian_currency(1234.56)


class TestConvertMonthToDate:
    """Tests for the convert_month_to_date function."""

    def test_janeiro(self):
        """Test January conversion."""
        result = convert_month_to_date("Jan", 2025)
        assert result == pd.Timestamp("2025-01-01")

    def test_agosto(self):
        """Test August conversion."""
        result = convert_month_to_date("Ago", 2025)
        assert result == pd.Timestamp("2025-08-01")

    def test_dezembro(self):
        """Test December conversion."""
        result = convert_month_to_date("Dez", 2025)
        assert result == pd.Timestamp("2025-12-01")

    def test_all_months(self):
        """Test all month abbreviations."""
        months = {
            "Jan": 1, "Fev": 2, "Mar": 3, "Abr": 4,
            "Mai": 5, "Jun": 6, "Jul": 7, "Ago": 8,
            "Set": 9, "Out": 10, "Nov": 11, "Dez": 12,
        }
        for abbrev, month_num in months.items():
            result = convert_month_to_date(abbrev, 2025)
            assert result.month == month_num
            assert result.year == 2025
            assert result.day == 1

    def test_case_insensitive(self):
        """Test case-insensitive month matching."""
        result = convert_month_to_date("ago", 2025)
        assert result == pd.Timestamp("2025-08-01")

    def test_with_whitespace(self):
        """Test month with surrounding whitespace."""
        result = convert_month_to_date("  Set  ", 2025)
        assert result == pd.Timestamp("2025-09-01")

    def test_unknown_month_raises_error(self):
        """Test that unknown month raises ValueError."""
        with pytest.raises(ValueError, match="Unknown month abbreviation"):
            convert_month_to_date("Unknown", 2025)

    def test_empty_string_raises_error(self):
        """Test that empty string raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            convert_month_to_date("", 2025)

    def test_none_raises_error(self):
        """Test that None raises ValueError."""
        with pytest.raises(ValueError):
            convert_month_to_date(None, 2025)

    def test_different_year(self):
        """Test conversion with different reference year."""
        result = convert_month_to_date("Mar", 2024)
        assert result == pd.Timestamp("2024-03-01")


class TestLoadDreCsv:
    """Testes para a função load_dre_csv."""

    def test_file_not_found_raises_error(self):
        """Testa que arquivo inexistente levanta FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_dre_csv("arquivo_inexistente.csv")

    def test_load_valid_csv(self):
        """Testa carregamento de arquivo CSV válido."""
        # Cria um arquivo CSV temporário com estrutura adequada
        # Usando encoding latin-1 para corresponder ao config.CSV_ENCODING
        csv_content = """Ano Txt;2025;;;;;;
situacao;(Vários itens);;;;;;
GrupoEmpresa;Grupo J+;;;;;;
;;;;;;;
Loja;_key_centro_custo;cc_parent_nome;Nome Grupo;cc_nome;Camada03;Mês;Realizado
TEST;01.01.001;01.01;RECEITAS S/ VENDAS;DINHEIRO;DINHEIRO;Ago;R$ 63.713
TEST;01.01.002;01.01;RECEITAS S/ VENDAS;PIX;PIX;Set;R$ 10.000
"""
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.csv', delete=False, encoding='latin-1'
        ) as f:
            f.write(csv_content)
            temp_path = f.name

        try:
            df = load_dre_csv(temp_path)
            assert len(df) == 2
            assert "Nome Grupo" in df.columns
            assert "cc_nome" in df.columns
            assert "Mês" in df.columns
            assert "Realizado" in df.columns
        finally:
            os.unlink(temp_path)


class TestLoadDreExcel:
    """Testes para a função load_dre_excel."""

    def test_file_not_found_raises_error(self):
        """Testa que arquivo inexistente levanta FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_dre_excel("arquivo_inexistente.xlsx")

    def test_load_valid_excel(self):
        """Testa carregamento de arquivo Excel válido."""
        # Cria um DataFrame com a estrutura esperada do Excel DRE
        # Linhas 0-3 são metadados, linha 4 é o cabeçalho, linhas 5+ são dados
        rows = [
            ['Ano Txt', '2025', '', '', '', '', '', ''],  # Linha 0 - Metadados
            ['situacao', '(Vários)', '', '', '', '', '', ''],  # Linha 1 - Metadados
            ['GrupoEmpresa', 'Grupo J+', '', '', '', '', '', ''],  # Linha 2 - Metadados
            ['', '', '', '', '', '', '', ''],  # Linha 3 - Metadados vazio
            ['Loja', '_key_centro_custo', 'cc_parent_nome', 'Nome Grupo', 'cc_nome', 'Camada03', 'Mês', 'Realizado'],  # Linha 4 - Cabeçalho
            ['TEST', '01.01.001', '01.01', 'RECEITAS S/ VENDAS', 'DINHEIRO', 'DINHEIRO', 'Ago', 'R$ 63.713'],  # Linha 5 - Dados
            ['TEST', '01.01.002', '01.01', 'RECEITAS S/ VENDAS', 'PIX', 'PIX', 'Set', 'R$ 10.000'],  # Linha 6 - Dados
        ]

        df_excel = pd.DataFrame(rows)

        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            temp_path = f.name

        # Salvar como Excel sem header e sem index
        df_excel.to_excel(temp_path, index=False, header=False, engine='openpyxl')

        try:
            df = load_dre_excel(temp_path)
            assert len(df) == 2
            assert "Nome Grupo" in df.columns
            assert "cc_nome" in df.columns
            assert "Mês" in df.columns
            assert "Realizado" in df.columns
        finally:
            os.unlink(temp_path)


class TestLoadDreFile:
    """Testes para a função load_dre_file (detecção automática de formato)."""

    def test_detects_excel_format(self):
        """Testa que formato Excel é detectado pela extensão .xlsx."""
        # Cria arquivo Excel temporário com estrutura correta
        rows = [
            ['Ano Txt', '2025', '', '', '', '', '', ''],
            ['situacao', '(Vários)', '', '', '', '', '', ''],
            ['GrupoEmpresa', 'Grupo J+', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['Loja', '_key_centro_custo', 'cc_parent_nome', 'Nome Grupo', 'cc_nome', 'Camada03', 'Mês', 'Realizado'],
            ['TEST', '01.01.001', '01.01', 'RECEITAS S/ VENDAS', 'DINHEIRO', 'DINHEIRO', 'Ago', 'R$ 63.713'],
        ]

        df_excel = pd.DataFrame(rows)

        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            temp_path = f.name

        df_excel.to_excel(temp_path, index=False, header=False, engine='openpyxl')

        try:
            df = load_dre_file(temp_path)
            assert len(df) == 1
            assert "Nome Grupo" in df.columns
        finally:
            os.unlink(temp_path)

    def test_detects_csv_format(self):
        """Testa que formato CSV é detectado pela extensão .csv."""
        csv_content = """Ano Txt;2025;;;;;;
situacao;(Vários itens);;;;;;
GrupoEmpresa;Grupo J+;;;;;;
;;;;;;;
Loja;_key_centro_custo;cc_parent_nome;Nome Grupo;cc_nome;Camada03;Mês;Realizado
TEST;01.01.001;01.01;RECEITAS S/ VENDAS;DINHEIRO;DINHEIRO;Ago;R$ 63.713
"""
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.csv', delete=False, encoding='latin-1'
        ) as f:
            f.write(csv_content)
            temp_path = f.name

        try:
            df = load_dre_file(temp_path)
            assert len(df) == 1
            assert "Nome Grupo" in df.columns
        finally:
            os.unlink(temp_path)

    def test_unsupported_format_raises_error(self):
        """Testa que formato não suportado levanta ValueError."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            f.write(b"some content")
            temp_path = f.name

        try:
            with pytest.raises(ValueError, match="não suportado"):
                load_dre_file(temp_path)
        finally:
            os.unlink(temp_path)

