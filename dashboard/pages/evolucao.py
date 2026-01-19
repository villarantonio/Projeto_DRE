"""
Página de Evolução Temporal do Dashboard.

Exibe gráficos de série temporal dos dados DRE.
"""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

import config
from dashboard.components.charts import create_line_chart, create_bar_chart


def render_evolucao(df: pd.DataFrame, categories: dict) -> None:
    """
    Renderiza página de evolução temporal.
    
    Args:
        df: DataFrame com dados DRE.
        categories: Dicionário de categorias.
    """
    st.header("📉 Evolução Temporal")
    st.markdown("Análise de tendências e variações ao longo do tempo.")
    
    col_mes = config.COLUMN_MES
    col_grupo = config.COLUMN_NOME_GRUPO
    col_valor = config.COLUMN_REALIZADO
    
    # Filtros
    col1, col2 = st.columns(2)
    
    with col1:
        grupos_disponiveis = sorted(df[col_grupo].unique().tolist()) if col_grupo in df.columns else []
        grupos_selecionados = st.multiselect(
            "Selecione os Grupos:",
            options=grupos_disponiveis,
            default=grupos_disponiveis[:3] if len(grupos_disponiveis) >= 3 else grupos_disponiveis,
        )
    
    with col2:
        tipo_visualizacao = st.radio(
            "Tipo de Visualização:",
            options=["Linha", "Barras Empilhadas"],
            horizontal=True,
        )
    
    st.markdown("---")
    
    # Preparar dados
    if col_mes in df.columns and col_grupo in df.columns and col_valor in df.columns:
        df_filtered = df.copy()
        
        if grupos_selecionados:
            df_filtered = df_filtered[df_filtered[col_grupo].isin(grupos_selecionados)]
        
        # Agregar por mês e grupo
        evolucao = df_filtered.groupby([col_mes, col_grupo])[col_valor].sum().reset_index()
        evolucao.columns = ["Mês", "Grupo", "Valor"]
        
        # Ordenar meses
        ordem_meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", 
                       "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        evolucao["Mês"] = pd.Categorical(
            evolucao["Mês"], 
            categories=[m for m in ordem_meses if m in evolucao["Mês"].unique()],
            ordered=True
        )
        evolucao = evolucao.sort_values("Mês")
        
        # Gráfico principal
        st.subheader("📈 Evolução por Grupo")
        
        if tipo_visualizacao == "Linha":
            fig = create_line_chart(
                evolucao,
                x="Mês",
                y="Valor",
                title="Evolução Mensal por Grupo",
                color="Grupo",
            )
        else:
            fig = create_bar_chart(
                evolucao,
                x="Mês",
                y="Valor",
                title="Evolução Mensal por Grupo",
                color="Grupo",
            )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Evolução total
        st.markdown("---")
        st.subheader("📊 Evolução do Resultado Total")
        
        total_mensal = df.groupby(col_mes)[col_valor].sum().reset_index()
        total_mensal.columns = ["Mês", "Resultado"]
        total_mensal["Mês"] = pd.Categorical(
            total_mensal["Mês"],
            categories=[m for m in ordem_meses if m in total_mensal["Mês"].unique()],
            ordered=True
        )
        total_mensal = total_mensal.sort_values("Mês")
        
        fig_total = create_line_chart(
            total_mensal,
            x="Mês",
            y="Resultado",
            title="Resultado Total por Mês",
        )
        
        # Colorir linha baseado no sinal
        fig_total.update_traces(
            line=dict(width=3),
            fill="tozeroy",
            fillcolor="rgba(44, 160, 44, 0.2)",
        )
        
        st.plotly_chart(fig_total, use_container_width=True)
        
        # Variação percentual
        st.markdown("---")
        st.subheader("📈 Variação Percentual Mensal")
        
        total_mensal["Variação %"] = total_mensal["Resultado"].pct_change() * 100
        total_mensal["Variação %"] = total_mensal["Variação %"].fillna(0).round(2)
        
        col_v1, col_v2 = st.columns(2)
        
        with col_v1:
            st.dataframe(
                total_mensal[["Mês", "Resultado", "Variação %"]],
                use_container_width=True,
                hide_index=True,
            )
        
        with col_v2:
            # Métricas de variação
            var_media = total_mensal["Variação %"].mean()
            var_max = total_mensal["Variação %"].max()
            var_min = total_mensal["Variação %"].min()
            
            st.metric("Variação Média", f"{var_media:.1f}%")
            st.metric("Maior Variação", f"{var_max:.1f}%")
            st.metric("Menor Variação", f"{var_min:.1f}%")
    
    else:
        st.warning("Colunas necessárias não encontradas no dataset.")

