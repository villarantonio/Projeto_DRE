"""
Página de Visão Geral do Dashboard.

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
)
from dashboard.components.data_loader import get_summary_stats


def render_overview(df: pd.DataFrame, categories: dict) -> None:
    """
    Renderiza página de visão geral.
    
    Args:
        df: DataFrame com dados DRE.
        categories: Dicionário de categorias.
    """
    st.header("📊 Visão Geral")
    st.markdown("Resumo executivo dos dados financeiros DRE.")
    
    # Estatísticas
    stats = get_summary_stats(df)
    
    # KPIs principais
    st.subheader("📈 Indicadores Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_kpi_card(
            value=stats["total_registros"],
            label="Total de Registros",
            prefix="",
            suffix=" itens",
        )
    
    with col2:
        create_kpi_card(
            value=stats["receitas"],
            label="Receitas Totais",
            prefix="R$ ",
            delta=5.2,  # Placeholder - calcular variação real
        )
    
    with col3:
        create_kpi_card(
            value=stats["custos"],
            label="Custos Totais",
            prefix="R$ ",
            delta=-3.1,  # Placeholder
            delta_color="inverse",
        )
    
    with col4:
        create_kpi_card(
            value=stats["margem"],
            label="Margem",
            suffix="%",
            delta=2.5,  # Placeholder
        )
    
    st.markdown("---")
    
    # Gráficos resumo
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("💰 Receitas vs Custos por Grupo")
        
        # Agregar por grupo
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
                title="Total por Grupo DRE",
                orientation="h",
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.subheader("📊 Distribuição de Categorias")
        
        # Contar categorias por grupo
        if categories:
            cat_counts = pd.DataFrame([
                {"Grupo": grupo, "Categorias": len(cats)}
                for grupo, cats in categories.items()
            ])
            
            fig = create_pie_chart(
                cat_counts,
                values="Categorias",
                names="Grupo",
                title="Categorias por Grupo",
                hole=0.4,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Categorias não disponíveis.")
    
    # Tabela de dados recentes
    st.markdown("---")
    st.subheader("📋 Últimos Registros")
    
    # Mostrar últimas 10 linhas
    display_cols = [
        col for col in [config.COLUMN_NOME_GRUPO, config.COLUMN_CC_NOME, 
                        config.COLUMN_MES, config.COLUMN_REALIZADO]
        if col in df.columns
    ]
    
    if display_cols:
        st.dataframe(
            df[display_cols].tail(10),
            use_container_width=True,
            hide_index=True,
        )
    
    # Info adicional
    st.markdown("---")
    with st.expander("ℹ️ Informações do Dataset"):
        st.write(f"**Arquivo:** `{config.PROCESSED_PARQUET_PATH}`")
        st.write(f"**Total de colunas:** {len(df.columns)}")
        st.write(f"**Colunas:** {', '.join(df.columns.tolist())}")
        st.write(f"**Grupos únicos:** {stats['total_grupos']}")

