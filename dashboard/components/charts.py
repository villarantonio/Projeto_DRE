"""
Componentes de gráficos para o Dashboard Manda Picanha.

Fornece funções para criar gráficos Plotly reutilizáveis
com template profissional e formatação brasileira.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from dashboard.components.styles import COLORS, CHART_COLORS, format_currency


# =============================================================================
# Template Profissional Plotly
# =============================================================================

CHART_LAYOUT = {
    "font": {
        "family": "Inter, -apple-system, BlinkMacSystemFont, sans-serif",
        "size": 12,
        "color": COLORS["text_dark"],
    },
    "title": {
        "font": {"size": 16, "color": COLORS["text_dark"], "weight": 600},
        "x": 0,
        "xanchor": "left",
    },
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "margin": {"l": 40, "r": 20, "t": 50, "b": 40},
    "legend": {
        "orientation": "h",
        "yanchor": "bottom",
        "y": -0.2,
        "xanchor": "center",
        "x": 0.5,
        "bgcolor": "rgba(255,255,255,0.8)",
        "bordercolor": COLORS["text_muted"],
        "borderwidth": 1,
    },
    "hoverlabel": {
        "bgcolor": COLORS["secondary"],
        "font_size": 12,
        "font_color": "white",
        "bordercolor": COLORS["secondary"],
    },
}


# =============================================================================
# Funções Auxiliares
# =============================================================================

def _apply_layout(fig: go.Figure, title: str = "", show_legend: bool = True) -> go.Figure:
    """Aplica layout padrão ao gráfico."""
    layout = CHART_LAYOUT.copy()
    layout["title"]["text"] = title
    layout["showlegend"] = show_legend
    fig.update_layout(**layout)
    return fig


def _format_hover_value(value: float) -> str:
    """Formata valor para hover tooltip."""
    return format_currency(value)


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
    color_positive: str = None,
    color_negative: str = None,
) -> go.Figure:
    """
    Cria gráfico de barras profissional.

    Args:
        df: DataFrame com dados.
        x: Coluna para eixo X.
        y: Coluna para eixo Y.
        title: Título do gráfico.
        color: Coluna para cores.
        orientation: 'v' (vertical) ou 'h' (horizontal).
        text_auto: Mostrar valores nas barras.
        color_positive: Cor para valores positivos.
        color_negative: Cor para valores negativos.

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
        color_discrete_sequence=CHART_COLORS,
    )

    # Aplicar cores por sinal se especificado
    if color_positive and color_negative and color is None:
        value_col = y if orientation == "v" else x
        colors = [
            color_positive if v >= 0 else color_negative
            for v in df[value_col]
        ]
        fig.update_traces(marker_color=colors)

    # Layout profissional
    _apply_layout(fig, title, show_legend=color is not None)

    # Customizações específicas de barra
    fig.update_traces(
        textposition="outside",
        textfont={"size": 11, "color": COLORS["text_dark"]},
        hovertemplate="<b>%{y}</b><br>Valor: %{x:,.2f}<extra></extra>" if orientation == "h"
                      else "<b>%{x}</b><br>Valor: %{y:,.2f}<extra></extra>",
    )

    # Grid sutil
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0,0,0,0.05)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0,0,0,0.05)")

    return fig


