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
# Template Profissional Plotly - Otimizado para Dark Mode
# =============================================================================

CHART_LAYOUT = {
    "font": {
        "family": "Inter, -apple-system, BlinkMacSystemFont, sans-serif",
        "size": 12,
        "color": COLORS["text_dark"],  # #FAFAFA no dark mode
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
        "bgcolor": "rgba(30, 30, 46, 0.9)",  # Dark mode legend background
        "bordercolor": COLORS["text_muted"],
        "borderwidth": 1,
        "font": {"color": COLORS["text_dark"]},  # Texto claro na legenda
    },
    "hoverlabel": {
        "bgcolor": "#1E1E2E",  # Dark mode hover background
        "font_size": 12,
        "font_color": "#FAFAFA",
        "bordercolor": COLORS["primary"],
    },
    # Eixos otimizados para dark mode
    "xaxis": {
        "gridcolor": "rgba(255, 255, 255, 0.1)",
        "linecolor": "rgba(255, 255, 255, 0.2)",
        "tickcolor": "rgba(255, 255, 255, 0.3)",
        "tickfont": {"color": COLORS["text_muted"]},
    },
    "yaxis": {
        "gridcolor": "rgba(255, 255, 255, 0.1)",
        "linecolor": "rgba(255, 255, 255, 0.2)",
        "tickcolor": "rgba(255, 255, 255, 0.3)",
        "tickfont": {"color": COLORS["text_muted"]},
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
    """Renderiza DataFrame com apariência de planilha.

    Usa ``st.dataframe`` com configuração de colunas numéricas
    formatadas como moeda brasileira (R$).

    Args:
        df: DataFrame para exibir (idealmente com colunas numéricas).
        value_columns: Colunas de valor para formatar como moeda.
        hide_index: Se True, oculta o índice.
    """
    df_display = df.copy()

    column_config: dict[str, st.column_config.Column] = {}

    if value_columns:
        for col in value_columns:
            if col in df_display.columns:
                column_config[col] = st.column_config.NumberColumn(
                    col,
                    format="R$ %,.2f",
                )

    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=hide_index,
        column_config=column_config or None,
    )


# =============================================================================
# Tabela Hierárquica DRE
# =============================================================================

def calculate_rob_percentage(
    value: float,
    rob_total: float,
    decimals: int = 2
) -> str:
    """
    Calcula percentual sobre Receita Operacional Bruta (ROB).

    Args:
        value: Valor da linha.
        rob_total: Total da Receita Operacional Bruta.
        decimals: Casas decimais.

    Returns:
        String formatada com percentual.
    """
    if rob_total == 0 or pd.isna(rob_total) or pd.isna(value):
        return "0,00%"

    percentage = (value / rob_total) * 100
    formatted = f"{percentage:.{decimals}f}".replace(".", ",")
    return f"{formatted}%"


def create_hierarchical_dre_table(
    df: pd.DataFrame,
    group_column: str = "Nome Grupo",
    store_column: str = "Loja",
    value_column: str = "Realizado",
    show_percentages: bool = True,
    max_stores: int = 15,
    format_values: bool = True,
) -> pd.DataFrame:
    """
    Cria tabela DRE hierárquica com colunas por loja.

    Args:
        df: DataFrame com dados DRE.
        group_column: Coluna de grupo/categoria.
        store_column: Coluna de loja.
        value_column: Coluna de valores.
        show_percentages: Se True, adiciona linhas de % ROB.
        max_stores: Número máximo de lojas a exibir.

    Returns:
        DataFrame formatado com estrutura hierárquica e colunas pivotadas.
    """
    # Validar colunas necessárias
    required_cols = [group_column, store_column, value_column]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.error(f"Colunas não encontradas: {', '.join(missing_cols)}")
        return pd.DataFrame()

    # Agregar dados por grupo e loja
    pivot_data = df.groupby([group_column, store_column])[value_column].sum().reset_index()

    # Criar tabela pivotada
    pivot_table = pivot_data.pivot_table(
        index=group_column,
        columns=store_column,
        values=value_column,
        aggfunc='sum',
        fill_value=0
    )

    # Limitar número de lojas
    if len(pivot_table.columns) > max_stores:
        # Selecionar top lojas por receita total
        store_totals = pivot_table.sum().sort_values(ascending=False)
        top_stores = store_totals.head(max_stores).index.tolist()
        pivot_table = pivot_table[top_stores]

    # Adicionar coluna Total Mês
    pivot_table.insert(0, 'Total Mês', pivot_table.sum(axis=1))

    # Resetar índice para ter "Conta" como coluna
    pivot_table = pivot_table.reset_index()
    pivot_table = pivot_table.rename(columns={group_column: 'Conta'})

    # Opcionalmente formatar valores como moeda para exibição direta
    if format_values:
        value_cols = [col for col in pivot_table.columns if col != 'Conta']
        for col in value_cols:
            pivot_table[col] = pivot_table[col].apply(
                lambda x: format_currency(x) if pd.notna(x) else "R$ 0,00"
            )

    return pivot_table


def create_styled_dre_html_table(
    df: pd.DataFrame,
    group_column: str = "Nome Grupo",
    store_column: str = "Loja",
    value_column: str = "Realizado",
    max_stores: int = 15,
    height: int = 500,
) -> None:
    """
    Renderiza tabela DRE estilizada com HTML/CSS customizado.

    Inclui:
    - Zebra striping para facilitar leitura
    - Destaque visual para linhas de totalizadores
    - Valores negativos em vermelho
    - Formatação de moeda brasileira (R$ 1.234,56)
    - Coluna "Conta" fixa à esquerda
    - Cabeçalho fixo ao rolar verticalmente

    Args:
        df: DataFrame com dados DRE.
        group_column: Coluna de grupo/categoria.
        store_column: Coluna de loja.
        value_column: Coluna de valores.
        max_stores: Número máximo de lojas a exibir.
        height: Altura máxima da tabela em pixels.
    """
    # Validar colunas necessárias
    required_cols = [group_column, store_column, value_column]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.error(f"Colunas não encontradas: {', '.join(missing_cols)}")
        return

    # Agregar dados por grupo e loja
    pivot_data = df.groupby([group_column, store_column])[value_column].sum().reset_index()

    # Criar tabela pivotada
    pivot_table = pivot_data.pivot_table(
        index=group_column,
        columns=store_column,
        values=value_column,
        aggfunc='sum',
        fill_value=0
    )

    # Limitar número de lojas
    if len(pivot_table.columns) > max_stores:
        store_totals = pivot_table.sum().sort_values(ascending=False)
        top_stores = store_totals.head(max_stores).index.tolist()
        pivot_table = pivot_table[top_stores]

    # Adicionar coluna Total Mês
    pivot_table.insert(0, 'Total Mês', pivot_table.sum(axis=1))

    # Resetar índice
    pivot_table = pivot_table.reset_index()
    pivot_table = pivot_table.rename(columns={group_column: 'Conta'})

    # Palavras-chave para identificar tipos de linha
    totalizadores = [
        'RECEITA LÍQUIDA', 'RECEITA LIQUIDA', 'RESULTADO BRUTO',
        'RESULTADO OPERACIONAL', 'LUCRO LÍQUIDO', 'LUCRO LIQUIDO',
        'LUCRO BRUTO', 'EBITDA', 'RESULTADO ANTES', 'RESULTADO FINAL',
        'TOTAL', 'SUBTOTAL'
    ]
    resultados = [
        'LUCRO LÍQUIDO', 'LUCRO LIQUIDO', 'RESULTADO FINAL',
        'RESULTADO DO EXERCÍCIO', 'RESULTADO DO EXERCICIO'
    ]
    receitas = ['RECEITA', 'VENDA', 'FATURAMENTO', 'ROB']
    custos = [
        '( - )', '(-)', 'CUSTO', 'DESPESA', 'GASTO', 'DEDUCAO',
        'DEDUÇÃO', 'IMPOSTO', 'SERVIÇO', 'SERVICO'
    ]

    def classify_row(conta: str) -> str:
        """Classifica o tipo de linha baseado no nome da conta."""
        conta_upper = str(conta).upper()
        for r in resultados:
            if r in conta_upper:
                return 'result'
        for t in totalizadores:
            if t in conta_upper:
                return 'total'
        for rec in receitas:
            if rec in conta_upper and not any(c in conta_upper for c in custos):
                return 'receita'
        for c in custos:
            if c in conta_upper:
                return 'custo'
        return 'normal'

    def format_value_html(value: float) -> str:
        """Formata valor como moeda brasileira com classe CSS."""
        if pd.isna(value):
            value = 0.0
        # Formatar como moeda brasileira
        abs_val = abs(value)
        formatted = f"R$ {abs_val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        if value < 0:
            return f'<span class="valor-negativo">({formatted})</span>'
        return f'<span class="valor-positivo">{formatted}</span>'

    # Construir HTML da tabela
    html_parts = ['<div class="dre-styled-container" style="max-height: {}px; overflow-y: auto;">'.format(height)]
    html_parts.append('<table class="dre-styled-table">')

    # Cabeçalho
    html_parts.append('<thead><tr>')
    for col in pivot_table.columns:
        html_parts.append(f'<th>{col}</th>')
    html_parts.append('</tr></thead>')

    # Corpo da tabela
    html_parts.append('<tbody>')
    for _, row in pivot_table.iterrows():
        conta = row['Conta']
        row_type = classify_row(conta)

        # Definir classe CSS da linha
        row_class = ''
        if row_type == 'result':
            row_class = 'dre-result-row'
        elif row_type == 'total':
            row_class = 'dre-total-row'
        elif row_type == 'receita':
            row_class = 'dre-receita-row'
        elif row_type == 'custo':
            row_class = 'dre-custo-row'

        html_parts.append(f'<tr class="{row_class}">')

        for col in pivot_table.columns:
            if col == 'Conta':
                html_parts.append(f'<td>{row[col]}</td>')
            else:
                html_parts.append(f'<td>{format_value_html(row[col])}</td>')

        html_parts.append('</tr>')

    html_parts.append('</tbody>')
    html_parts.append('</table>')
    html_parts.append('</div>')

    # Renderizar
    st.markdown(''.join(html_parts), unsafe_allow_html=True)


def render_store_filter(
    df: pd.DataFrame,
    store_column: str = "Loja",
    key: str = "store_filter",
    label: str = "Filtrar por Loja(s)"
) -> list[str]:
    """
    Renderiza filtro de seleção de lojas.

    Args:
        df: DataFrame com dados DRE.
        store_column: Nome da coluna de loja.
        key: Chave única para o widget.
        label: Label do filtro.

    Returns:
        Lista de lojas selecionadas.
    """
    from dashboard.components.data_loader import get_unique_stores

    stores = get_unique_stores(df, store_column)

    if not stores:
        st.warning(f"Coluna '{store_column}' não encontrada ou vazia.")
        return []

    col1, col2 = st.columns([3, 1])

    with col1:
        selected_stores = st.multiselect(
            label,
            options=stores,
            default=stores,  # Todas selecionadas por padrão
            key=key,
        )

    with col2:
        if st.button("Limpar Filtros", key=f"{key}_clear"):
            st.session_state[key] = stores
            st.rerun()

    return selected_stores if selected_stores else stores

