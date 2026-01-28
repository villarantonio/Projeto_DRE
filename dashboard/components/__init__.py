"""
Componentes reutilizáveis do Dashboard.

Os componentes são importados diretamente dos módulos específicos
(charts, data_loader, styles) para evitar dependências circulares
e problemas de importação no Streamlit Cloud.
"""

__all__ = [
    "create_bar_chart",
    "create_line_chart",
    "create_pie_chart",
    "create_treemap",
    "create_kpi_card",
    "create_hierarchical_dre_table",
    "render_store_filter",
    "calculate_rob_percentage",
    "load_processed_data",
    "load_categories",
    "load_narratives",
    "get_unique_stores",
    "filter_by_stores",
]

