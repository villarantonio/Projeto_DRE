"""
Testes unitários para o módulo finetune_preparer.

Cobertura de testes:
- Carregamento de narrativas (CSV)
- Carregamento de categorias (JSON)
- Criação de pares Q&A
- Exportação JSONL (múltiplos formatos)
- Validação de dataset
- Cobertura de categorias
"""

import json
import tempfile
from pathlib import Path

import pandas as pd
import pytest

from src.finetune_preparer import (
    FineTuneDatasetBuilder,
    build_finetune_dataset,
)


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def sample_narratives_csv(tmp_path: Path) -> Path:
    """Cria arquivo CSV de narrativas de exemplo."""
    csv_path = tmp_path / "narrativas.csv"
    data = {
        "Nome Grupo": [
            "RECEITAS S/ VENDAS",
            "RECEITAS S/ VENDAS",
            "( - ) CUSTOS VARIÁVEIS",
            "( - ) CUSTOS VARIÁVEIS",
            "DESPESAS FIXAS",
        ],
        "cc_nome": ["PIX", "DINHEIRO", "BOVINOS", "BEBIDAS", "ALUGUEL"],
        "Mês": ["Jan", "Jan", "Jan", "Fev", "Fev"],
        "Realizado": [15000.50, 8500.00, -12000.00, -3500.00, -5000.00],
        "Narrativa_IA": [
            "Em Jan, PIX registrou R$ 15.000,50 em receitas.",
            "Em Jan, DINHEIRO registrou R$ 8.500,00 em receitas.",
            "Em Jan, BOVINOS registrou custo de R$ 12.000,00.",
            "Em Fev, BEBIDAS registrou custo de R$ 3.500,00.",
            "Em Fev, ALUGUEL registrou despesa de R$ 5.000,00.",
        ],
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False, sep=";", encoding="utf-8-sig")
    return csv_path


