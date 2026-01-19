"""
Dashboard Interativo DRE - Manda Picanha.

Aplicacao Streamlit para visualizacao de dados financeiros
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
from dashboard.components.styles import (
    apply_styles,
    render_header,
    render_footer,
    render_page_indicator,
    COLORS,
)
from dashboard.components.auth import (
    init_session_state,
    is_authenticated,
    render_login_page,
    render_logout_button,
)


# =============================================================================
# Configuracao da Pagina
# =============================================================================

st.set_page_config(
    page_title="DRE Dashboard - Manda Picanha",
    page_icon="🥩",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/villarantonio/Projeto_DRE",
        "Report a bug": "https://github.com/villarantonio/Projeto_DRE/issues",
        "About": "Dashboard de analise financeira DRE - Projeto Manda Picanha",
    }
)


# =============================================================================
# Inicializar Session State de Autenticacao
# =============================================================================

init_session_state()


# =============================================================================
# Aplicar Estilos CSS Globais
# =============================================================================

apply_styles()


# =============================================================================
# Verificacao de Autenticacao
# =============================================================================

if not is_authenticated():
    render_login_page()
    st.stop()


# =============================================================================
# Sidebar - Navegação e Filtros
# =============================================================================

# Páginas disponíveis com ícones
PAGES = {
    "overview": {"name": "Visao Geral", "icon": "📊", "desc": "Resumo executivo"},
    "dre_mensal": {"name": "DRE Mensal", "icon": "📈", "desc": "Demonstrativo mensal"},
    "evolucao": {"name": "Evolucao", "icon": "📉", "desc": "Tendencias temporais"},
    "composicao": {"name": "Composicao", "icon": "🥧", "desc": "Analise de custos"},
    "classificacao_ia": {"name": "Classificacao IA", "icon": "🤖", "desc": "Classificador inteligente"},
}

with st.sidebar:
    # Logo e título
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <span style="font-size: 3rem;">🥩</span>
            <h2 style="color: white; margin: 0.5rem 0 0 0; font-weight: 700;">Manda Picanha</h2>
            <p style="color: rgba(255,255,255,0.7); font-size: 0.8rem; margin: 0;">Dashboard Financeiro DRE</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 1rem 0;'>", unsafe_allow_html=True)

    # Navegação
    st.markdown("<p style='color: rgba(255,255,255,0.5); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;'>NAVEGACAO</p>", unsafe_allow_html=True)

    # Criar lista de opções formatadas
    page_options = [f"{info['icon']} {info['name']}" for info in PAGES.values()]
    page_keys = list(PAGES.keys())

    selected_index = st.radio(
        "Selecione a pagina:",
        options=range(len(page_options)),
        format_func=lambda i: page_options[i],
        label_visibility="collapsed",
    )

    selected_page_key = page_keys[selected_index]
    selected_page_info = PAGES[selected_page_key]

    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 1rem 0;'>", unsafe_allow_html=True)

    # Status dos dados
    st.markdown("<p style='color: rgba(255,255,255,0.5); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;'>STATUS DOS DADOS</p>", unsafe_allow_html=True)

    try:
        df = load_processed_data()
        categories = load_categories()

        # Cards de status compactos
        st.markdown(f"""
            <div style="background: rgba(39, 174, 96, 0.2); border-left: 3px solid #27AE60; padding: 0.75rem; border-radius: 4px; margin-bottom: 0.5rem;">
                <p style="color: #27AE60; font-size: 0.75rem; margin: 0; text-transform: uppercase;">Registros</p>
                <p style="color: white; font-size: 1.25rem; font-weight: 700; margin: 0;">{len(df):,}</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="background: rgba(52, 152, 219, 0.2); border-left: 3px solid #3498DB; padding: 0.75rem; border-radius: 4px;">
                <p style="color: #3498DB; font-size: 0.75rem; margin: 0; text-transform: uppercase;">Grupos DRE</p>
                <p style="color: white; font-size: 1.25rem; font-weight: 700; margin: 0;">{len(categories)}</p>
            </div>
        """, unsafe_allow_html=True)

    except FileNotFoundError:
        st.markdown("""
            <div style="background: rgba(231, 76, 60, 0.2); border-left: 3px solid #E74C3C; padding: 0.75rem; border-radius: 4px;">
                <p style="color: #E74C3C; font-size: 0.85rem; margin: 0;">Dados nao encontrados</p>
                <p style="color: rgba(255,255,255,0.7); font-size: 0.75rem; margin: 0.25rem 0 0 0;">Execute python main.py</p>
            </div>
        """, unsafe_allow_html=True)
        df = None
        categories = {}

    # Botao de logout
    render_logout_button()

    # Versao no rodape da sidebar
    st.markdown("<p style='color: rgba(255,255,255,0.3); font-size: 0.7rem; text-align: center;'>v1.3.0 | Pipeline DRE</p>", unsafe_allow_html=True)


# =============================================================================
# Conteúdo Principal
# =============================================================================

# Header principal
render_header("Dashboard DRE", "Analise financeira em tempo real")

# Indicador de página atual
render_page_indicator(selected_page_info["name"])

if df is None:
    st.error("### Dados nao disponiveis")
    st.markdown("""
    Para visualizar o dashboard, execute primeiro o pipeline de processamento:

    ```bash
    python main.py
    ```

    Isso ira gerar os arquivos necessarios em `output/`.
    """)
    st.stop()


# Importar e renderizar página selecionada
if selected_page_key == "overview":
    from dashboard.pages.overview import render_overview
    render_overview(df, categories)

elif selected_page_key == "dre_mensal":
    from dashboard.pages.dre_mensal import render_dre_mensal
    render_dre_mensal(df, categories)

elif selected_page_key == "evolucao":
    from dashboard.pages.evolucao import render_evolucao
    render_evolucao(df, categories)

elif selected_page_key == "composicao":
    from dashboard.pages.composicao import render_composicao
    render_composicao(df, categories)

elif selected_page_key == "classificacao_ia":
    from dashboard.pages.classificacao_ia import render_classificacao_ia
    render_classificacao_ia(df, categories)


# =============================================================================
# Footer
# =============================================================================

render_footer()

