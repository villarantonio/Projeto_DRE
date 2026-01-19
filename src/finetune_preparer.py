"""
Preparador de Dataset para Fine-tuning de Modelos de IA.

Este módulo transforma dados do relatório narrativo em formato estruturado
para fine-tuning de modelos de linguagem (Gemini, GPT, etc.).

Gera arquivos JSONL compatíveis com APIs de fine-tuning.

Author: Projeto DRE - Manda Picanha
"""

import json
import logging
import sys
from pathlib import Path
from typing import Any

import pandas as pd

# Import config from parent
try:
    import config
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    import config


logger = logging.getLogger(__name__)


class FineTuneDatasetBuilder:
    """
    Construtor de datasets para fine-tuning de modelos de IA.
    
    Transforma narrativas do DRE em pares question-answer
    estruturados para treinamento supervisionado.
    
    Attributes:
        narratives_df: DataFrame com narrativas carregadas.
        categories: Dicionário com hierarquia de categorias.
        qa_pairs: Lista de pares question-answer gerados.
    """
    
    def __init__(
        self,
        narrative_path: Path | None = None,
        categories_path: Path | None = None,
    ):
        """
        Inicializa o construtor de dataset.
        
        Args:
            narrative_path: Caminho para CSV de narrativas.
            categories_path: Caminho para JSON de categorias.
        """
        self.narrative_path = narrative_path or config.NARRATIVE_CSV_PATH
        self.categories_path = categories_path or config.CATEGORIES_JSON_PATH
        self.narratives_df: pd.DataFrame | None = None
        self.categories: dict[str, list[str]] = {}
        self.qa_pairs: list[dict[str, Any]] = []
        
    def load_narratives(self) -> pd.DataFrame:
        """
        Carrega narrativas do arquivo CSV.
        
        Returns:
            DataFrame com narrativas.
            
        Raises:
            FileNotFoundError: Se arquivo não existir.
            ValueError: Se DataFrame estiver vazio.
        """
        if not self.narrative_path.exists():
            raise FileNotFoundError(
                f"Arquivo de narrativas não encontrado: {self.narrative_path}"
            )
        
        # Tenta diferentes encodings e separadores
        for encoding in ['utf-8-sig', 'utf-8', 'latin-1']:
            for sep in [';', ',']:
                try:
                    df = pd.read_csv(
                        self.narrative_path,
                        encoding=encoding,
                        sep=sep,
                        on_bad_lines='skip',  # Ignora linhas corrompidas
                    )
                    if len(df.columns) > 1:
                        self.narratives_df = df
                        logger.info(
                            f"Narrativas carregadas: {len(df)} registros "
                            f"(encoding={encoding}, sep='{sep}')"
                        )
                        return df
                except Exception:
                    continue
        
        raise ValueError(
            f"Não foi possível carregar narrativas de {self.narrative_path}"
        )
    
    def load_categories(self) -> dict[str, list[str]]:
        """
        Carrega hierarquia de categorias do JSON.
        
        Returns:
            Dicionário {grupo: [categorias]}.
        """
        if not self.categories_path.exists():
            logger.warning(f"Categories JSON não encontrado: {self.categories_path}")
            return {}
        
        with open(self.categories_path, 'r', encoding='utf-8') as f:
            self.categories = json.load(f)
        
        logger.info(f"Categorias carregadas: {len(self.categories)} grupos")
        return self.categories
    
    def create_qa_pairs(self) -> list[dict[str, Any]]:
        """
        Cria pares question-answer a partir das narrativas.
        
        Gera diferentes tipos de perguntas:
        - Classificação de gasto
        - Valor de categoria em mês específico
        - Comparação entre períodos
        
        Returns:
            Lista de dicionários com pares Q&A.
        """
        if self.narratives_df is None:
            self.load_narratives()
        
        self.qa_pairs = []
        df = self.narratives_df
        
        # Identifica colunas relevantes
        col_grupo = config.COLUMN_NOME_GRUPO if config.COLUMN_NOME_GRUPO in df.columns else 'Nome Grupo'
        col_categoria = config.COLUMN_CC_NOME if config.COLUMN_CC_NOME in df.columns else 'cc_nome'
        col_mes = config.COLUMN_MES if config.COLUMN_MES in df.columns else 'Mês'
        col_valor = config.COLUMN_REALIZADO if config.COLUMN_REALIZADO in df.columns else 'Realizado'
        col_narrativa = 'Narrativa_IA' if 'Narrativa_IA' in df.columns else None
        
        for idx, row in df.iterrows():
            grupo = str(row.get(col_grupo, '')).strip()
            categoria = str(row.get(col_categoria, '')).strip()
            mes = str(row.get(col_mes, '')).strip()
            valor = row.get(col_valor, 0)
            narrativa = str(row.get(col_narrativa, '')) if col_narrativa else ''
            
            if not categoria or not grupo:
                continue
            
            # Tipo 1: Classificação de gasto
            self.qa_pairs.append({
                "type": "classification",
                "question": f"Classifique o gasto '{categoria}' em uma categoria DRE.",
                "answer": f"O gasto '{categoria}' pertence ao grupo '{grupo}'.",
                "metadata": {
                    "categoria": categoria,
                    "grupo": grupo,
                    "mes": mes,
                }
            })
            
            # Tipo 2: Valor específico
            if valor and pd.notna(valor):
                valor_fmt = f"R$ {float(valor):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                self.qa_pairs.append({
                    "type": "value_query",
                    "question": f"Qual foi o valor de '{categoria}' em {mes}?",
                    "answer": f"O valor de '{categoria}' em {mes} foi {valor_fmt}.",
                    "metadata": {
                        "categoria": categoria,
                        "grupo": grupo,
                        "mes": mes,
                        "valor": float(valor) if pd.notna(valor) else 0,
                    }
                })
            
            # Tipo 3: Narrativa (se disponível)
            if narrativa and narrativa != 'nan':
                self.qa_pairs.append({
                    "type": "narrative",
                    "question": f"Descreva o registro de '{categoria}' em {mes}.",
                    "answer": narrativa,
                    "metadata": {
                        "categoria": categoria,
                        "grupo": grupo,
                        "mes": mes,
                    }
                })
        
        logger.info(f"Pares Q&A criados: {len(self.qa_pairs)}")
        return self.qa_pairs
    
    def export_jsonl(
        self,
        output_path: Path | None = None,
        format_type: str = "gemini",
    ) -> Path:
        """
        Exporta dataset para formato JSONL.
        
        Args:
            output_path: Caminho de saída. Se None, usa config.
            format_type: Formato do JSONL ('gemini', 'openai', 'generic').
            
        Returns:
            Path do arquivo gerado.
        """
        if not self.qa_pairs:
            self.create_qa_pairs()
        
        output_path = output_path or config.OUTPUT_DIR / "finetune_dataset.jsonl"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for pair in self.qa_pairs:
                if format_type == "gemini":
                    # Formato Gemini Tuning API
                    record = {
                        "text_input": pair["question"],
                        "output": pair["answer"],
                    }
                elif format_type == "openai":
                    # Formato OpenAI Fine-tuning
                    record = {
                        "messages": [
                            {"role": "user", "content": pair["question"]},
                            {"role": "assistant", "content": pair["answer"]},
                        ]
                    }
                else:
                    # Formato genérico
                    record = pair
                
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        
        logger.info(f"Dataset exportado: {output_path} ({len(self.qa_pairs)} registros)")
        return output_path
    
    def validate_dataset(self) -> dict[str, Any]:
        """
        Valida qualidade do dataset gerado.
        
        Returns:
            Dicionário com métricas de validação.
        """
        if not self.qa_pairs:
            self.create_qa_pairs()
        
        # Contagem por tipo
        type_counts = {}
        for pair in self.qa_pairs:
            pair_type = pair.get("type", "unknown")
            type_counts[pair_type] = type_counts.get(pair_type, 0) + 1
        
        # Categorias únicas
        categories = set()
        groups = set()
        for pair in self.qa_pairs:
            meta = pair.get("metadata", {})
            if meta.get("categoria"):
                categories.add(meta["categoria"])
            if meta.get("grupo"):
                groups.add(meta["grupo"])
        
        # Tamanho médio das respostas
        answer_lengths = [len(p.get("answer", "")) for p in self.qa_pairs]
        avg_length = sum(answer_lengths) / len(answer_lengths) if answer_lengths else 0
        
        validation = {
            "total_pairs": len(self.qa_pairs),
            "pairs_by_type": type_counts,
            "unique_categories": len(categories),
            "unique_groups": len(groups),
            "avg_answer_length": round(avg_length, 2),
            "min_answer_length": min(answer_lengths) if answer_lengths else 0,
            "max_answer_length": max(answer_lengths) if answer_lengths else 0,
            "is_valid": len(self.qa_pairs) >= 100,  # Mínimo recomendado
        }
        
        logger.info(f"Validação: {validation['total_pairs']} pares, válido={validation['is_valid']}")
        return validation
    
    def get_category_coverage(self) -> dict[str, float]:
        """
        Calcula cobertura de categorias no dataset.
        
        Returns:
            Dicionário com percentual de cobertura por grupo.
        """
        if not self.categories:
            self.load_categories()
        
        if not self.qa_pairs:
            self.create_qa_pairs()
        
        # Categorias presentes no dataset
        dataset_categories = set()
        for pair in self.qa_pairs:
            meta = pair.get("metadata", {})
            if meta.get("categoria"):
                dataset_categories.add(meta["categoria"])
        
        # Calcular cobertura por grupo
        coverage = {}
        for grupo, cats in self.categories.items():
            cats_set = set(cats)
            covered = cats_set.intersection(dataset_categories)
            coverage[grupo] = len(covered) / len(cats_set) if cats_set else 0.0
        
        return coverage


