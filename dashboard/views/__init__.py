"""
Páginas do Dashboard DRE.

As views são importadas sob demanda (lazy loading) no app.py
para evitar dependências circulares e problemas de importação
no Streamlit Cloud.
"""

__all__ = [
    "render_overview",
    "render_dre_mensal",
    "render_evolucao",
    "render_composicao",
    "render_classificacao_ia",
]

