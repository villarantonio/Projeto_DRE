"""
Modulo de Previsao Financeira com Prophet.

Implementa previsoes de receita e custos usando Facebook Prophet,
otimizado para funcionar com apenas 12 meses de dados historicos.

AVISO: Previsoes com menos de 24 meses de historico tem precisao reduzida.
       Use os resultados como indicativo, nao como valores exatos.

Author: Projeto DRE - Manda Picanha
Version: 1.0.0 (Modelo Simplificado)
"""

import logging
import sys
import warnings
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

# Suprimir warnings do Prophet/cmdstanpy
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*cmdstan.*")

try:
    from prophet import Prophet
except ImportError:
    Prophet = None

# Import config
try:
    import config
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    import config

logger = logging.getLogger(__name__)


# Constantes
MIN_MONTHS_RECOMMENDED = 24
MIN_MONTHS_REQUIRED = 6
DEFAULT_FORECAST_PERIODS = 6


@dataclass
class ForecastResult:
    """Resultado de uma previsao."""
    
    categoria: str
    grupo: str
    forecast_df: pd.DataFrame
    metrics: dict[str, Any]
    warnings: list[str]


class DREForecaster:
    """
    Previsor de series temporais para dados DRE.
    
    Usa Facebook Prophet otimizado para historico curto (12 meses).
    Inclui avisos sobre limitacoes de precisao.
    """
    
    def __init__(self, data_path: Path | None = None):
        """
        Inicializa o previsor.
        
        Args:
            data_path: Caminho para o parquet processado.
        """
        if Prophet is None:
            raise ImportError(
                "Prophet nao instalado. Execute: pip install prophet"
            )
        
        self.data_path = data_path or config.OUTPUT_DIR / "processed_dre.parquet"
        self.df: pd.DataFrame | None = None
        self.warnings: list[str] = []
        
    def load_data(self) -> pd.DataFrame:
        """Carrega dados do parquet processado."""
        if not self.data_path.exists():
            raise FileNotFoundError(f"Arquivo nao encontrado: {self.data_path}")
        
        self.df = pd.read_parquet(self.data_path)
        
        # Verificar quantidade de meses
        mes_col = "Mes" if "Mes" in self.df.columns else "Mês"
        n_months = self.df[mes_col].nunique()
        
        if n_months < MIN_MONTHS_REQUIRED:
            raise ValueError(
                f"Dados insuficientes: {n_months} meses. Minimo: {MIN_MONTHS_REQUIRED}"
            )
        
        if n_months < MIN_MONTHS_RECOMMENDED:
            self.warnings.append(
                f"AVISO: Historico de {n_months} meses (recomendado: {MIN_MONTHS_RECOMMENDED}). "
                "Previsoes terao precisao reduzida."
            )
        
        logger.info(f"Dados carregados: {len(self.df)} registros, {n_months} meses")
        return self.df
    
    def prepare_prophet_data(
        self,
        grupo: str | None = None,
        categoria: str | None = None,
    ) -> pd.DataFrame:
        """
        Prepara dados no formato Prophet (ds, y).
        
        Args:
            grupo: Filtrar por grupo DRE.
            categoria: Filtrar por categoria especifica.
            
        Returns:
            DataFrame com colunas ds (data) e y (valor).
        """
        if self.df is None:
            self.load_data()
        
        df = self.df.copy()
        mes_col = "Mes" if "Mes" in df.columns else "Mês"
        valor_col = "Realizado"
        
        # Aplicar filtros
        if grupo:
            df = df[df["Nome Grupo"] == grupo]
        if categoria:
            df = df[df["cc_nome"] == categoria]
        
        # Agregar por mes
        monthly = df.groupby(mes_col)[valor_col].sum().reset_index()
        monthly.columns = ["ds", "y"]
        monthly["ds"] = pd.to_datetime(monthly["ds"])
        monthly = monthly.sort_values("ds")
        
        return monthly

    def create_model(self, yearly_seasonality: bool = True) -> Prophet:
        """
        Cria modelo Prophet otimizado para historico curto.

        Args:
            yearly_seasonality: Usar sazonalidade anual.

        Returns:
            Modelo Prophet configurado.
        """
        model = Prophet(
            # Configuracoes para historico curto
            yearly_seasonality=yearly_seasonality,
            weekly_seasonality=False,  # Dados mensais
            daily_seasonality=False,   # Dados mensais
            seasonality_mode="multiplicative",
            # Aumentar incerteza para refletir limitacao de dados
            interval_width=0.80,  # Intervalo de confianca 80% (mais conservador)
            # Flexibilidade do modelo
            changepoint_prior_scale=0.1,  # Mais rigido para poucos dados
            seasonality_prior_scale=5.0,
        )
        return model

    def forecast(
        self,
        periods: int = DEFAULT_FORECAST_PERIODS,
        grupo: str | None = None,
        categoria: str | None = None,
    ) -> ForecastResult:
        """
        Gera previsao para os proximos periodos.

        Args:
            periods: Numero de meses a prever (padrao: 6).
            grupo: Filtrar por grupo DRE.
            categoria: Filtrar por categoria.

        Returns:
            ForecastResult com previsoes e metricas.
        """
        # Preparar dados
        prophet_df = self.prepare_prophet_data(grupo, categoria)

        if len(prophet_df) < MIN_MONTHS_REQUIRED:
            raise ValueError(
                f"Dados insuficientes apos filtros: {len(prophet_df)} meses"
            )

        # Criar e treinar modelo
        model = self.create_model(yearly_seasonality=len(prophet_df) >= 12)

        # Suprimir output do Prophet
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model.fit(prophet_df)

        # Gerar datas futuras
        future = model.make_future_dataframe(periods=periods, freq="MS")

        # Fazer previsao
        forecast_df = model.predict(future)

        # Calcular metricas
        metrics = self._calculate_metrics(prophet_df, forecast_df)

        # Adicionar warnings
        result_warnings = self.warnings.copy()
        if len(prophet_df) < MIN_MONTHS_RECOMMENDED:
            result_warnings.append(
                f"Previsao baseada em apenas {len(prophet_df)} meses de dados. "
                "Intervalos de confianca podem ser imprecisos."
            )

        return ForecastResult(
            categoria=categoria or "TOTAL",
            grupo=grupo or "TODOS",
            forecast_df=forecast_df,
            metrics=metrics,
            warnings=result_warnings,
        )

    def _calculate_metrics(
        self,
        historical: pd.DataFrame,
        forecast: pd.DataFrame,
    ) -> dict[str, Any]:
        """Calcula metricas da previsao."""
        # Valores historicos
        hist_values = historical["y"].values

        # Previsoes para periodo historico
        merged = forecast[forecast["ds"].isin(historical["ds"])]
        pred_values = merged["yhat"].values[:len(hist_values)]

        # MAPE (Mean Absolute Percentage Error)
        if len(pred_values) > 0 and len(hist_values) > 0:
            mape = (abs(hist_values - pred_values) / abs(hist_values + 1e-10)).mean() * 100
        else:
            mape = None

        # Tendencia
        future_only = forecast[~forecast["ds"].isin(historical["ds"])]
        if len(future_only) > 1:
            trend = "alta" if future_only["yhat"].iloc[-1] > future_only["yhat"].iloc[0] else "baixa"
        else:
            trend = "estavel"

        return {
            "meses_historico": len(historical),
            "meses_previsao": len(future_only),
            "mape_percent": round(mape, 2) if mape else None,
            "tendencia": trend,
            "ultimo_valor_real": float(hist_values[-1]) if len(hist_values) > 0 else None,
            "proxima_previsao": float(future_only["yhat"].iloc[0]) if len(future_only) > 0 else None,
        }

    def get_grupos_disponiveis(self) -> list[str]:
        """Retorna lista de grupos DRE disponiveis."""
        if self.df is None:
            self.load_data()
        grupos = [g for g in self.df["Nome Grupo"].unique().tolist() if g is not None]
        return sorted(grupos)

    def forecast_all_grupos(
        self,
        periods: int = DEFAULT_FORECAST_PERIODS,
    ) -> dict[str, ForecastResult]:
        """
        Gera previsoes para todos os grupos.

        Args:
            periods: Meses a prever.

        Returns:
            Dicionario {grupo: ForecastResult}.
        """
        results = {}
        for grupo in self.get_grupos_disponiveis():
            try:
                results[grupo] = self.forecast(periods=periods, grupo=grupo)
            except Exception as e:
                logger.warning(f"Erro ao prever {grupo}: {e}")
        return results


