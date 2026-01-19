"""
Página de Composição do Dashboard.

Exibe análise de composição de receitas e custos com treemaps e pizzas.
"""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

import config
from dashboard.components.charts import create_pie_chart, create_treemap


def render_composicao(df: pd.DataFrame, categories: dict) -> None:
    """
    Renderiza página de composição.
    
    Args:
        df: DataFrame com dados DRE.
        categories: Dicionário de categorias.
    """
    st.header("🥧 Composição Financeira")
    st.markdown("Análise da composição de receitas, custos e despesas.")
    
    col_grupo = config.COLUMN_NOME_GRUPO
    col_cat = config.COLUMN_CC_NOME
    col_valor = config.COLUMN_REALIZADO
    col_mes = config.COLUMN_MES
    
    # Filtro de mês
    meses = sorted(df[col_mes].unique().tolist()) if col_mes in df.columns else []
    mes_selecionado = st.selectbox(
        "Filtrar por Mês:",
        options=["Todos"] + meses,
    )
    
    df_filtered = df.copy()
    if mes_selecionado != "Todos" and col_mes in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[col_mes] == mes_selecionado]
    
    st.markdown("---")
    
    # Tabs para diferentes visões
    tab1, tab2, tab3 = st.tabs(["📊 Receitas", "📉 Custos/Despesas", "🗺️ Hierarquia"])
    
    with tab1:
        st.subheader("💚 Composição de Receitas")
        
        # Filtrar apenas receitas (valores positivos)
        receitas = df_filtered[df_filtered[col_valor] > 0].copy()
        
        if len(receitas) > 0 and col_cat in receitas.columns:
            # Agregar por categoria
            receitas_agg = receitas.groupby(col_cat)[col_valor].sum().reset_index()
            receitas_agg.columns = ["Categoria", "Valor"]
            receitas_agg = receitas_agg.sort_values("Valor", ascending=False).head(10)
            
            fig = create_pie_chart(
                receitas_agg,
                values="Valor",
                names="Categoria",
                title="Top 10 Fontes de Receita",
                hole=0.4,
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela detalhada
            with st.expander("📋 Detalhamento"):
                receitas_agg["Valor Formatado"] = receitas_agg["Valor"].apply(
                    lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                )
                receitas_agg["Percentual"] = (
                    receitas_agg["Valor"] / receitas_agg["Valor"].sum() * 100
                ).round(1).astype(str) + "%"
                st.dataframe(
                    receitas_agg[["Categoria", "Valor Formatado", "Percentual"]],
                    use_container_width=True,
                    hide_index=True,
                )
        else:
            st.info("Sem dados de receitas para o período selecionado.")
    
    with tab2:
        st.subheader("🔴 Composição de Custos e Despesas")
        
        # Filtrar apenas custos/despesas (valores negativos)
        custos = df_filtered[df_filtered[col_valor] < 0].copy()
        custos[col_valor] = custos[col_valor].abs()  # Converter para positivo
        
        if len(custos) > 0 and col_cat in custos.columns:
            # Agregar por categoria
            custos_agg = custos.groupby(col_cat)[col_valor].sum().reset_index()
            custos_agg.columns = ["Categoria", "Valor"]
            custos_agg = custos_agg.sort_values("Valor", ascending=False).head(10)
            
            fig = create_pie_chart(
                custos_agg,
                values="Valor",
                names="Categoria",
                title="Top 10 Maiores Custos/Despesas",
                hole=0.4,
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela detalhada
            with st.expander("📋 Detalhamento"):
                custos_agg["Valor Formatado"] = custos_agg["Valor"].apply(
                    lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                )
                custos_agg["Percentual"] = (
                    custos_agg["Valor"] / custos_agg["Valor"].sum() * 100
                ).round(1).astype(str) + "%"
                st.dataframe(
                    custos_agg[["Categoria", "Valor Formatado", "Percentual"]],
                    use_container_width=True,
                    hide_index=True,
                )
        else:
            st.info("Sem dados de custos para o período selecionado.")
    
    with tab3:
        st.subheader("🗺️ Hierarquia Completa (Treemap)")
        
        if col_grupo in df_filtered.columns and col_cat in df_filtered.columns:
            # Preparar dados para treemap (valores absolutos)
            treemap_data = df_filtered.copy()
            treemap_data["Valor_Abs"] = treemap_data[col_valor].abs()
            
            # Filtrar valores maiores que zero
            treemap_data = treemap_data[treemap_data["Valor_Abs"] > 0]
            
            if len(treemap_data) > 0:
                # Agregar
                treemap_agg = treemap_data.groupby(
                    [col_grupo, col_cat]
                )["Valor_Abs"].sum().reset_index()
                treemap_agg.columns = ["Grupo", "Categoria", "Valor"]
                
                fig = create_treemap(
                    treemap_agg,
                    path=["Grupo", "Categoria"],
                    values="Valor",
                    title="Hierarquia DRE Completa",
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Sem dados para gerar treemap.")
        else:
            st.warning("Colunas de hierarquia não encontradas.")

