"""
Classificador de Gastos Financeiros com IA (Google Gemini).

Este módulo classifica gastos financeiros automaticamente usando
Google Gemini 2.0 Flash e contexto RAG do arquivo categories.json.

Refatorado para seguir a estrutura do projeto (src/).

Author: Projeto DRE - Manda Picanha
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

import pandas as pd

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None

# Import config from parent
try:
    import config
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    import config


logger = logging.getLogger(__name__)


# --- CONFIGURAÇÕES ---
ARQUIVO_MESTRE = config.NARRATIVE_CSV_PATH if hasattr(config, 'NARRATIVE_CSV_PATH') else Path("relatorio_narrativo_ia.csv")
ARQUIVO_INPUT = Path("entrada.csv")
CATEGORIES_JSON = config.CATEGORIES_JSON_PATH if hasattr(config, 'CATEGORIES_JSON_PATH') else Path("output/categories.json")

API_KEY = os.getenv("GEMINI_API_KEY")

# Modelo da IA (inicialização lazy)
_model = None


def get_model():
    """Retorna instância do modelo Gemini (singleton)."""
    global _model
    if _model is None and API_KEY and GENAI_AVAILABLE:
        genai.configure(api_key=API_KEY)
        _model = genai.GenerativeModel('gemini-2.0-flash')
    return _model


def carregar_categorias_rag(categories_path: Path = None) -> dict:
    """
    Carrega categorias do arquivo JSON para contexto RAG.

    Args:
        categories_path: Caminho para o arquivo categories.json.

    Returns:
        Dicionário com grupos e suas categorias.
    """
    path = categories_path or CATEGORIES_JSON
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    logger.warning(f"Arquivo {path} não encontrado")
    return {}


def formatar_contexto_rag(categorias_dict: dict) -> str:
    """
    Formata o dicionário de categorias em texto para o prompt.

    Args:
        categorias_dict: Dicionário {grupo: [categorias]}.

    Returns:
        Texto formatado para o prompt da IA.
    """
    if not categorias_dict:
        return "Sem categorias disponíveis."

    contexto_partes = []
    for grupo, categorias in categorias_dict.items():
        cats_str = ", ".join(categorias)
        contexto_partes.append(f"- {grupo}: {cats_str}")

    return "\n".join(contexto_partes)


def carregar_dados(mestre_path: Path = None, input_path: Path = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Carrega dados do arquivo mestre e entrada.

    Args:
        mestre_path: Caminho para o arquivo mestre.
        input_path: Caminho para o arquivo de entrada.

    Returns:
        Tupla (df_mestre, df_novo).

    Raises:
        SystemExit: Se arquivos não existirem.
    """
    mestre = mestre_path or ARQUIVO_MESTRE
    entrada = input_path or ARQUIVO_INPUT

    # Carrega o Mestre
    if mestre.exists():
        try:
            df_mestre = pd.read_csv(mestre, sep=';', encoding='utf-8')
        except Exception:
            df_mestre = pd.read_csv(mestre, sep=',', encoding='utf-8')
    else:
        logger.error(f"Arquivo mestre '{mestre}' não encontrado.")
        sys.exit(1)

    # Carrega a Entrada
    if entrada.exists():
        try:
            df_novo = pd.read_csv(entrada, sep=';', encoding='utf-8')
        except Exception:
            df_novo = pd.read_csv(entrada, sep=',', encoding='utf-8')
    else:
        logger.info("Arquivo de entrada não encontrado. Nada a processar.")
        sys.exit(0)

    return df_mestre, df_novo


def classificar_gasto(descricao: str, categorias_validas: list = None, contexto_rag: str = "") -> str:
    """
    Classifica um gasto usando IA com contexto RAG.

    Args:
        descricao: Descrição do gasto a classificar.
        categorias_validas: Lista de categorias válidas (fallback).
        contexto_rag: Contexto formatado do categories.json.

    Returns:
        Categoria classificada ou "ERRO_IA"/"OUTROS".
    """
    model = get_model()
    if model is None:
        return "ERRO_IA"

    categorias_validas = categorias_validas or []

    # Usa contexto RAG se disponível, senão usa lista simples
    if contexto_rag:
        contexto = f"""
HIERARQUIA DE CATEGORIAS FINANCEIRAS (DRE):
{contexto_rag}
"""
    else:
        contexto = f"Categorias disponíveis: {', '.join(categorias_validas)}"

    prompt = f"""
Você é um especialista em classificação financeira para restaurantes.

{contexto}

TAREFA: Classifique o gasto abaixo em UMA categoria específica (cc_nome).
GASTO: "{descricao}"

REGRAS:
1. Responda APENAS com o nome exato da categoria (ex: BOVINOS, REFRIGERANTES)
2. NÃO inclua o grupo (ex: "( - ) CUSTOS VARIÁVEIS")
3. Se não encontrar categoria adequada, responda "OUTROS"
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Erro na classificação IA: {e}")
        return "ERRO_IA"


def processar_classificacao(
    df_mestre: pd.DataFrame,
    df_novo: pd.DataFrame,
    contexto_rag: str = ""
) -> pd.DataFrame:
    """
    Processa classificação de novos dados.

    Args:
        df_mestre: DataFrame com dados históricos.
        df_novo: DataFrame com novos dados.
        contexto_rag: Contexto RAG formatado.

    Returns:
        DataFrame novo com classificações.
    """
    col_cat = 'cc_nome'
    if col_cat not in df_mestre.columns:
        col_cat = df_mestre.columns[2] if len(df_mestre.columns) > 2 else df_mestre.columns[0]

    categorias_fallback = df_mestre[col_cat].dropna().unique().tolist()

    # Garante que a coluna de categoria existe no novo
    if col_cat not in df_novo.columns:
        df_novo[col_cat] = ""

    for i, row in df_novo.iterrows():
        desc = str(row.get('Descricao', 'Sem descrição'))
        cat_ia = classificar_gasto(desc, categorias_fallback, contexto_rag)
        df_novo.at[i, col_cat] = cat_ia
        logger.info(f"Classificado: {desc[:30]}... -> {cat_ia}")

    return df_novo


# =============================================================================
# Standalone Execution
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    if not API_KEY:
        print("Erro: GEMINI_API_KEY não configurada.")
        sys.exit(1)

    print("--- INICIANDO CLASSIFICADOR IA (src/ai_classifier.py) ---")

    # Carregar dados
    df_mestre, df_novo = carregar_dados()

    # Carregar contexto RAG
    categorias_dict = carregar_categorias_rag()
    contexto_rag = formatar_contexto_rag(categorias_dict)

    if categorias_dict:
        print(f"✅ RAG carregado: {len(categorias_dict)} grupos")
    else:
        print("⚠️ Usando categorias do CSV como fallback")

    if df_novo.empty:
        print("Entrada vazia. Nada a processar.")
        sys.exit(0)

    # Processar
    df_resultado = processar_classificacao(df_mestre, df_novo, contexto_rag)

    # Salvar
    df_resultado = df_resultado.reindex(columns=df_mestre.columns, fill_value='')
    df_final = pd.concat([df_mestre, df_resultado], ignore_index=True)
    df_final.to_csv(ARQUIVO_MESTRE, sep=';', index=False, encoding='utf-8')

    print(f"✅ SUCESSO: {len(df_resultado)} itens classificados e salvos.")
