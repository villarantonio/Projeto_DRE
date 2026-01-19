"""
Estilos CSS centralizados para o Dashboard Manda Picanha.

Define paleta de cores, componentes reutilizáveis e helpers de formatação.
"""

import streamlit as st

# =============================================================================
# Paleta de Cores Corporativa - Manda Picanha
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
    "success": "#27AE60",       # Verde positivo
    "success_light": "#A8E6CF",
    "danger": "#E74C3C",        # Vermelho negativo
    "danger_light": "#FFCCCC",
    "warning": "#F39C12",       # Laranja alerta
    "info": "#3498DB",          # Azul informativo
    
    # Cores de fundo
    "bg_dark": "#1E1E1E",
    "bg_light": "#F8F9FA",
    "bg_card": "#FFFFFF",
    
    # Texto
    "text_dark": "#2C3E50",
    "text_light": "#FFFFFF",
    "text_muted": "#6C757D",
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
    """Retorna CSS global do dashboard."""
    return """
    <style>
        /* === TIPOGRAFIA === */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* === HEADER PRINCIPAL === */
        .main-header {
            background: linear-gradient(135deg, #C41E3A 0%, #8B0000 100%);
            color: white;
            padding: 1.5rem 2rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 15px rgba(196, 30, 58, 0.3);
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
        
        /* === SIDEBAR === */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #2C3E50 0%, #1E1E1E 100%);
        }
        
        [data-testid="stSidebar"] .stMarkdown {
            color: #FFFFFF;
        }
        
        [data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.1);
        }
        
        /* === CARDS DE KPI === */
        div[data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid #E9ECEF;
            border-radius: 12px;
            padding: 1.25rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        
        div[data-testid="stMetric"] label {
            color: #6C757D !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: #2C3E50 !important;
            font-size: 1.75rem !important;
            font-weight: 700 !important;
        }
        
        /* === BOTÕES === */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #C41E3A 0%, #8B0000 100%);
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .stButton > button[kind="primary"]:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(196, 30, 58, 0.4);
        }

        /* === SEÇÕES === */
        .section-header {
            color: #2C3E50;
            font-size: 1.25rem;
            font-weight: 600;
            margin: 1.5rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #C41E3A;
        }

        /* === TABELAS === */
        .stDataFrame {
            border-radius: 8px;
            overflow: hidden;
        }

        .stDataFrame thead th {
            background: #2C3E50 !important;
            color: white !important;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 0.5px;
        }

        /* === EXPANDERS === */
        .streamlit-expanderHeader {
            background: #F8F9FA;
            border-radius: 8px;
            font-weight: 500;
        }

        /* === TABS === */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
            padding: 0.75rem 1.25rem;
            font-weight: 500;
        }

        /* === FOOTER === */
        .footer {
            text-align: center;
            color: #6C757D;
            font-size: 0.8rem;
            padding: 1.5rem;
            margin-top: 2rem;
            border-top: 1px solid #E9ECEF;
        }

        /* === LOADING === */
        .stSpinner > div {
            border-color: #C41E3A !important;
        }

        /* === SCROLLBAR === */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #F1F1F1;
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb {
            background: #C41E3A;
            border-radius: 4px;
        }

        /* === PAGE INDICATOR === */
        .page-indicator {
            display: inline-block;
            background: #C41E3A;
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
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

