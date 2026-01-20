"""
Pagina de Composicao do Dashboard.

Exibe analise de composicao de receitas e custos com treemaps e pizzas.
"""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

import config
from dashboard.components.charts import create_pie_chart, create_treemap
from dashboard.components.styles import render_section_header, format_currency, format_percentage


def render_composicao(df: pd.DataFrame, categories: dict) -> None:
    """
    Renderiza pagina de composicao.

    Args:
        df: DataFrame com dados DRE.
        categories: Dicionario de categorias.
    """
    col_grupo = config.COLUMN_NOME_GRUPO
    col_cat = config.COLUMN_CC_NOME
    col_valor = config.COLUMN_REALIZADO
    col_mes = config.COLUMN_MES

    # Filtro de mes
    st.markdown("""
        <div style="background: #F8F9FA; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <p style="color: #6C757D; font-size: 0.8rem; margin: 0 0 0.5rem 0; text-transform: uppercase; letter-spacing: 0.5px;">Periodo</p>
        </div>
    """, unsafe_allow_html=True)

    meses = sorted([m for m in df[col_mes].unique().tolist() if m is not None]) if col_mes in df.columns else []
    mes_selecionado = st.selectbox(
        "Mes",
        options=["Todos"] + meses,
        label_visibility="collapsed",
    )

    df_filtered = df.copy()
    if mes_selecionado != "Todos" and col_mes in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[col_mes] == mes_selecionado]

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Tabs para diferentes visoes
    tab1, tab2, tab3 = st.tabs(["💚 Receitas", "🔴 Custos/Despesas", "🗺️ Hierarquia Completa"])

    with tab1:
        render_section_header("Composicao de Receitas", "💚")

        # Filtrar apenas receitas (valores positivos)
        receitas = df_filtered[df_filtered[col_valor] > 0].copy()

        if len(receitas) > 0 and col_cat in receitas.columns:
            receitas_agg = receitas.groupby(col_cat)[col_valor].sum().reset_index()
            receitas_agg.columns = ["Categoria", "Valor"]
            receitas_agg = receitas_agg.sort_values("Valor", ascending=False).head(10)

            fig = create_pie_chart(
                receitas_agg,
                values="Valor",
                names="Categoria",
                title="Top 10 Fontes de Receita",
            )
            st.plotly_chart(fig, use_container_width=True)

            with st.expander("📋 Detalhamento das Receitas"):
                receitas_agg["Valor Formatado"] = receitas_agg["Valor"].apply(format_currency)
                receitas_agg["Percentual"] = receitas_agg["Valor"].apply(
                    lambda x: format_percentage(x / receitas_agg["Valor"].sum() * 100)
                )
                st.dataframe(
                    receitas_agg[["Categoria", "Valor Formatado", "Percentual"]],
                    use_container_width=True,
                    hide_index=True,
                )
        else:
            st.info("Sem dados de receitas para o periodo selecionado.")

    with tab2:
        render_section_header("Composicao de Custos e Despesas", "🔴")

        # Filtrar apenas custos/despesas (valores negativos)
        custos = df_filtered[df_filtered[col_valor] < 0].copy()
        custos[col_valor] = custos[col_valor].abs()

        if len(custos) > 0 and col_cat in custos.columns:
            custos_agg = custos.groupby(col_cat)[col_valor].sum().reset_index()
            custos_agg.columns = ["Categoria", "Valor"]
            custos_agg = custos_agg.sort_values("Valor", ascending=False).head(10)

            fig = create_pie_chart(
                custos_agg,
                values="Valor",
                names="Categoria",
                title="Top 10 Maiores Custos",
            )
            st.plotly_chart(fig, use_container_width=True)

            with st.expander("📋 Detalhamento dos Custos"):
                custos_agg["Valor Formatado"] = custos_agg["Valor"].apply(format_currency)
                custos_agg["Percentual"] = custos_agg["Valor"].apply(
                    lambda x: format_percentage(x / custos_agg["Valor"].sum() * 100)
                )
                st.dataframe(
                    custos_agg[["Categoria", "Valor Formatado", "Percentual"]],
                    use_container_width=True,
                    hide_index=True,
                )
        else:
            st.info("Sem dados de custos para o periodo selecionado.")

    with tab3:
        render_section_header("Hierarquia Completa", "🗺️")

        if col_grupo in df_filtered.columns and col_cat in df_filtered.columns:
            treemap_data = df_filtered.copy()
            treemap_data["Valor_Abs"] = treemap_data[col_valor].abs()
            treemap_data = treemap_data[treemap_data["Valor_Abs"] > 0]

            if len(treemap_data) > 0:
                treemap_agg = treemap_data.groupby(
                    [col_grupo, col_cat]
                )["Valor_Abs"].sum().reset_index()
                treemap_agg.columns = ["Grupo", "Categoria", "Valor"]

                fig = create_treemap(
                    treemap_agg,
                    path=["Grupo", "Categoria"],
                    values="Valor",
                    title="",
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Sem dados para gerar treemap.")
        else:
            st.warning("Colunas de hierarquia nao encontradas.")

