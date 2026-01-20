"""
Estilos CSS centralizados para o Dashboard Manda Picanha.

Define paleta de cores, componentes reutilizáveis e helpers de formatação.
"""

import streamlit as st

# =============================================================================
# Paleta de Cores Corporativa - Manda Picanha (Otimizada para Dark Mode)
# =============================================================================

COLORS = {
    # Cores primárias
    "primary": "#C41E3A",       # Vermelho carne
    "primary_dark": "#8B0000",  # Vermelho escuro
    "primary_light": "#FF6B6B", # Vermelho claro

    # Cores secundárias
    "secondary": "#2C3E50",     # Azul escuro profissional
    "secondary_light": "#34495E",

    # Cores de acento
    "accent_gold": "#D4AF37",   # Dourado premium
    "accent_cream": "#FFF8DC",  # Creme

    # Cores semânticas
    "success": "#2ECC71",       # Verde positivo (mais vibrante para dark)
    "success_light": "#A8E6CF",
    "danger": "#E74C3C",        # Vermelho negativo
    "danger_light": "#FFCCCC",
    "warning": "#F1C40F",       # Amarelo alerta (mais vibrante para dark)
    "info": "#3498DB",          # Azul informativo

    # Cores de fundo (Dark Mode)
    "bg_dark": "#0E1117",       # Fundo principal Streamlit dark
    "bg_light": "#262730",      # Alias para compatibilidade (agora é secundário)
    "bg_secondary": "#262730",  # Fundo secundário Streamlit dark
    "bg_card": "#1E1E2E",       # Fundo dos cards (escuro)
    "bg_hover": "#2D2D3D",      # Hover em cards

    # Texto (Dark Mode) - Cores claras para fundo escuro
    "text_dark": "#FAFAFA",     # Alias para compatibilidade (texto principal no dark)
    "text_light": "#FAFAFA",    # Texto claro (igual ao principal no dark mode)
    "text_primary": "#FAFAFA",  # Texto principal
    "text_secondary": "#B0B0B0", # Texto secundário
    "text_muted": "#8E8E8E",    # Texto apagado (mais claro para dark)

    # Bordas
    "border": "#3D3D4D",        # Bordas sutis
    "border_light": "#4D4D5D",  # Bordas mais claras
}

# Sequência de cores para gráficos
CHART_COLORS = [
    "#C41E3A",  # Vermelho carne
    "#27AE60",  # Verde
    "#3498DB",  # Azul
    "#F39C12",  # Laranja
    "#9B59B6",  # Roxo
    "#1ABC9C",  # Turquesa
    "#E74C3C",  # Vermelho claro
    "#34495E",  # Azul escuro
]


# =============================================================================
# CSS Global do Dashboard
# =============================================================================

