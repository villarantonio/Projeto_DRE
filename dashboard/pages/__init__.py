"""
Páginas do Dashboard DRE.
"""

from dashboard.pages.overview import render_overview
from dashboard.pages.dre_mensal import render_dre_mensal
from dashboard.pages.evolucao import render_evolucao
from dashboard.pages.composicao import render_composicao
from dashboard.pages.classificacao_ia import render_classificacao_ia

__all__ = [
    "render_overview",
    "render_dre_mensal",
    "render_evolucao",
    "render_composicao",
    "render_classificacao_ia",
]