def build_finetune_dataset(
    narrative_path: Path | None = None,
    categories_path: Path | None = None,
    output_path: Path | None = None,
    format_type: str = "gemini",
) -> dict[str, Any]:
    """
    Função de conveniência para construir dataset completo.
    
    Args:
        narrative_path: Caminho para narrativas CSV.
        categories_path: Caminho para categorias JSON.
        output_path: Caminho de saída JSONL.
        format_type: Formato de exportação.
        
    Returns:
        Dicionário com métricas e caminho do arquivo.
    """
    builder = FineTuneDatasetBuilder(narrative_path, categories_path)
    builder.load_narratives()
    builder.load_categories()
    builder.create_qa_pairs()
    
    exported_path = builder.export_jsonl(output_path, format_type)
    validation = builder.validate_dataset()
    coverage = builder.get_category_coverage()
    
    return {
        "output_path": str(exported_path),
        "validation": validation,
        "category_coverage": coverage,
    }


# =============================================================================
# Standalone Execution
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    
    print("=" * 60)
    print("FINE-TUNE DATASET BUILDER - DRE Manda Picanha")
    print("=" * 60)
    
    try:
        result = build_finetune_dataset()
        
        print(f"\n✅ Dataset gerado: {result['output_path']}")
        print(f"\n📊 Validação:")
        for key, value in result['validation'].items():
            print(f"   - {key}: {value}")
        
        print(f"\n📁 Cobertura por Grupo:")
        for grupo, cov in result['category_coverage'].items():
            print(f"   - {grupo}: {cov:.1%}")
            
    except FileNotFoundError as e:
        print(f"\n❌ Erro: {e}")
        print("Execute primeiro o pipeline principal (main.py) para gerar os arquivos.")
        sys.exit(1)

