"""
Páginas do Dashboard DRE.
"""

from dashboard.views.overview import render_overview
from dashboard.views.dre_mensal import render_dre_mensal
from dashboard.views.evolucao import render_evolucao
from dashboard.views.composicao import render_composicao
from dashboard.views.classificacao_ia import render_classificacao_ia

__all__ = [
    "render_overview",
    "render_dre_mensal",
    "render_evolucao",
    "render_composicao",
    "render_classificacao_ia",
]

