"""
Pagina de Evolucao Temporal do Dashboard.

Exibe graficos de serie temporal dos dados DRE.
"""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

import config
from dashboard.components.charts import create_line_chart, create_bar_chart, create_kpi_card
from dashboard.components.styles import render_section_header, format_currency, format_percentage, COLORS


def render_evolucao(df: pd.DataFrame, categories: dict) -> None:
    """
    Renderiza pagina de evolucao temporal.

    Args:
        df: DataFrame com dados DRE.
        categories: Dicionario de categorias.
    """
    col_mes = config.COLUMN_MES
    col_grupo = config.COLUMN_NOME_GRUPO
    col_valor = config.COLUMN_REALIZADO

    # Filtros
    st.markdown("""
        <div style="background: #F8F9FA; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <p style="color: #6C757D; font-size: 0.8rem; margin: 0 0 0.5rem 0; text-transform: uppercase; letter-spacing: 0.5px;">Configuracoes</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        grupos_disponiveis = sorted(df[col_grupo].unique().tolist()) if col_grupo in df.columns else []
        grupos_selecionados = st.multiselect(
            "Grupos DRE",
            options=grupos_disponiveis,
            default=grupos_disponiveis[:3] if len(grupos_disponiveis) >= 3 else grupos_disponiveis,
            placeholder="Selecione os grupos...",
        )

    with col2:
        tipo_visualizacao = st.radio(
            "Tipo de Grafico",
            options=["Linha", "Barras"],
            horizontal=True,
        )
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Preparar dados
    if col_mes in df.columns and col_grupo in df.columns and col_valor in df.columns:
        df_filtered = df.copy()

        if grupos_selecionados:
            df_filtered = df_filtered[df_filtered[col_grupo].isin(grupos_selecionados)]

        # Agregar por mes e grupo
        evolucao = df_filtered.groupby([col_mes, col_grupo])[col_valor].sum().reset_index()
        evolucao.columns = ["Mes", "Grupo", "Valor"]

        # Ordenar meses
        ordem_meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
                       "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        evolucao["Mes"] = pd.Categorical(
            evolucao["Mes"],
            categories=[m for m in ordem_meses if m in evolucao["Mes"].unique()],
            ordered=True
        )
        evolucao = evolucao.sort_values("Mes")

        # Grafico principal
        render_section_header("Evolucao por Grupo", "📈")

        if tipo_visualizacao == "Linha":
            fig = create_line_chart(
                evolucao,
                x="Mes",
                y="Valor",
                title="",
                color="Grupo",
            )
        else:
            fig = create_bar_chart(
                evolucao,
                x="Mes",
                y="Valor",
                title="",
                color="Grupo",
            )

        st.plotly_chart(fig, use_container_width=True)

        # Evolucao total
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        render_section_header("Resultado Total Consolidado", "📊")

        total_mensal = df.groupby(col_mes)[col_valor].sum().reset_index()
        total_mensal.columns = ["Mes", "Resultado"]
        total_mensal["Mes"] = pd.Categorical(
            total_mensal["Mes"],
            categories=[m for m in ordem_meses if m in total_mensal["Mes"].unique()],
            ordered=True
        )
        total_mensal = total_mensal.sort_values("Mes")

        fig_total = create_line_chart(
            total_mensal,
            x="Mes",
            y="Resultado",
            title="",
            fill_area=True,
        )

        st.plotly_chart(fig_total, use_container_width=True)

        # Variacao percentual
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        render_section_header("Analise de Variacao", "📈")

        total_mensal["Variacao"] = total_mensal["Resultado"].pct_change() * 100
        total_mensal["Variacao"] = total_mensal["Variacao"].fillna(0).round(2)

        col_v1, col_v2 = st.columns([2, 1])

        with col_v1:
            display_df = total_mensal.copy()
            display_df["Resultado Formatado"] = display_df["Resultado"].apply(format_currency)
            display_df["Variacao %"] = display_df["Variacao"].apply(lambda x: format_percentage(x))
            st.dataframe(
                display_df[["Mes", "Resultado Formatado", "Variacao %"]],
                use_container_width=True,
                hide_index=True,
            )

        with col_v2:
            var_media = total_mensal["Variacao"].mean()
            var_max = total_mensal["Variacao"].max()
            var_min = total_mensal["Variacao"].min()

            create_kpi_card(var_media, "Variacao Media", suffix="%", icon="📊")
            create_kpi_card(var_max, "Maior Variacao", suffix="%", icon="📈")
            create_kpi_card(var_min, "Menor Variacao", suffix="%", icon="📉")

    else:
        st.warning("Colunas necessarias nao encontradas no dataset.")

