"""
Módulo de carregamento de dados para o Dashboard.

Fornece funções cacheadas para carregar dados processados
do pipeline DRE.
"""

import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Adiciona raiz do projeto ao path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

import config


@st.cache_data(ttl=300)  # Cache por 5 minutos
def load_processed_data() -> pd.DataFrame:
    """
    Carrega dados processados do arquivo Parquet.
    
    Returns:
        DataFrame com dados DRE processados.
        
    Raises:
        FileNotFoundError: Se arquivo não existir.
    """
    parquet_path = config.PROCESSED_PARQUET_PATH
    
    if not parquet_path.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {parquet_path}\n"
            "Execute 'python main.py' para gerar os dados."
        )
    
    df = pd.read_parquet(parquet_path)
    
    # Garantir tipos corretos
    if config.COLUMN_REALIZADO in df.columns:
        df[config.COLUMN_REALIZADO] = pd.to_numeric(
            df[config.COLUMN_REALIZADO], errors='coerce'
        ).fillna(0)
    
    return df


@st.cache_data(ttl=300)
def load_categories() -> dict[str, list[str]]:
    """
    Carrega hierarquia de categorias do JSON.
    
    Returns:
        Dicionário {grupo: [categorias]}.
    """
    json_path = config.CATEGORIES_JSON_PATH
    
    if not json_path.exists():
        return {}
    
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@st.cache_data(ttl=300)
def load_narratives() -> pd.DataFrame:
    """
    Carrega relatório de narrativas.
    
    Returns:
        DataFrame com narrativas para IA.
    """
    csv_path = config.NARRATIVE_CSV_PATH
    
    if not csv_path.exists():
        return pd.DataFrame()
    
    # Tenta diferentes encodings
    for encoding in ['utf-8-sig', 'utf-8', 'latin-1']:
        for sep in [';', ',']:
            try:
                df = pd.read_csv(csv_path, encoding=encoding, sep=sep)
                if len(df.columns) > 1:
                    return df
            except Exception:
                continue
    
    return pd.DataFrame()


def get_summary_stats(df: pd.DataFrame) -> dict:
    """
    Calcula estatísticas resumidas do DataFrame.
    
    Args:
        df: DataFrame com dados DRE.
        
    Returns:
        Dicionário com estatísticas.
    """
    col_valor = config.COLUMN_REALIZADO
    col_grupo = config.COLUMN_NOME_GRUPO
    
    stats = {
        "total_registros": len(df),
        "total_grupos": df[col_grupo].nunique() if col_grupo in df.columns else 0,
        "total_valor": df[col_valor].sum() if col_valor in df.columns else 0,
        "receitas": df[df[col_valor] > 0][col_valor].sum() if col_valor in df.columns else 0,
        "custos": abs(df[df[col_valor] < 0][col_valor].sum()) if col_valor in df.columns else 0,
    }
    
    # Calcular margem se possível
    if stats["receitas"] > 0:
        stats["margem"] = ((stats["receitas"] - stats["custos"]) / stats["receitas"]) * 100
    else:
        stats["margem"] = 0
    
    return stats


def filter_dataframe(
    df: pd.DataFrame,
    grupos: list[str] | None = None,
    meses: list[str] | None = None,
) -> pd.DataFrame:
    """
    Filtra DataFrame por grupos e meses.

    Args:
        df: DataFrame original.
        grupos: Lista de grupos para filtrar.
        meses: Lista de meses para filtrar.

    Returns:
        DataFrame filtrado.
    """
    filtered = df.copy()

    col_grupo = config.COLUMN_NOME_GRUPO
    col_mes = config.COLUMN_MES

    if grupos and col_grupo in filtered.columns:
        filtered = filtered[filtered[col_grupo].isin(grupos)]

    if meses and col_mes in filtered.columns:
        filtered = filtered[filtered[col_mes].isin(meses)]

    return filtered


def get_unique_stores(df: pd.DataFrame, store_column: str = "Loja") -> list[str]:
    """
    Retorna lista de lojas únicas no DataFrame.

    Args:
        df: DataFrame com dados.
        store_column: Nome da coluna de lojas.

    Returns:
        Lista de lojas únicas ordenadas.
    """
    if store_column not in df.columns:
        return []

    stores = df[store_column].dropna().unique().tolist()
    return sorted([str(s) for s in stores])


def filter_by_stores(
    df: pd.DataFrame,
    stores: list[str] | None,
    store_column: str = "Loja"
) -> pd.DataFrame:
    """
    Filtra DataFrame por lojas selecionadas.

    Args:
        df: DataFrame original.
        stores: Lista de lojas para filtrar (None = todas).
        store_column: Nome da coluna de lojas.

    Returns:
        DataFrame filtrado.
    """
    if not stores or store_column not in df.columns:
        return df

    return df[df[store_column].isin(stores)]

