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
    create_bar_chart,
    create_pie_chart,
    create_kpi_card,
    create_styled_dataframe,
)
from dashboard.components.data_loader import get_summary_stats
from dashboard.components.styles import (
    render_section_header,
    format_currency,
    COLORS,
)


def render_overview(df: pd.DataFrame, categories: dict) -> None:
    """
    Renderiza pagina de visao geral.

    Args:
        df: DataFrame com dados DRE.
        categories: Dicionario de categorias.
    """
    # Estatísticas
    stats = get_summary_stats(df)

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

    # Graficos resumo
    col_left, col_right = st.columns(2)

    with col_left:
        render_section_header("Resultado por Grupo DRE", "💰")

        col_grupo = config.COLUMN_NOME_GRUPO
        col_valor = config.COLUMN_REALIZADO

        if col_grupo in df.columns and col_valor in df.columns:
            grupo_totals = df.groupby(col_grupo)[col_valor].sum().reset_index()
            grupo_totals.columns = ["Grupo", "Valor"]
            grupo_totals = grupo_totals.sort_values("Valor", ascending=True)

            fig = create_bar_chart(
                grupo_totals,
                x="Valor",
                y="Grupo",
                title="",
                orientation="h",
                color_positive=COLORS["success"],
                color_negative=COLORS["danger"],
            )
            st.plotly_chart(fig, use_container_width=True)

    with col_right:
        render_section_header("Distribuicao de Categorias", "📊")

        if categories:
            cat_counts = pd.DataFrame([
                {"Grupo": grupo, "Categorias": len(cats)}
                for grupo, cats in categories.items()
            ])

            fig = create_pie_chart(
                cat_counts,
                values="Categorias",
                names="Grupo",
                title="",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Categorias nao disponiveis.")

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Tabela de dados recentes
    render_section_header("Ultimos Registros", "📋")

    display_cols = [
        col for col in [config.COLUMN_NOME_GRUPO, config.COLUMN_CC_NOME,
                        config.COLUMN_MES, config.COLUMN_REALIZADO]
        if col in df.columns
    ]

    if display_cols:
        df_display = df[display_cols].tail(10).copy()
        # Formatar valor
        if config.COLUMN_REALIZADO in df_display.columns:
            df_display[config.COLUMN_REALIZADO] = df_display[config.COLUMN_REALIZADO].apply(format_currency)
        st.dataframe(df_display, use_container_width=True, hide_index=True)

    # Info adicional em expander estilizado
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    with st.expander("ℹ️ Informacoes do Dataset"):
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.markdown(f"**Arquivo:** `{config.PROCESSED_PARQUET_PATH}`")
            st.markdown(f"**Total de colunas:** {len(df.columns)}")
        with col_info2:
            st.markdown(f"**Grupos unicos:** {stats['total_grupos']}")
            st.markdown(f"**Colunas:** {', '.join(df.columns.tolist()[:5])}...")

