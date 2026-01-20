"""
Pagina de Previsoes Financeiras com Prophet.

Exibe previsoes de receita e custos para os proximos meses,
com avisos sobre limitacoes do modelo simplificado.
"""

import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Imports do projeto
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dashboard.components.styles import (
    COLORS,
    format_currency,
    render_section_header,
)

try:
    from src.forecaster import DREForecaster, ForecastResult
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False


def create_forecast_chart(
    result: "ForecastResult",
    historical_df: pd.DataFrame,
) -> go.Figure:
    """
    Cria grafico de previsao com historico e intervalos de confianca.
    
    Args:
        result: Resultado da previsao.
        historical_df: Dados historicos.
        
    Returns:
        Figura Plotly.
    """
    forecast = result.forecast_df
    
    # Separar historico e futuro
    last_date = historical_df["ds"].max()
    historical_forecast = forecast[forecast["ds"] <= last_date]
    future_forecast = forecast[forecast["ds"] > last_date]
    
    fig = go.Figure()
    
    # Intervalo de confianca (futuro)
    fig.add_trace(go.Scatter(
        x=pd.concat([future_forecast["ds"], future_forecast["ds"][::-1]]),
        y=pd.concat([future_forecast["yhat_upper"], future_forecast["yhat_lower"][::-1]]),
        fill="toself",
        fillcolor="rgba(52, 152, 219, 0.2)",
        line=dict(color="rgba(255,255,255,0)"),
        name="Intervalo 80%",
        hoverinfo="skip",
    ))
    
    # Valores reais (historico)
    fig.add_trace(go.Scatter(
        x=historical_df["ds"],
        y=historical_df["y"],
        mode="lines+markers",
        name="Realizado",
        line=dict(color=COLORS["primary"], width=3),
        marker=dict(size=8),
    ))
    
    # Previsao ajustada (historico)
    fig.add_trace(go.Scatter(
        x=historical_forecast["ds"],
        y=historical_forecast["yhat"],
        mode="lines",
        name="Modelo Ajustado",
        line=dict(color=COLORS["secondary"], width=2, dash="dot"),
    ))
    
    # Previsao futura
    fig.add_trace(go.Scatter(
        x=future_forecast["ds"],
        y=future_forecast["yhat"],
        mode="lines+markers",
        name="Previsao",
        line=dict(color=COLORS["success"], width=3),
        marker=dict(size=10, symbol="diamond"),
    ))
    
    # Layout
    fig.update_layout(
        title=dict(
            text=f"Previsao: {result.grupo}",
            font=dict(size=18),
        ),
        xaxis_title="Periodo",
        yaxis_title="Valor (R$)",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        plot_bgcolor="white",
        height=450,
    )
    
    # Linha vertical separando historico/futuro
    fig.add_vline(
        x=last_date,
        line_dash="dash",
        line_color="gray",
        annotation_text="Inicio Previsao",
        annotation_position="top",
    )
    
    return fig


def create_metrics_cards(result: "ForecastResult") -> None:
    """Exibe cards com metricas da previsao."""
    metrics = result.metrics
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Meses Historico",
            f"{metrics['meses_historico']}",
            delta="-12 vs recomendado" if metrics["meses_historico"] < 24 else None,
            delta_color="off",
        )
    
    with col2:
        st.metric(
            "Meses Previsao",
            f"{metrics['meses_previsao']}",
        )
    
    with col3:
        tendencia = metrics["tendencia"]
        icon = "alta" if tendencia == "alta" else ("baixa" if tendencia == "baixa" else "->")
        st.metric(
            "Tendencia",
            tendencia.upper(),
            delta=icon,
            delta_color="normal" if tendencia == "alta" else "inverse",
        )
    
    with col4:
        if metrics["proxima_previsao"]:
            st.metric(
                "Proxima Previsao",
                format_currency(metrics["proxima_previsao"]),
            )


