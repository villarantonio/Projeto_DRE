"""
Pagina de DRE Mensal do Dashboard.

Exibe demonstrativo de resultados em formato contabil.
"""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

import config
from dashboard.components.charts import create_bar_chart, create_kpi_card
from dashboard.components.styles import (
    render_section_header,
    format_currency,
    COLORS,
)


def render_dre_mensal(df: pd.DataFrame, categories: dict) -> None:
    """
    Renderiza pagina de DRE mensal.

    Args:
        df: DataFrame com dados DRE.
        categories: Dicionario de categorias.
    """
    col_mes = config.COLUMN_MES
    col_grupo = config.COLUMN_NOME_GRUPO
    col_valor = config.COLUMN_REALIZADO

    # Filtros em container estilizado
    st.markdown("""
        <div style="background: #F8F9FA; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
            <p style="color: #6C757D; font-size: 0.8rem; margin: 0 0 0.5rem 0; text-transform: uppercase; letter-spacing: 0.5px;">Filtros</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        meses_disponiveis = sorted(df[col_mes].unique().tolist()) if col_mes in df.columns else []
        mes_selecionado = st.selectbox(
            "Mes",
            options=["Todos"] + meses_disponiveis,
            index=0,
        )

    with col2:
        grupos_disponiveis = sorted(df[col_grupo].unique().tolist()) if col_grupo in df.columns else []
        grupos_selecionados = st.multiselect(
            "Grupos DRE",
            options=grupos_disponiveis,
            default=[],
            placeholder="Selecione os grupos...",
        )
    
    # Aplicar filtros
    df_filtered = df.copy()

    if mes_selecionado != "Todos" and col_mes in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[col_mes] == mes_selecionado]

    if grupos_selecionados and col_grupo in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[col_grupo].isin(grupos_selecionados)]

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Calcular totais primeiro para os KPIs
    if col_grupo in df_filtered.columns and col_valor in df_filtered.columns:
        dre_table = df_filtered.groupby(col_grupo)[col_valor].sum().reset_index()
        dre_table.columns = ["Grupo", "Valor"]
        dre_table = dre_table.sort_values("Grupo")

        total_receitas = dre_table[dre_table["Valor"] > 0]["Valor"].sum()
        total_custos = dre_table[dre_table["Valor"] < 0]["Valor"].sum()
        resultado = total_receitas + total_custos

        # KPIs de Resultado
        col_t1, col_t2, col_t3 = st.columns(3)

        with col_t1:
            create_kpi_card(
                value=total_receitas,
                label="Total Receitas",
                prefix="R$ ",
                icon="💚",
            )

        with col_t2:
            create_kpi_card(
                value=abs(total_custos),
                label="Custos e Despesas",
                prefix="R$ ",
                icon="🔴",
            )

        with col_t3:
            create_kpi_card(
                value=resultado,
                label="Resultado Liquido",
                prefix="R$ ",
                icon="📊",
                delta=round((resultado / total_receitas * 100) if total_receitas else 0, 1),
            )

        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

        # Tabela DRE
        render_section_header("Demonstrativo de Resultado", "📋")

        # Formatar valores
        dre_display = dre_table.copy()
        dre_display["Valor Formatado"] = dre_display["Valor"].apply(format_currency)

        st.dataframe(
            dre_display[["Grupo", "Valor Formatado"]],
            use_container_width=True,
            hide_index=True,
        )
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Grafico de barras
    render_section_header("Visualizacao por Grupo", "📊")

    if col_grupo in df_filtered.columns and col_valor in df_filtered.columns:
        grupo_chart = df_filtered.groupby(col_grupo)[col_valor].sum().reset_index()
        grupo_chart.columns = ["Grupo", "Valor"]
        grupo_chart = grupo_chart.sort_values("Valor", ascending=True)

        periodo = f" - {mes_selecionado}" if mes_selecionado != "Todos" else ""
        fig = create_bar_chart(
            grupo_chart,
            x="Valor",
            y="Grupo",
            title=f"DRE por Grupo{periodo}",
            orientation="h",
            color_positive=COLORS["success"],
            color_negative=COLORS["danger"],
        )

        st.plotly_chart(fig, use_container_width=True)

    # Detalhamento por categoria
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    with st.expander("📋 Detalhamento por Categoria"):
        col_cat = config.COLUMN_CC_NOME
        if col_cat in df_filtered.columns:
            detail = df_filtered.groupby([col_grupo, col_cat])[col_valor].sum().reset_index()
            detail.columns = ["Grupo", "Categoria", "Valor"]
            detail = detail.sort_values(["Grupo", "Valor"], ascending=[True, False])
            detail["Valor Formatado"] = detail["Valor"].apply(format_currency)

            st.dataframe(
                detail[["Grupo", "Categoria", "Valor Formatado"]],
                use_container_width=True,
                hide_index=True,
            )

