"""
Testes unitários para o módulo ai_classifier (src/).

Este módulo contém testes para as funções de classificação de gastos
usando IA (Google Gemini) e manipulação de dados CSV.

Author: Antonio Henrique
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

# Adiciona o diretório raiz ao path para importação
sys.path.insert(0, str(Path(__file__).parent.parent))


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def sample_mestre_df():
    """Cria um DataFrame mestre de exemplo para testes."""
    return pd.DataFrame({
        'Narrativa_IA': [
            'Em Ago, o grupo "RECEITAS" registrou R$ 1000.',
            'Em Set, o grupo "CUSTOS" registrou R$ -500.',
        ],
        'Mês': ['Ago', 'Set'],
        'Nome Grupo': ['RECEITAS S/ VENDAS', '( - ) CUSTOS VARIÁVEIS'],
        'cc_nome': ['DINHEIRO', 'BOVINOS'],
        'Realizado': ['R$ 1.000', '-R$ 500'],
    })


@pytest.fixture
def sample_entrada_df():
    """Cria um DataFrame de entrada de exemplo para testes."""
    return pd.DataFrame({
        'Data': ['15/01/2026'],
        'Descricao': ['Pagamento fornecedor carne'],
        'Valor': [200],
        'Mes': ['Jan'],
    })


@pytest.fixture
def temp_csv_files(sample_mestre_df, sample_entrada_df, tmp_path):
    """Cria arquivos CSV temporários para testes."""
    mestre_path = tmp_path / "relatorio_narrativo_ia.csv"
    entrada_path = tmp_path / "entrada.csv"

    sample_mestre_df.to_csv(mestre_path, sep=';', index=False, encoding='utf-8')
    sample_entrada_df.to_csv(entrada_path, sep=';', index=False, encoding='utf-8')

    return str(mestre_path), str(entrada_path)


# =============================================================================
# Testes para carregar_dados()
# =============================================================================

class TestCarregarDados:
    """Testes para a função carregar_dados()."""

    def test_carregar_dados_arquivos_existentes(self, temp_csv_files, monkeypatch):
        """Testa carregamento quando ambos os arquivos existem."""
        mestre_path, entrada_path = temp_csv_files

        # Mock das constantes do módulo
        monkeypatch.setattr('src.ai_classifier.ARQUIVO_MESTRE', Path(mestre_path))
        monkeypatch.setattr('src.ai_classifier.ARQUIVO_INPUT', Path(entrada_path))

        from src.ai_classifier import carregar_dados

        df_mestre, df_novo = carregar_dados(Path(mestre_path), Path(entrada_path))

        assert not df_mestre.empty
        assert not df_novo.empty
        assert 'cc_nome' in df_mestre.columns
        assert 'Descricao' in df_novo.columns

    def test_carregar_dados_mestre_nao_existe(self, tmp_path, monkeypatch):
        """Testa erro quando arquivo mestre não existe."""
        from src.ai_classifier import carregar_dados

        with pytest.raises(SystemExit) as exc_info:
            carregar_dados(tmp_path / "nao_existe.csv", tmp_path / "entrada.csv")

        assert exc_info.value.code == 1

    def test_carregar_dados_entrada_nao_existe(self, temp_csv_files, tmp_path, monkeypatch):
        """Testa saída limpa quando arquivo de entrada não existe."""
        mestre_path, _ = temp_csv_files

        from src.ai_classifier import carregar_dados

        with pytest.raises(SystemExit) as exc_info:
            carregar_dados(Path(mestre_path), tmp_path / "nao_existe.csv")

        assert exc_info.value.code == 0  # Saída normal, não erro


# =============================================================================
# Testes para classificar_gasto()
# =============================================================================

class TestClassificarGasto:
    """Testes para a função classificar_gasto()."""

    @patch('src.ai_classifier.get_model')
    def test_classificar_gasto_sucesso(self, mock_get_model):
        """Testa classificação bem-sucedida de um gasto."""
        # Mock da resposta da IA
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "BOVINOS"
        mock_model.generate_content.return_value = mock_response
        mock_get_model.return_value = mock_model

        from src.ai_classifier import classificar_gasto

        categorias = ['DINHEIRO', 'BOVINOS', 'AVES', 'REFRIGERANTES']
        resultado = classificar_gasto("Compra de carne bovina", categorias)

        assert resultado == "BOVINOS"
        mock_model.generate_content.assert_called_once()

    @patch('src.ai_classifier.get_model')
    def test_classificar_gasto_erro_ia(self, mock_get_model):
        """Testa tratamento de erro quando IA falha."""
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_get_model.return_value = mock_model

        from src.ai_classifier import classificar_gasto

        categorias = ['DINHEIRO', 'BOVINOS']
        resultado = classificar_gasto("Qualquer descrição", categorias)

        assert resultado == "ERRO_IA"


# =============================================================================
# Testes para main()
# =============================================================================

class TestMain:
    """Testes para funções de processamento."""

    @patch('src.ai_classifier.carregar_dados')
    @patch('src.ai_classifier.classificar_gasto')
    def test_processar_classificacao(self, mock_classificar, mock_carregar, sample_mestre_df, sample_entrada_df, tmp_path):
        """Testa processamento completo de dados novos."""
        mock_classificar.return_value = "BOVINOS"

        from src.ai_classifier import processar_classificacao

        resultado = processar_classificacao(sample_mestre_df, sample_entrada_df, "")

        assert not resultado.empty
        assert 'cc_nome' in resultado.columns

    def test_formatar_contexto_rag(self):
        """Testa formatação do contexto RAG."""
        from src.ai_classifier import formatar_contexto_rag

        categorias = {
            "RECEITAS": ["DINHEIRO", "CARTAO"],
            "CUSTOS": ["BOVINOS", "AVES"]
        }

        resultado = formatar_contexto_rag(categorias)

        assert "RECEITAS" in resultado
        assert "DINHEIRO" in resultado
        assert "BOVINOS" in resultado

    def test_formatar_contexto_rag_vazio(self):
        """Testa formatação quando não há categorias."""
        from src.ai_classifier import formatar_contexto_rag

        resultado = formatar_contexto_rag({})

        assert resultado == "Sem categorias disponíveis."


# =============================================================================
# Testes de Integração RAG
# =============================================================================

# Caminho do arquivo categories.json (gerado pelo pipeline)
CATEGORIES_PATH = Path(__file__).parent.parent / "output" / "categories.json"


class TestIntegracaoRAG:
    """Testes para integração com categories.json.

    Nota: Estes testes são skipped no CI pois dependem do arquivo
    categories.json que é gerado pelo pipeline de processamento.
    """

    @pytest.mark.skipif(
        not CATEGORIES_PATH.exists(),
        reason="categories.json não existe (gerado pelo pipeline)"
    )
    def test_categories_json_existe(self):
        """Verifica se o arquivo categories.json existe."""
        assert CATEGORIES_PATH.exists(), "Arquivo categories.json não encontrado"

    @pytest.mark.skipif(
        not CATEGORIES_PATH.exists(),
        reason="categories.json não existe (gerado pelo pipeline)"
    )
    def test_categories_json_formato_valido(self):
        """Verifica se categories.json tem formato válido."""
        import json

        with open(CATEGORIES_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert isinstance(data, dict)
        assert len(data) > 0

        # Verifica estrutura: grupo -> lista de categorias
        for grupo, categorias in data.items():
            assert isinstance(grupo, str)
            assert isinstance(categorias, list)
            assert all(isinstance(cat, str) for cat in categorias)

    @pytest.mark.skipif(
        not CATEGORIES_PATH.exists(),
        reason="categories.json não existe (gerado pelo pipeline)"
    )
    def test_categorias_principais_presentes(self):
        """Verifica se categorias principais estão presentes."""
        import json

        with open(CATEGORIES_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)

        grupos_esperados = [
            "RECEITAS S/ VENDAS",
            "( - ) CUSTOS VARIÁVEIS",
            "( - ) GASTOS COM PESSOAL",
        ]

        for grupo in grupos_esperados:
            assert grupo in data, f"Grupo '{grupo}' não encontrado em categories.json"

