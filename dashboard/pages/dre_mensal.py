"""
Página de DRE Mensal do Dashboard.

Exibe demonstrativo de resultados em formato contábil.
"""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

import config
from dashboard.components.charts import create_bar_chart


def render_dre_mensal(df: pd.DataFrame, categories: dict) -> None:
    """
    Renderiza página de DRE mensal.
    
    Args:
        df: DataFrame com dados DRE.
        categories: Dicionário de categorias.
    """
    st.header("📈 DRE Mensal")
    st.markdown("Demonstração do Resultado do Exercício por mês.")
    
    col_mes = config.COLUMN_MES
    col_grupo = config.COLUMN_NOME_GRUPO
    col_valor = config.COLUMN_REALIZADO
    
    # Filtros
    col1, col2 = st.columns(2)
    
    with col1:
        # Filtro de mês
        meses_disponiveis = sorted(df[col_mes].unique().tolist()) if col_mes in df.columns else []
        mes_selecionado = st.selectbox(
            "Selecione o Mês:",
            options=["Todos"] + meses_disponiveis,
            index=0,
        )
    
    with col2:
        # Filtro de grupo
        grupos_disponiveis = sorted(df[col_grupo].unique().tolist()) if col_grupo in df.columns else []
        grupos_selecionados = st.multiselect(
            "Filtrar por Grupo:",
            options=grupos_disponiveis,
            default=[],
        )
    
    # Aplicar filtros
    df_filtered = df.copy()
    
    if mes_selecionado != "Todos" and col_mes in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[col_mes] == mes_selecionado]
    
    if grupos_selecionados and col_grupo in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[col_grupo].isin(grupos_selecionados)]
    
    st.markdown("---")
    
    # DRE em formato tabular
    st.subheader("📋 Demonstrativo de Resultado")
    
    if col_grupo in df_filtered.columns and col_valor in df_filtered.columns:
        # Agregar por grupo
        dre_table = df_filtered.groupby(col_grupo)[col_valor].sum().reset_index()
        dre_table.columns = ["Grupo", "Valor (R$)"]
        dre_table = dre_table.sort_values("Grupo")
        
        # Formatar valores
        dre_table["Valor Formatado"] = dre_table["Valor (R$)"].apply(
            lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )
        
        # Calcular totais
        total_receitas = dre_table[dre_table["Valor (R$)"] > 0]["Valor (R$)"].sum()
        total_custos = dre_table[dre_table["Valor (R$)"] < 0]["Valor (R$)"].sum()
        resultado = total_receitas + total_custos
        
        # Exibir tabela
        st.dataframe(
            dre_table[["Grupo", "Valor Formatado"]],
            use_container_width=True,
            hide_index=True,
        )
        
        # Totais
        col_t1, col_t2, col_t3 = st.columns(3)
        
        with col_t1:
            st.metric(
                "💚 Total Receitas",
                f"R$ {total_receitas:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            )
        
        with col_t2:
            st.metric(
                "🔴 Total Custos/Despesas",
                f"R$ {abs(total_custos):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            )
        
        with col_t3:
            color = "💚" if resultado >= 0 else "🔴"
            st.metric(
                f"{color} Resultado Líquido",
                f"R$ {resultado:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            )
    
    st.markdown("---")
    
    # Gráfico de barras
    st.subheader("📊 Visualização por Grupo")
    
    if col_grupo in df_filtered.columns and col_valor in df_filtered.columns:
        grupo_chart = df_filtered.groupby(col_grupo)[col_valor].sum().reset_index()
        grupo_chart.columns = ["Grupo", "Valor"]
        grupo_chart = grupo_chart.sort_values("Valor", ascending=True)
        
        fig = create_bar_chart(
            grupo_chart,
            x="Valor",
            y="Grupo",
            title=f"DRE por Grupo - {mes_selecionado}",
            orientation="h",
        )
        
        # Colorir barras por sinal
        fig.update_traces(
            marker_color=[
                "#2ca02c" if v >= 0 else "#d62728" 
                for v in grupo_chart["Valor"]
            ]
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Detalhamento por categoria
    st.markdown("---")
    with st.expander("📋 Detalhamento por Categoria"):
        col_cat = config.COLUMN_CC_NOME
        if col_cat in df_filtered.columns:
            detail = df_filtered.groupby([col_grupo, col_cat])[col_valor].sum().reset_index()
            detail.columns = ["Grupo", "Categoria", "Valor"]
            detail = detail.sort_values(["Grupo", "Valor"], ascending=[True, False])
            
            st.dataframe(detail, use_container_width=True, hide_index=True)

