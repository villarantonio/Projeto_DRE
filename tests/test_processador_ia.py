"""
Testes unitários para o módulo data_processor_ia (src/).

Este módulo contém testes para as funções de processamento de dados
com trava de segurança contra duplicidade e classificação IA.

Author: Antonio Henrique
"""

import os
import sys
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
            'Em Out, o grupo "RECEITAS" registrou R$ 800.',
        ],
        'Mes': ['Ago', 'Set', 'Out'],
        'Nome Grupo': ['RECEITAS S/ VENDAS', '( - ) CUSTOS VARIÁVEIS', 'RECEITAS S/ VENDAS'],
        'cc_nome': ['DINHEIRO', 'BOVINOS', 'IFOOD'],
        'Realizado': ['R$ 1.000', '-R$ 500', 'R$ 800'],
    })


@pytest.fixture
def sample_entrada_df():
    """Cria um DataFrame de entrada de exemplo para testes."""
    return pd.DataFrame({
        'Data': ['15/01/2026', '20/01/2026'],
        'Descricao': ['Pagamento fornecedor carne', 'Compra de bebidas'],
        'Valor': [200, 150],
        'Mes': ['Nov', 'Nov'],  # Mês novo, não duplicado
    })


@pytest.fixture
def sample_entrada_duplicada_df():
    """Cria um DataFrame com mês já existente (duplicado)."""
    return pd.DataFrame({
        'Data': ['15/01/2026'],
        'Descricao': ['Pagamento teste'],
        'Valor': [100],
        'Mes': ['Ago'],  # Já existe no mestre
    })


# =============================================================================
# Testes para trava_seguranca_duplicidade()
# =============================================================================

class TestTravaSegurancaDuplicidade:
    """Testes para a função trava_seguranca_duplicidade()."""

    def test_trava_permite_meses_novos(self, sample_mestre_df, sample_entrada_df):
        """Testa que meses novos são permitidos sem erro."""
        from src.data_processor_ia import trava_seguranca_duplicidade

        # Não deve lançar exceção
        trava_seguranca_duplicidade(sample_mestre_df, sample_entrada_df)

    def test_trava_bloqueia_meses_duplicados(self, sample_mestre_df, sample_entrada_duplicada_df):
        """Testa que meses duplicados são bloqueados."""
        from src.data_processor_ia import trava_seguranca_duplicidade

        with pytest.raises(SystemExit) as exc_info:
            trava_seguranca_duplicidade(sample_mestre_df, sample_entrada_duplicada_df)

        assert exc_info.value.code == 1  # Erro de duplicidade

    def test_trava_sem_coluna_mes(self, sample_mestre_df):
        """Testa comportamento quando coluna 'Mes' não existe."""
        from src.data_processor_ia import trava_seguranca_duplicidade

        df_sem_mes = pd.DataFrame({
            'Data': ['15/01/2026'],
            'Descricao': ['Pagamento teste'],
            'Valor': [100],
        })

        # Deve passar sem erro (pula validação)
        trava_seguranca_duplicidade(sample_mestre_df, df_sem_mes)

    def test_trava_multiplos_meses_novos(self, sample_mestre_df):
        """Testa com múltiplos meses novos."""
        from src.data_processor_ia import trava_seguranca_duplicidade

        df_multiplos_meses = pd.DataFrame({
            'Data': ['15/11/2026', '20/12/2026', '25/01/2027'],
            'Descricao': ['Item 1', 'Item 2', 'Item 3'],
            'Valor': [100, 200, 300],
            'Mes': ['Nov', 'Dez', 'Jan'],  # Todos novos
        })

        # Não deve lançar exceção
        trava_seguranca_duplicidade(sample_mestre_df, df_multiplos_meses)

    def test_trava_parcialmente_duplicado(self, sample_mestre_df):
        """Testa quando alguns meses são novos e outros duplicados."""
        from src.data_processor_ia import trava_seguranca_duplicidade

        df_parcial = pd.DataFrame({
            'Data': ['15/11/2026', '20/08/2026'],  # Nov=novo, Ago=duplicado
            'Descricao': ['Item novo', 'Item duplicado'],
            'Valor': [100, 200],
            'Mes': ['Nov', 'Ago'],
        })

        with pytest.raises(SystemExit) as exc_info:
            trava_seguranca_duplicidade(sample_mestre_df, df_parcial)

        assert exc_info.value.code == 1