def get_css() -> str:
    """Retorna CSS global do dashboard - Otimizado para Dark Mode."""
    return """
    <style>
        /* === TIPOGRAFIA === */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* === FORÇAR DARK MODE === */
        /* Esconder opção de tema no menu de configurações */
        [data-testid="stSidebarUserContent"] [data-testid="stMarkdownContainer"] select,
        button[title="View fullscreen"],
        .stDeployButton {
            /* Mantém visíveis mas remove opções de tema */
        }

        /* === HEADER PRINCIPAL === */
        .main-header {
            background: linear-gradient(135deg, #C41E3A 0%, #8B0000 100%);
            color: white;
            padding: 1.5rem 2rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 20px rgba(196, 30, 58, 0.4);
        }

        .main-header h1 {
            font-size: 2rem;
            font-weight: 700;
            margin: 0;
            letter-spacing: -0.5px;
        }

        .main-header p {
            font-size: 0.95rem;
            opacity: 0.9;
            margin: 0.5rem 0 0 0;
        }

        /* === SIDEBAR (Dark Mode) === */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%) !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            background: transparent !important;
        }

        /* Texto da sidebar */
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] .stMarkdown span,
        [data-testid="stSidebar"] .stMarkdown h1,
        [data-testid="stSidebar"] .stMarkdown h2,
        [data-testid="stSidebar"] .stMarkdown h3 {
            color: rgba(255, 255, 255, 0.95) !important;
        }

        /* Radio buttons na sidebar */
        [data-testid="stSidebar"] .stRadio label,
        [data-testid="stSidebar"] .stRadio label span {
            color: rgba(255, 255, 255, 0.92) !important;
        }

        [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label {
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 0.6rem 1rem;
            margin-bottom: 0.3rem;
            transition: all 0.2s ease;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label:hover {
            background-color: rgba(196, 30, 58, 0.2);
            border-color: rgba(196, 30, 58, 0.4);
            transform: translateX(3px);
        }

        [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label[data-checked="true"] {
            background-color: rgba(196, 30, 58, 0.25);
            border-left: 3px solid #C41E3A;
            border-color: rgba(196, 30, 58, 0.5);
        }

        /* Selectbox e Slider na sidebar */
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stSlider label,
        [data-testid="stSidebar"] .stNumberInput label {
            color: rgba(255, 255, 255, 0.9) !important;
        }

        /* Button na sidebar */
        [data-testid="stSidebar"] .stButton button {
            color: #FFFFFF !important;
            background: linear-gradient(135deg, #C41E3A 0%, #8B0000 100%);
            border: none;
        }

        [data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.12);
        }

        /* === CARDS DE KPI (Dark Mode) === */
        div[data-testid="stMetric"] {
            background: linear-gradient(145deg, #1E1E2E 0%, #252535 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 1.25rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
        }

        div[data-testid="stMetric"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
            border-color: rgba(196, 30, 58, 0.3);
        }

        div[data-testid="stMetric"] label {
            color: #B0B0B0 !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: #FAFAFA !important;
            font-size: 1.75rem !important;
            font-weight: 700 !important;
        }

        div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
            font-weight: 600;
        }

        /* === BOTÕES (Dark Mode) === */
        .stButton > button {
            background: linear-gradient(135deg, #C41E3A 0%, #8B0000 100%);
            color: white !important;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(196, 30, 58, 0.5);
        }

        /* === SEÇÕES (Dark Mode) === */
        .section-header {
            color: #FAFAFA;
            font-size: 1.25rem;
            font-weight: 600;
            margin: 1.5rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #C41E3A;
        }

        /* === TABELAS (Dark Mode) === */
        .stDataFrame {
            border-radius: 8px;
            overflow: hidden;
        }

        .stDataFrame thead th {
            background: linear-gradient(135deg, #C41E3A 0%, #8B0000 100%) !important;
            color: white !important;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 0.5px;
        }

        .stDataFrame tbody td {
            background: #1E1E2E !important;
            color: #FAFAFA !important;
            border-color: rgba(255, 255, 255, 0.08) !important;
        }

        .stDataFrame tbody tr:hover td {
            background: #262636 !important;
        }

        /* === EXPANDERS (Dark Mode) === */
        .streamlit-expanderHeader {
            background: #1E1E2E !important;
            border-radius: 8px;
            font-weight: 500;
            color: #FAFAFA !important;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .streamlit-expanderContent {
            background: #262730 !important;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-top: none;
        }

        /* === TABS (Dark Mode) === */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: transparent;
        }

        .stTabs [data-baseweb="tab"] {
            background: #1E1E2E;
            border-radius: 8px 8px 0 0;
            padding: 0.75rem 1.25rem;
            font-weight: 500;
            color: #B0B0B0;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: #262730;
            color: #FAFAFA;
            border-bottom-color: #C41E3A;
        }

        /* === SELECTBOX/INPUT (Dark Mode) === */
        .stSelectbox > div > div,
        .stMultiSelect > div > div,
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            background: #1E1E2E !important;
            color: #FAFAFA !important;
            border-color: rgba(255, 255, 255, 0.15) !important;
        }

        .stSelectbox label,
        .stMultiSelect label,
        .stTextInput label,
        .stNumberInput label,
        .stSlider label {
            color: #B0B0B0 !important;
        }

        /* === FOOTER (Dark Mode) === */
        .footer {
            text-align: center;
            color: #6C757D;
            font-size: 0.8rem;
            padding: 1.5rem;
            margin-top: 2rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* === LOADING === */
        .stSpinner > div {
            border-color: #C41E3A !important;
        }

        /* === SCROLLBAR (Dark Mode) === */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #1E1E2E;
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #C41E3A 0%, #8B0000 100%);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #E74C3C;
        }

        /* === PAGE INDICATOR === */
        .page-indicator {
            display: inline-block;
            background: linear-gradient(135deg, #C41E3A 0%, #8B0000 100%);
            color: white;
            padding: 0.3rem 0.85rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
            box-shadow: 0 2px 8px rgba(196, 30, 58, 0.3);
        }

        /* === ALERTAS E MENSAGENS (Dark Mode) === */
        .stAlert {
            border-radius: 8px;
        }

        .stSuccess {
            background: rgba(46, 204, 113, 0.15) !important;
            border-left: 4px solid #2ECC71;
        }

        .stError {
            background: rgba(231, 76, 60, 0.15) !important;
            border-left: 4px solid #E74C3C;
        }

        .stWarning {
            background: rgba(241, 196, 15, 0.15) !important;
            border-left: 4px solid #F1C40F;
        }

        .stInfo {
            background: rgba(52, 152, 219, 0.15) !important;
            border-left: 4px solid #3498DB;
        }

        /* === PLOTLY CHARTS (Dark Mode) === */
        .js-plotly-plot .plotly .modebar {
            background: rgba(30, 30, 46, 0.9) !important;
        }

        .js-plotly-plot .plotly .modebar-btn path {
            fill: #B0B0B0 !important;
        }

        .js-plotly-plot .plotly .modebar-btn:hover path {
            fill: #C41E3A !important;
        }
    </style>
    """


