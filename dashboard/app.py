"""
Dashboard Interativo DRE - Manda Picanha.

Aplicação Streamlit para visualização de dados financeiros
processados pelo pipeline DRE.

Uso:
    streamlit run dashboard/app.py

Author: Projeto DRE - Manda Picanha
"""

import sys
from pathlib import Path

import streamlit as st

# Adiciona raiz do projeto ao path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

import config
from dashboard.components.data_loader import load_processed_data, load_categories


# =============================================================================
# Configuração da Página
# =============================================================================

st.set_page_config(
    page_title="DRE Dashboard - Manda Picanha",
    page_icon="🥩",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/villarantonio/Projeto_DRE",
        "Report a bug": "https://github.com/villarantonio/Projeto_DRE/issues",
        "About": "Dashboard de análise financeira DRE - Projeto Manda Picanha",
    }
)


# =============================================================================
# Estilos CSS Customizados
# =============================================================================

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
    }
    .stMetric > div {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# Sidebar - Navegação e Filtros
# =============================================================================

with st.sidebar:
    st.markdown("## 🥩 Manda Picanha")
    st.markdown("---")
    
    st.markdown("### 🧭 Navegação")
    
    # Páginas disponíveis
    pages = {
        "📊 Visão Geral": "overview",
        "📈 DRE Mensal": "dre_mensal",
        "📉 Evolução Temporal": "evolucao",
        "🥧 Composição": "composicao",
        "🤖 Classificação IA": "classificacao_ia",
    }
    
    selected_page = st.radio(
        "Selecione a página:",
        options=list(pages.keys()),
        label_visibility="collapsed",
    )
    
    st.markdown("---")
    st.markdown("### 🔧 Configurações")
    
    # Status dos dados
    try:
        df = load_processed_data()
        categories = load_categories()
        st.success(f"✅ {len(df):,} registros carregados")
        st.info(f"📁 {len(categories)} grupos de categorias")
    except FileNotFoundError:
        st.error("❌ Dados não encontrados")
        st.warning("Execute `python main.py` primeiro")
        df = None
        categories = {}


# =============================================================================
# Conteúdo Principal
# =============================================================================

st.markdown('<p class="main-header">🥩 Dashboard DRE - Manda Picanha</p>', unsafe_allow_html=True)

if df is None:
    st.error("### ⚠️ Dados não disponíveis")
    st.markdown("""
    Para visualizar o dashboard, execute primeiro o pipeline de processamento:
    
    ```bash
    python main.py
    ```
    
    Isso irá gerar os arquivos necessários em `output/`.
    """)
    st.stop()


# Importar páginas dinamicamente
if pages[selected_page] == "overview":
    from dashboard.pages.overview import render_overview
    render_overview(df, categories)

elif pages[selected_page] == "dre_mensal":
    from dashboard.pages.dre_mensal import render_dre_mensal
    render_dre_mensal(df, categories)

elif pages[selected_page] == "evolucao":
    from dashboard.pages.evolucao import render_evolucao
    render_evolucao(df, categories)

elif pages[selected_page] == "composicao":
    from dashboard.pages.composicao import render_composicao
    render_composicao(df, categories)

elif pages[selected_page] == "classificacao_ia":
    from dashboard.pages.classificacao_ia import render_classificacao_ia
    render_classificacao_ia(df, categories)


# =============================================================================
# Footer
# =============================================================================

st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #888; font-size: 0.8rem;">
        Pipeline DRE v1.1.0 | Projeto Manda Picanha | 2026
    </div>
    """,
    unsafe_allow_html=True,
)