# =============================================================================
# Testes para classificar_gasto()
# =============================================================================

class TestClassificarGastoProcessador:
    """Testes para a função classificar_gasto() do processador."""

    @patch('src.data_processor_ia.get_model')
    def test_classificar_gasto_retorna_categoria(self, mock_get_model):
        """Testa que classificação retorna categoria correta."""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "REFRIGERANTES"
        mock_model.generate_content.return_value = mock_response
        mock_get_model.return_value = mock_model

        from src.data_processor_ia import classificar_gasto

        categorias = ['DINHEIRO', 'REFRIGERANTES']
        resultado = classificar_gasto("Compra de coca-cola", categorias)

        assert resultado == "REFRIGERANTES"

    @patch('src.data_processor_ia.get_model')
    def test_classificar_gasto_erro_retorna_fallback(self, mock_get_model):
        """Testa fallback quando IA falha."""
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_get_model.return_value = mock_model

        from src.data_processor_ia import classificar_gasto

        categorias = ['DINHEIRO', 'BOVINOS']
        resultado = classificar_gasto("Descrição qualquer", categorias)

        assert resultado == "ERRO_IA"

    @patch('src.data_processor_ia.get_model')
    def test_classificar_gasto_strip_whitespace(self, mock_get_model):
        """Testa que whitespace é removido da resposta."""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "  BOVINOS  \n"
        mock_model.generate_content.return_value = mock_response
        mock_get_model.return_value = mock_model

        from src.data_processor_ia import classificar_gasto

        categorias = ['DINHEIRO', 'BOVINOS']
        resultado = classificar_gasto("Carne", categorias)

        assert resultado == "BOVINOS"

    @patch('src.data_processor_ia.get_model')
    def test_classificar_gasto_categoria_outros(self, mock_get_model):
        """Testa quando IA não consegue classificar."""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "OUTROS"
        mock_model.generate_content.return_value = mock_response
        mock_get_model.return_value = mock_model

        from src.data_processor_ia import classificar_gasto

        categorias = ['DINHEIRO', 'BOVINOS']
        resultado = classificar_gasto("Item desconhecido xyz", categorias)

        assert resultado == "OUTROS"


# =============================================================================
# Testes de Integração
# =============================================================================

class TestIntegracaoProcessador:
    """Testes de integração do processador."""

    @patch('src.data_processor_ia.get_model')
    def test_processar_com_validacao(self, mock_get_model, sample_mestre_df, sample_entrada_df, tmp_path):
        """Testa fluxo completo do processamento com validação."""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "BOVINOS"
        mock_model.generate_content.return_value = mock_response
        mock_get_model.return_value = mock_model

        from src.data_processor_ia import processar_com_validacao

        output_path = tmp_path / "output.csv"

        df_resultado = processar_com_validacao(
            sample_mestre_df,
            sample_entrada_df,
            output_path
        )

        assert len(df_resultado) >= len(sample_mestre_df)
        assert output_path.exists()

    def test_constantes_importadas_de_ai_classifier(self):
        """Verifica que constantes são importadas de ai_classifier."""
        from src.data_processor_ia import ARQUIVO_MESTRE
        from src.ai_classifier import ARQUIVO_MESTRE as ARQUIVO_MESTRE_ORIGINAL

        # Deve ser o mesmo objeto (importado)
        assert ARQUIVO_MESTRE == ARQUIVO_MESTRE_ORIGINAL
