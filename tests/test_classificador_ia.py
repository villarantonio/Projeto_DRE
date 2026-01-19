"""
Testes unitários para o módulo classificador_ia.

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
        monkeypatch.setattr('classificador_ia.ARQUIVO_MESTRE', mestre_path)
        monkeypatch.setattr('classificador_ia.ARQUIVO_INPUT', entrada_path)

        from classificador_ia import carregar_dados

        df_mestre, df_novo = carregar_dados()

        assert not df_mestre.empty
        assert not df_novo.empty
        assert 'cc_nome' in df_mestre.columns
        assert 'Descricao' in df_novo.columns

    def test_carregar_dados_mestre_nao_existe(self, tmp_path, monkeypatch):
        """Testa erro quando arquivo mestre não existe."""
        monkeypatch.setattr('classificador_ia.ARQUIVO_MESTRE', str(tmp_path / "nao_existe.csv"))
        monkeypatch.setattr('classificador_ia.ARQUIVO_INPUT', str(tmp_path / "entrada.csv"))

        from classificador_ia import carregar_dados

        with pytest.raises(SystemExit) as exc_info:
            carregar_dados()

        assert exc_info.value.code == 1

    def test_carregar_dados_entrada_nao_existe(self, temp_csv_files, tmp_path, monkeypatch):
        """Testa saída limpa quando arquivo de entrada não existe."""
        mestre_path, _ = temp_csv_files

        monkeypatch.setattr('classificador_ia.ARQUIVO_MESTRE', mestre_path)
        monkeypatch.setattr('classificador_ia.ARQUIVO_INPUT', str(tmp_path / "nao_existe.csv"))

        from classificador_ia import carregar_dados

        with pytest.raises(SystemExit) as exc_info:
            carregar_dados()

        assert exc_info.value.code == 0  # Saída normal, não erro


# =============================================================================
# Testes para classificar_gasto()
# =============================================================================

class TestClassificarGasto:
    """Testes para a função classificar_gasto()."""

    @patch('classificador_ia.model')
    def test_classificar_gasto_sucesso(self, mock_model):
        """Testa classificação bem-sucedida de um gasto."""
        # Mock da resposta da IA
        mock_response = MagicMock()
        mock_response.text = "BOVINOS"
        mock_model.generate_content.return_value = mock_response

        from classificador_ia import classificar_gasto

        categorias = ['DINHEIRO', 'BOVINOS', 'AVES', 'REFRIGERANTES']
        resultado = classificar_gasto("Compra de carne bovina", categorias)

        assert resultado == "BOVINOS"
        mock_model.generate_content.assert_called_once()

    @patch('classificador_ia.model')
    def test_classificar_gasto_erro_ia(self, mock_model):
        """Testa tratamento de erro quando IA falha."""
        mock_model.generate_content.side_effect = Exception("API Error")

        from classificador_ia import classificar_gasto

        categorias = ['DINHEIRO', 'BOVINOS']
        resultado = classificar_gasto("Qualquer descrição", categorias)


# =============================================================================
# Testes para main()
# =============================================================================

class TestMain:
    """Testes para a função main()."""

    @patch('classificador_ia.carregar_dados')
    @patch('classificador_ia.classificar_gasto')
    def test_main_processa_dados_novos(self, mock_classificar, mock_carregar, sample_mestre_df, sample_entrada_df, tmp_path):
        """Testa processamento completo de dados novos."""
        mock_carregar.return_value = (sample_mestre_df, sample_entrada_df)
        mock_classificar.return_value = "BOVINOS"

        # Configura arquivo de saída temporário
        with patch('classificador_ia.ARQUIVO_MESTRE', str(tmp_path / "output.csv")):
            from classificador_ia import main

            # Não deve lançar exceção
            try:
                main()
            except SystemExit:
                pass  # Ignora sys.exit() normal

    @patch('classificador_ia.carregar_dados')
    @patch('classificador_ia.API_KEY', 'fake_key_for_test')
    def test_main_entrada_vazia(self, mock_carregar, sample_mestre_df):
        """Testa saída quando entrada está vazia."""
        df_vazio = pd.DataFrame()
        mock_carregar.return_value = (sample_mestre_df, df_vazio)

        from classificador_ia import main

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0  # Saída normal


# =============================================================================
# Testes de Integração RAG
# =============================================================================

class TestIntegracaoRAG:
    """Testes para integração com categories.json."""

    def test_categories_json_existe(self):
        """Verifica se o arquivo categories.json existe."""
        categories_path = Path(__file__).parent.parent / "output" / "categories.json"
        assert categories_path.exists(), "Arquivo categories.json não encontrado"

    def test_categories_json_formato_valido(self):
        """Verifica se categories.json tem formato válido."""
        import json
        categories_path = Path(__file__).parent.parent / "output" / "categories.json"

        with open(categories_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert isinstance(data, dict)
        assert len(data) > 0

        # Verifica estrutura: grupo -> lista de categorias
        for grupo, categorias in data.items():
            assert isinstance(grupo, str)
            assert isinstance(categorias, list)
            assert all(isinstance(cat, str) for cat in categorias)

    def test_categorias_principais_presentes(self):
        """Verifica se categorias principais estão presentes."""
        import json
        categories_path = Path(__file__).parent.parent / "output" / "categories.json"

        with open(categories_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        grupos_esperados = [
            "RECEITAS S/ VENDAS",
            "( - ) CUSTOS VARIÁVEIS",
            "( - ) GASTOS COM PESSOAL",
        ]

        for grupo in grupos_esperados:
            assert grupo in data, f"Grupo '{grupo}' não encontrado em categories.json"