def create_line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: str | None = None,
    markers: bool = True,
    fill_area: bool = False,
) -> go.Figure:
    """
    Cria gráfico de linhas profissional.

    Args:
        df: DataFrame com dados.
        x: Coluna para eixo X.
        y: Coluna para eixo Y.
        title: Título do gráfico.
        color: Coluna para séries múltiplas.
        markers: Mostrar marcadores nos pontos.
        fill_area: Preencher área sob a linha.

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
        color_discrete_sequence=CHART_COLORS,
    )

    # Layout profissional
    _apply_layout(fig, title, show_legend=color is not None)

    # Customizações específicas de linha
    fig.update_traces(
        line={"width": 3},
        marker={"size": 8, "line": {"width": 2, "color": "white"}},
        hovertemplate="<b>%{x}</b><br>Valor: R$ %{y:,.2f}<extra></extra>",
    )

    if fill_area:
        fig.update_traces(fill="tozeroy", fillcolor=f"rgba(196, 30, 58, 0.1)")

    # Grid sutil
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0,0,0,0.05)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0,0,0,0.05)")
    fig.update_layout(hovermode="x unified")

    return fig


def create_pie_chart(
    df: pd.DataFrame,
    values: str,
    names: str,
    title: str = "",
    hole: float = 0.45,
) -> go.Figure:
    """
    Cria gráfico de pizza/donut profissional.

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
        color_discrete_sequence=CHART_COLORS,
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        textfont={"size": 11, "color": "white"},
        hovertemplate="<b>%{label}</b><br>Valor: R$ %{value:,.2f}<br>Percentual: %{percent}<extra></extra>",
        marker={"line": {"color": "white", "width": 2}},
    )

    _apply_layout(fig, title, show_legend=True)
    fig.update_layout(
        legend={"orientation": "v", "yanchor": "middle", "y": 0.5, "xanchor": "left", "x": 1.02},
    )

    return fig


def create_treemap(
    df: pd.DataFrame,
    path: list[str],
    values: str,
    title: str = "",
) -> go.Figure:
    """
    Cria gráfico treemap hierárquico profissional.

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
        color_discrete_sequence=CHART_COLORS,
    )

    fig.update_traces(
        textinfo="label+value+percent entry",
        textfont={"size": 12},
        hovertemplate="<b>%{label}</b><br>Valor: R$ %{value:,.2f}<br>Percentual: %{percentEntry:.1%}<extra></extra>",
        marker={"line": {"width": 1, "color": "white"}},
    )

    _apply_layout(fig, title, show_legend=False)
    fig.update_layout(margin={"l": 10, "r": 10, "t": 50, "b": 10})

    return fig


def create_kpi_card(
    value: float | int,
    label: str,
    delta: float | None = None,
    delta_color: str = "normal",
    prefix: str = "",
    suffix: str = "",
    icon: str = "",
) -> None:
    """
    Renderiza card de KPI profissional usando st.metric.

    Args:
        value: Valor principal.
        label: Label do KPI.
        delta: Variação percentual (opcional).
        delta_color: Cor do delta ('normal', 'inverse', 'off').
        prefix: Prefixo do valor (ex: 'R$ ').
        suffix: Sufixo do valor (ex: '%').
        icon: Emoji/ícone para o label (opcional).
    """
    # Formatar valor no padrão brasileiro
    if isinstance(value, float):
        if abs(value) >= 1_000_000:
            # Formato: R$ 1,23M
            formatted = f"{value/1_000_000:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            display_value = f"{prefix}{formatted}M{suffix}"
        elif abs(value) >= 1_000:
            # Formato: R$ 123,4K
            formatted = f"{value/1_000:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
            display_value = f"{prefix}{formatted}K{suffix}"
        else:
            # Formato: R$ 123,45
            formatted = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            display_value = f"{prefix}{formatted}{suffix}"
    else:
        # Formato inteiro: 1.234
        formatted = f"{value:,}".replace(",", ".")
        display_value = f"{prefix}{formatted}{suffix}"

    # Formatar delta com vírgula decimal
    delta_str = None
    if delta is not None:
        delta_formatted = f"{delta:+.1f}".replace(".", ",")
        delta_str = f"{delta_formatted}%"

    # Label com ícone
    full_label = f"{icon} {label}" if icon else label

    st.metric(
        label=full_label,
        value=display_value,
        delta=delta_str,
        delta_color=delta_color,
    )


# =============================================================================
# Componentes de Tabela
# =============================================================================

def create_styled_dataframe(
    df: pd.DataFrame,
    value_columns: list[str] | None = None,
    hide_index: bool = True,
) -> None:
    """
    Renderiza DataFrame com formatação profissional.

    Args:
        df: DataFrame para exibir.
        value_columns: Colunas de valor para formatar como moeda.
        hide_index: Ocultar índice.
    """
    df_display = df.copy()

    # Formatar colunas de valor
    if value_columns:
        for col in value_columns:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(
                    lambda x: format_currency(x) if pd.notna(x) else "-"
                )

    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=hide_index,
    )