def forecast_receita(periods: int = 6) -> ForecastResult:
    """
    Funcao de conveniencia para prever receita total.

    Args:
        periods: Meses a prever.

    Returns:
        ForecastResult com previsao de receita.
    """
    forecaster = DREForecaster()
    return forecaster.forecast(periods=periods, grupo="RECEITAS S/ VENDAS")


def forecast_total(periods: int = 6) -> ForecastResult:
    """
    Funcao de conveniencia para prever resultado total.

    Args:
        periods: Meses a prever.

    Returns:
        ForecastResult com previsao total.
    """
    forecaster = DREForecaster()
    return forecaster.forecast(periods=periods)


# =============================================================================
# Standalone Execution
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    print("=" * 60)
    print("FORECASTER DRE - Manda Picanha")
    print("=" * 60)
    print()
    print("AVISO: Modelo simplificado para 12 meses de historico.")
    print("       Previsoes tem precisao reduzida vs 24+ meses.")
    print()

    try:
        forecaster = DREForecaster()
        forecaster.load_data()

        # Previsao total
        print("Gerando previsao para os proximos 6 meses...")
        result = forecaster.forecast(periods=6)

        print(f"\n=== PREVISAO: {result.grupo} - {result.categoria} ===")

        # Warnings
        for w in result.warnings:
            print(f"[!] {w}")

        # Metricas
        print(f"\nMetricas:")
        for k, v in result.metrics.items():
            print(f"  - {k}: {v}")

        # Previsoes futuras
        future = result.forecast_df[
            result.forecast_df["ds"] > forecaster.df["Mês"].max()
        ][["ds", "yhat", "yhat_lower", "yhat_upper"]]

        print(f"\nPrevisoes:")
        for _, row in future.iterrows():
            mes = row["ds"].strftime("%b/%Y")
            valor = f"R$ {row['yhat']:,.0f}".replace(",", ".")
            intervalo = f"[{row['yhat_lower']:,.0f} - {row['yhat_upper']:,.0f}]"
            print(f"  {mes}: {valor} {intervalo}")

    except Exception as e:
        print(f"\nErro: {e}")
        print("Execute primeiro o pipeline principal (main.py).")

