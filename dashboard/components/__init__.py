"""
Componentes reutilizáveis do Dashboard.
"""

from dashboard.components.charts import (
    create_bar_chart,
    create_line_chart,
    create_pie_chart,
    create_treemap,
    create_kpi_card,
)
from dashboard.components.data_loader import (
    load_processed_data,
    load_categories,
    load_narratives,
)

__all__ = [
    "create_bar_chart",
    "create_line_chart",
    "create_pie_chart",
    "create_treemap",
    "create_kpi_card",
    "load_processed_data",
    "load_categories",
    "load_narratives",
]

