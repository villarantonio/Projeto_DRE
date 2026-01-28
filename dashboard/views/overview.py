"""
Pagina de Visao Geral do Dashboard.

Exibe KPIs principais e resumo dos dados DRE com filtros interativos.
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
    filter_by_months,
    get_unique_stores,
    get_unique_months,
    clean_dataframe_text,
)
from dashboard.components.styles import render_section_header


def format_month_label(month) -> str:
    """
    Formata timestamp de mes para exibicao amigavel.

    Args:
        month: Timestamp ou valor do mes.

    Returns:
        String formatada como 'Jan/2025'.
    """
    try:
        if hasattr(month, 'strftime'):
            return month.strftime('%b/%Y')
        return str(month)
    except Exception:
        return str(month)


def render_overview(df: pd.DataFrame, categories: dict) -> None:
    """
    Renderiza pagina de visao geral com filtros interativos.

    Args:
        df: DataFrame com dados DRE.
        categories: Dicionario de categorias.
    """
    # -------------------------------------------------------------------------
    # Aplicar limpeza de encoding nos dados
    # -------------------------------------------------------------------------
    df_clean = clean_dataframe_text(df, [config.COLUMN_NOME_GRUPO])

    # -------------------------------------------------------------------------
    # Filtros interativos no topo da pagina
    # -------------------------------------------------------------------------
    st.markdown("### 🔍 Filtros")

    col_filter1, col_filter2 = st.columns(2)

    # Filtro de lojas
    with col_filter1:
        selected_stores = render_store_filter(
            df_clean,
            store_column="Loja",
            key="overview_store_filter",
            label="🏪 Selecione as lojas"
        )

    # Filtro de meses/periodo
    with col_filter2:
        available_months = get_unique_months(df_clean, "Mês")

        # Formatar labels dos meses para exibicao
        month_labels = {m: format_month_label(m) for m in available_months}

        selected_months = st.multiselect(
            "📅 Selecione os meses",
            options=available_months,
            default=available_months,  # Todos selecionados por padrao
            format_func=lambda x: month_labels.get(x, str(x)),
            key="overview_month_filter"
        )

    # Aplicar filtros
    df_filtered = filter_by_stores(df_clean, selected_stores, "Loja")
    df_filtered = filter_by_months(df_filtered, selected_months, "Mês")

    # Mostrar resumo dos filtros aplicados
    filter_info = []
    if selected_stores:
        filter_info.append(f"**Lojas:** {len(selected_stores)} selecionadas")
    else:
        filter_info.append(f"**Lojas:** Todas ({len(get_unique_stores(df_clean, 'Loja'))})")

    if selected_months:
        filter_info.append(f"**Meses:** {len(selected_months)} selecionados")
    else:
        filter_info.append(f"**Meses:** Todos ({len(available_months)})")

    st.caption(" | ".join(filter_info))

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # Estatisticas e KPIs
    # -------------------------------------------------------------------------
    stats = get_summary_stats(df_filtered)

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
            icon="💚",
        )

    with col3:
        create_kpi_card(
            value=abs(stats["custos"]),
            label="Custos Totais",
            prefix="R$ ",
            delta_color="inverse",
            icon="🔴",
        )

    with col4:
        create_kpi_card(
            value=stats["margem"],
            label="Margem Liquida",
            suffix="%",
            icon="📊",
        )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # Tabela DRE em formato de planilha (estilo Excel)
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

    # -------------------------------------------------------------------------
    # Informacoes adicionais do dataset
    # -------------------------------------------------------------------------
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    with st.expander("ℹ️ Informacoes do Dataset"):
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.markdown(f"**Arquivo:** `{config.PROCESSED_PARQUET_PATH}`")
            st.markdown(f"**Total de colunas:** {len(df.columns)}")
            st.markdown(f"**Registros filtrados:** {len(df_filtered):,}")
        with col_info2:
            st.markdown(f"**Grupos unicos:** {stats['total_grupos']}")
            all_stores = get_unique_stores(df_clean, "Loja")
            st.markdown(f"**Total de lojas:** {len(all_stores)}")
            st.markdown(f"**Total de meses:** {len(available_months)}")