def create_forecast_table(result: "ForecastResult", historical_df: pd.DataFrame) -> pd.DataFrame:
    """Cria tabela com previsoes formatadas."""
    forecast = result.forecast_df
    last_date = historical_df["ds"].max()
    future = forecast[forecast["ds"] > last_date].copy()

    future["Mes"] = future["ds"].dt.strftime("%b/%Y")
    future["Previsao"] = future["yhat"].apply(format_currency)
    future["Minimo (80%)"] = future["yhat_lower"].apply(format_currency)
    future["Maximo (80%)"] = future["yhat_upper"].apply(format_currency)

    return future[["Mes", "Previsao", "Minimo (80%)", "Maximo (80%)"]]


def render_warnings(result: "ForecastResult") -> None:
    """Exibe avisos sobre limitacoes do modelo."""
    if result.warnings:
        st.warning(
            "**Aviso de Precisao Limitada**\n\n" +
            "\n".join([f"- {w}" for w in result.warnings])
        )


def render() -> None:
    """Renderiza a pagina de previsoes."""
    render_section_header(
        "Previsoes Financeiras",
        "Projecao de receitas e custos com Facebook Prophet",
    )

    # Verificar se Prophet esta disponivel
    if not PROPHET_AVAILABLE:
        st.error(
            "**Prophet nao instalado**\n\n"
            "Execute: `pip install prophet` para habilitar previsoes."
        )
        return

    # Disclaimer principal
    st.info(
        "**Modelo Simplificado** - Este previsor usa apenas 12 meses de historico. "
        "Para previsoes mais precisas, sao recomendados 24+ meses de dados. "
        "Use os resultados como **indicativo**, nao como valores exatos."
    )

    # Configuracoes
    st.sidebar.markdown("---")
    st.sidebar.subheader("Configuracoes de Previsao")

    periods = st.sidebar.slider(
        "Meses a prever",
        min_value=1,
        max_value=12,
        value=6,
        help="Numero de meses futuros para projetar",
    )

    try:
        # Carregar forecaster
        forecaster = DREForecaster()
        forecaster.load_data()

        grupos = ["TODOS"] + forecaster.get_grupos_disponiveis()

        selected_grupo = st.sidebar.selectbox(
            "Grupo DRE",
            grupos,
            help="Selecione um grupo para previsao especifica",
        )

        grupo_param = None if selected_grupo == "TODOS" else selected_grupo

        # Botao para gerar previsao
        if st.sidebar.button("Gerar Previsao", type="primary", use_container_width=True):
            with st.spinner("Treinando modelo Prophet..."):
                result = forecaster.forecast(periods=periods, grupo=grupo_param)
                st.session_state["forecast_result"] = result
                st.session_state["forecast_historical"] = forecaster.prepare_prophet_data(grupo=grupo_param)

        # Exibir resultado se existir
        if "forecast_result" in st.session_state:
            result = st.session_state["forecast_result"]
            historical = st.session_state["forecast_historical"]

            # Warnings
            render_warnings(result)

            # Metricas
            st.markdown("### Metricas do Modelo")
            create_metrics_cards(result)

            st.markdown("---")

            # Grafico
            st.markdown("### Grafico de Previsao")
            fig = create_forecast_chart(result, historical)
            st.plotly_chart(fig, use_container_width=True)

            # Tabela de previsoes
            st.markdown("### Previsoes Detalhadas")
            table = create_forecast_table(result, historical)
            st.dataframe(table, use_container_width=True, hide_index=True)

        else:
            st.info("Clique em **Gerar Previsao** na barra lateral para iniciar.")

    except FileNotFoundError:
        st.error(
            "**Dados nao encontrados**\n\n"
            "Execute primeiro o pipeline principal (`python main.py`) "
            "para gerar os dados processados."
        )
    except Exception as e:
        st.error(f"**Erro ao gerar previsao:** {e}")

