"""
Componentes de gráficos para o Dashboard.

Fornece funções para criar gráficos Plotly reutilizáveis
para visualização de dados DRE.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# =============================================================================
# Paleta de Cores
# =============================================================================

COLORS = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "success": "#2ca02c",
    "danger": "#d62728",
    "warning": "#bcbd22",
    "info": "#17becf",
    "receitas": "#2ca02c",
    "custos": "#d62728",
    "despesas": "#ff7f0e",
}

COLOR_SEQUENCE = px.colors.qualitative.Set2


# =============================================================================
# Gráficos
# =============================================================================

def create_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: str | None = None,
    orientation: str = "v",
    text_auto: bool = True,
) -> go.Figure:
    """
    Cria gráfico de barras.
    
    Args:
        df: DataFrame com dados.
        x: Coluna para eixo X.
        y: Coluna para eixo Y.
        title: Título do gráfico.
        color: Coluna para cores.
        orientation: 'v' (vertical) ou 'h' (horizontal).
        text_auto: Mostrar valores nas barras.
        
    Returns:
        Figura Plotly.
    """
    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        color=color,
        orientation=orientation,
        text_auto=".2s" if text_auto else False,
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial", size=12),
        title_font_size=16,
        showlegend=color is not None,
    )
    
    fig.update_traces(textposition="outside")
    
    return fig


def create_line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: str | None = None,
    markers: bool = True,
) -> go.Figure:
    """
    Cria gráfico de linhas.
    
    Args:
        df: DataFrame com dados.
        x: Coluna para eixo X.
        y: Coluna para eixo Y.
        title: Título do gráfico.
        color: Coluna para séries múltiplas.
        markers: Mostrar marcadores nos pontos.
        
    Returns:
        Figura Plotly.
    """
    fig = px.line(
        df,
        x=x,
        y=y,
        title=title,
        color=color,
        markers=markers,
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial", size=12),
        title_font_size=16,
        hovermode="x unified",
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="lightgray")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="lightgray")
    
    return fig


def create_pie_chart(
    df: pd.DataFrame,
    values: str,
    names: str,
    title: str = "",
    hole: float = 0.4,
) -> go.Figure:
    """
    Cria gráfico de pizza/donut.
    
    Args:
        df: DataFrame com dados.
        values: Coluna com valores.
        names: Coluna com labels.
        title: Título do gráfico.
        hole: Tamanho do buraco (0 = pizza, >0 = donut).
        
    Returns:
        Figura Plotly.
    """
    fig = px.pie(
        df,
        values=values,
        names=names,
        title=title,
        hole=hole,
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
    )
    
    fig.update_layout(
        font=dict(family="Arial", size=12),
        title_font_size=16,
    )
    
    return fig


def create_treemap(
    df: pd.DataFrame,
    path: list[str],
    values: str,
    title: str = "",
) -> go.Figure:
    """
    Cria gráfico treemap hierárquico.
    
    Args:
        df: DataFrame com dados.
        path: Lista de colunas para hierarquia.
        values: Coluna com valores.
        title: Título do gráfico.
        
    Returns:
        Figura Plotly.
    """
    fig = px.treemap(
        df,
        path=path,
        values=values,
        title=title,
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    
    fig.update_layout(
        font=dict(family="Arial", size=12),
        title_font_size=16,
    )
    
    return fig


def create_kpi_card(
    value: float | int,
    label: str,
    delta: float | None = None,
    delta_color: str = "normal",
    prefix: str = "",
    suffix: str = "",
) -> None:
    """
    Renderiza card de KPI usando st.metric.
    
    Args:
        value: Valor principal.
        label: Label do KPI.
        delta: Variação (opcional).
        delta_color: Cor do delta ('normal', 'inverse', 'off').
        prefix: Prefixo do valor (ex: 'R$ ').
        suffix: Sufixo do valor (ex: '%').
    """
    # Formatar valor
    if isinstance(value, float):
        if abs(value) >= 1_000_000:
            display_value = f"{prefix}{value/1_000_000:.2f}M{suffix}"
        elif abs(value) >= 1_000:
            display_value = f"{prefix}{value/1_000:.1f}K{suffix}"
        else:
            display_value = f"{prefix}{value:.2f}{suffix}"
    else:
        display_value = f"{prefix}{value:,}{suffix}"
    
    # Formatar delta
    delta_str = None
    if delta is not None:
        delta_str = f"{delta:+.1f}%"
    
    st.metric(
        label=label,
        value=display_value,
        delta=delta_str,
        delta_color=delta_color,
    )

