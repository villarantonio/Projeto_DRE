"""
Pacote de Automação Financeira DRE.

Este pacote contém módulos para limpeza de dados, gerenciamento de categorias,
geração de narrativas e processamento de dados financeiros para DRE
(Demonstração do Resultado do Exercício).

Suporta arquivos de entrada nos formatos Excel (.xlsx) e CSV (.csv).
"""

from src.data_cleaner import (
    load_dre_file,
    load_dre_excel,
    load_dre_csv,
    convert_brazilian_currency,
    convert_month_to_date,
)
from src.category_engine import CategoryManager
from src.narrative_generator import (
    generate_narratives,
    save_narrative_report,
    get_narrative_summary,
    clean_text,
    create_narrative,
)

# Importações condicionais para módulos de IA (requerem google-generativeai)
try:
    from src.ai_classifier import (
        classificar_gasto,
        carregar_categorias_rag,
        formatar_contexto_rag,
        processar_classificacao,
    )
    from src.data_processor_ia import (
        trava_seguranca_duplicidade,
        processar_com_validacao,
    )
    from src.finetune_preparer import (
        FineTuneDatasetBuilder,
        build_finetune_dataset,
    )
    _AI_AVAILABLE = True
except ImportError:
    _AI_AVAILABLE = False

__all__ = [
    # Data cleaner - Funções de carregamento
    "load_dre_file",      # Detecta formato automaticamente (recomendado)
    "load_dre_excel",     # Carrega arquivos Excel (.xlsx)
    "load_dre_csv",       # Carrega arquivos CSV (legado)
    # Data cleaner - Funções de conversão
    "convert_brazilian_currency",
    "convert_month_to_date",
    # Category engine
    "CategoryManager",
    # Narrative generator
    "generate_narratives",
    "save_narrative_report",
    "get_narrative_summary",
    "clean_text",
    "create_narrative",
    # AI Classifier (requer google-generativeai)
    "classificar_gasto",
    "carregar_categorias_rag",
    "formatar_contexto_rag",
    "processar_classificacao",
    # Data Processor IA
    "trava_seguranca_duplicidade",
    "processar_com_validacao",
    # Fine-tune Preparer
    "FineTuneDatasetBuilder",
    "build_finetune_dataset",
]