@pytest.fixture
def sample_categories_json(tmp_path: Path) -> Path:
    """Cria arquivo JSON de categorias de exemplo."""
    json_path = tmp_path / "categories.json"
    categories = {
        "RECEITAS S/ VENDAS": ["PIX", "DINHEIRO", "CARTÃO", "IFOOD"],
        "( - ) CUSTOS VARIÁVEIS": ["BOVINOS", "BEBIDAS", "HORTIFRUTI"],
        "DESPESAS FIXAS": ["ALUGUEL", "ENERGIA", "INTERNET"],
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(categories, f, ensure_ascii=False, indent=2)
    return json_path


@pytest.fixture
def builder_with_data(
    sample_narratives_csv: Path,
    sample_categories_json: Path,
) -> FineTuneDatasetBuilder:
    """Retorna builder com dados carregados."""
    builder = FineTuneDatasetBuilder(
        narrative_path=sample_narratives_csv,
        categories_path=sample_categories_json,
    )
    builder.load_narratives()
    builder.load_categories()
    return builder


# =============================================================================
# Testes de Carregamento
# =============================================================================

class TestLoadNarratives:
    """Testes para carregamento de narrativas."""
    
    def test_load_narratives_success(
        self,
        sample_narratives_csv: Path,
    ):
        """Testa carregamento bem-sucedido de CSV."""
        builder = FineTuneDatasetBuilder(narrative_path=sample_narratives_csv)
        df = builder.load_narratives()
        
        assert df is not None
        assert len(df) == 5
        assert "cc_nome" in df.columns
        assert "Narrativa_IA" in df.columns
    
    def test_load_narratives_file_not_found(self, tmp_path: Path):
        """Testa erro quando arquivo não existe."""
        builder = FineTuneDatasetBuilder(
            narrative_path=tmp_path / "nao_existe.csv"
        )
        
        with pytest.raises(FileNotFoundError):
            builder.load_narratives()
    
    def test_load_narratives_different_encodings(self, tmp_path: Path):
        """Testa carregamento com diferentes encodings."""
        csv_path = tmp_path / "latin1.csv"
        data = {"col1": ["café", "açúcar"], "col2": [1, 2]}
        df = pd.DataFrame(data)
        df.to_csv(csv_path, index=False, sep=",", encoding="latin-1")
        
        builder = FineTuneDatasetBuilder(narrative_path=csv_path)
        loaded_df = builder.load_narratives()
        
        assert len(loaded_df) == 2


class TestLoadCategories:
    """Testes para carregamento de categorias."""
    
    def test_load_categories_success(
        self,
        sample_categories_json: Path,
    ):
        """Testa carregamento bem-sucedido de JSON."""
        builder = FineTuneDatasetBuilder(categories_path=sample_categories_json)
        categories = builder.load_categories()
        
        assert len(categories) == 3
        assert "RECEITAS S/ VENDAS" in categories
        assert "PIX" in categories["RECEITAS S/ VENDAS"]
    
    def test_load_categories_file_not_found(self, tmp_path: Path):
        """Testa retorno vazio quando arquivo não existe."""
        builder = FineTuneDatasetBuilder(
            categories_path=tmp_path / "nao_existe.json"
        )
        categories = builder.load_categories()
        
        assert categories == {}


# =============================================================================
# Testes de Criação de Q&A
# =============================================================================

class TestCreateQAPairs:
    """Testes para criação de pares question-answer."""
    
    def test_create_qa_pairs_generates_correct_count(
        self,
        builder_with_data: FineTuneDatasetBuilder,
    ):
        """Testa que pares Q&A são gerados corretamente."""
        pairs = builder_with_data.create_qa_pairs()
        
        # 5 registros * 3 tipos (classificação, valor, narrativa) = 15
        assert len(pairs) >= 10  # Mínimo esperado
    
    def test_qa_pairs_have_required_fields(
        self,
        builder_with_data: FineTuneDatasetBuilder,
    ):
        """Testa que pares têm campos obrigatórios."""
        pairs = builder_with_data.create_qa_pairs()
        
        for pair in pairs:
            assert "type" in pair
            assert "question" in pair
            assert "answer" in pair
            assert "metadata" in pair
    
    def test_qa_pairs_classification_type(
        self,
        builder_with_data: FineTuneDatasetBuilder,
    ):
        """Testa pares do tipo classificação."""
        pairs = builder_with_data.create_qa_pairs()
        
        classification_pairs = [p for p in pairs if p["type"] == "classification"]
        assert len(classification_pairs) >= 5
        
        # Verifica conteúdo
        sample = classification_pairs[0]
        assert "Classifique" in sample["question"]
        assert "pertence ao grupo" in sample["answer"]


# =============================================================================
# Testes de Exportação
# =============================================================================

class TestExportJSONL:
    """Testes para exportação JSONL."""
    
    def test_export_jsonl_gemini_format(
        self,
        builder_with_data: FineTuneDatasetBuilder,
        tmp_path: Path,
    ):
        """Testa exportação no formato Gemini."""
        output_path = tmp_path / "output.jsonl"
        builder_with_data.create_qa_pairs()
        result_path = builder_with_data.export_jsonl(output_path, "gemini")
        
        assert result_path.exists()
        
        with open(result_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        assert len(lines) > 0
        first_record = json.loads(lines[0])
        assert "text_input" in first_record
        assert "output" in first_record
    
    def test_export_jsonl_openai_format(
        self,
        builder_with_data: FineTuneDatasetBuilder,
        tmp_path: Path,
    ):
        """Testa exportação no formato OpenAI."""
        output_path = tmp_path / "output_openai.jsonl"
        builder_with_data.create_qa_pairs()
        result_path = builder_with_data.export_jsonl(output_path, "openai")
        
        assert result_path.exists()
        
        with open(result_path, "r", encoding="utf-8") as f:
            first_line = f.readline()
        
        record = json.loads(first_line)
        assert "messages" in record
        assert len(record["messages"]) == 2
        assert record["messages"][0]["role"] == "user"
        assert record["messages"][1]["role"] == "assistant"


# =============================================================================
# Testes de Validação
# =============================================================================

class TestValidateDataset:
    """Testes para validação de dataset."""
    
    def test_validate_returns_metrics(
        self,
        builder_with_data: FineTuneDatasetBuilder,
    ):
        """Testa que validação retorna métricas esperadas."""
        builder_with_data.create_qa_pairs()
        validation = builder_with_data.validate_dataset()
        
        assert "total_pairs" in validation
        assert "pairs_by_type" in validation
        assert "unique_categories" in validation
        assert "avg_answer_length" in validation
        assert "is_valid" in validation
    
    def test_category_coverage(
        self,
        builder_with_data: FineTuneDatasetBuilder,
    ):
        """Testa cálculo de cobertura de categorias."""
        builder_with_data.create_qa_pairs()
        coverage = builder_with_data.get_category_coverage()
        
        assert len(coverage) == 3  # 3 grupos
        # RECEITAS tem 2/4 categorias (PIX, DINHEIRO)
        assert coverage["RECEITAS S/ VENDAS"] == 0.5


# =============================================================================
# Testes de Função de Conveniência
# =============================================================================

class TestBuildFineTuneDataset:
    """Testes para função de conveniência."""
    
    def test_build_finetune_dataset_complete(
        self,
        sample_narratives_csv: Path,
        sample_categories_json: Path,
        tmp_path: Path,
    ):
        """Testa construção completa do dataset."""
        output_path = tmp_path / "complete.jsonl"
        
        result = build_finetune_dataset(
            narrative_path=sample_narratives_csv,
            categories_path=sample_categories_json,
            output_path=output_path,
            format_type="gemini",
        )
        
        assert "output_path" in result
        assert "validation" in result
        assert "category_coverage" in result
        assert Path(result["output_path"]).exists()

