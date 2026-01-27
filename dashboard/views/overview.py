"""
Pagina de Visao Geral do Dashboard.

Exibe KPIs principais e resumo dos dados DRE.
"""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

import config
from dashboard.components.charts import (
    create_kpi_card,
    create_styled_dre_html_table,
    render_store_filter,
)
from dashboard.components.data_loader import (
    get_summary_stats,
    filter_by_stores,
    get_unique_stores,
)
from dashboard.components.styles import render_section_header


def render_overview(df: pd.DataFrame, categories: dict) -> None:
    """
    Renderiza pagina de visao geral.

    Args:
        df: DataFrame com dados DRE.
        categories: Dicionario de categorias.
    """
    # Filtro de loja no topo
    st.markdown("### 🏪 Filtro de Lojas")
    selected_stores = render_store_filter(
        df,
        store_column="Loja",
        key="overview_store_filter",
        label="Selecione as lojas para análise"
    )

    # Aplicar filtro
    df_filtered = filter_by_stores(df, selected_stores, "Loja")

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Estatísticas
    stats = get_summary_stats(df_filtered)

    # KPIs principais em grid responsivo
    render_section_header("Indicadores Principais", "📈")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        create_kpi_card(
            value=stats["total_registros"],
            label="Total de Registros",
            icon="📋",
        )

    with col2:
        create_kpi_card(
            value=stats["receitas"],
            label="Receitas Totais",
            prefix="R$ ",
            delta=5.2,
            icon="💚",
        )

    with col3:
        create_kpi_card(
            value=abs(stats["custos"]),
            label="Custos Totais",
            prefix="R$ ",
            delta=-3.1,
            delta_color="inverse",
            icon="🔴",
        )

    with col4:
        create_kpi_card(
            value=stats["margem"],
            label="Margem Liquida",
            suffix="%",
            delta=2.5,
            icon="📊",
        )
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # Visao Geral em formato de planilha (estilo Excel)
    # -------------------------------------------------------------------------

    render_section_header("Demonstrativo de Resultado do Exercicio - Visao Geral", "📊")

    col_grupo = config.COLUMN_NOME_GRUPO
    col_valor = config.COLUMN_REALIZADO

    if col_grupo in df_filtered.columns and col_valor in df_filtered.columns:
        # Tabela DRE estilizada com HTML/CSS customizado
        create_styled_dre_html_table(
            df_filtered,
            group_column=col_grupo,
            store_column="Loja",
            value_column=col_valor,
            max_stores=15,
            height=550,
        )
    else:
        st.warning("Colunas necessarias nao encontradas para montar a tabela DRE.")

    # Info adicional em expander estilizado
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    with st.expander("ℹ️ Informacoes do Dataset"):
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.markdown(f"**Arquivo:** `{config.PROCESSED_PARQUET_PATH}`")
            st.markdown(f"**Total de colunas:** {len(df.columns)}")
            if selected_stores:
                st.markdown(f"**Lojas selecionadas:** {len(selected_stores)}")
        with col_info2:
            st.markdown(f"**Grupos unicos:** {stats['total_grupos']}")
            st.markdown(f"**Colunas:** {', '.join(df.columns.tolist()[:5])}...")
            all_stores = get_unique_stores(df, "Loja")
            st.markdown(f"**Total de lojas:** {len(all_stores)}")