def apply_styles() -> None:
    """Aplica os estilos CSS globais ao dashboard."""
    st.markdown(get_css(), unsafe_allow_html=True)


# =============================================================================
# Componentes de UI Reutilizáveis
# =============================================================================

def render_header(title: str, subtitle: str = "") -> None:
    """Renderiza header principal do dashboard."""
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(f"""
        <div class="main-header">
            <h1>🥩 {title}</h1>
            {subtitle_html}
        </div>
    """, unsafe_allow_html=True)


def render_section_header(title: str, icon: str = "") -> None:
    """Renderiza header de seção."""
    icon_html = f"{icon} " if icon else ""
    st.markdown(f'<div class="section-header">{icon_html}{title}</div>', unsafe_allow_html=True)


def render_page_indicator(page_name: str) -> None:
    """Renderiza indicador de página atual."""
    st.markdown(f'<span class="page-indicator">{page_name}</span>', unsafe_allow_html=True)


def render_footer() -> None:
    """Renderiza footer do dashboard."""
    st.markdown("""
        <div class="footer">
            <strong>Pipeline DRE v1.2.0</strong> | Manda Picanha &copy; 2026<br>
            <small>Dados atualizados em tempo real</small>
        </div>
    """, unsafe_allow_html=True)


# =============================================================================
# Formatação de Valores
# =============================================================================

def format_currency(value: float, prefix: str = "R$ ") -> str:
    """
    Formata valor monetário no padrão brasileiro.

    Args:
        value: Valor numérico.
        prefix: Prefixo (default: 'R$ ').

    Returns:
        String formatada: R$ 1.234.567,89
    """
    if value is None:
        return f"{prefix}0,00"

    # Formata com pontos como separador de milhar e vírgula decimal
    formatted = f"{abs(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    sign = "-" if value < 0 else ""
    return f"{sign}{prefix}{formatted}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Formata valor como percentual.

    Args:
        value: Valor numérico.
        decimals: Casas decimais.

    Returns:
        String formatada: 12,5%
    """
    if value is None:
        return "0,0%"
    formatted = f"{value:.{decimals}f}".replace(".", ",")
    return f"{formatted}%"


def format_number(value: float | int, abbreviate: bool = True) -> str:
    """
    Formata número com abreviação opcional.

    Args:
        value: Valor numérico.
        abbreviate: Se True, abrevia para K, M, B.

    Returns:
        String formatada.
    """
    if value is None:
        return "0"

    if abbreviate:
        if abs(value) >= 1_000_000_000:
            return f"{value/1_000_000_000:.1f}B".replace(".", ",")
        elif abs(value) >= 1_000_000:
            return f"{value/1_000_000:.1f}M".replace(".", ",")
        elif abs(value) >= 1_000:
            return f"{value/1_000:.1f}K".replace(".", ",")

    return f"{value:,.0f}".replace(",", ".")

