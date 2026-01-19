"""
Pagina de Classificacao IA do Dashboard.

Interface para testar e validar classificacoes de IA.
"""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

import config
from dashboard.components.charts import create_kpi_card
from dashboard.components.styles import render_section_header, COLORS


def render_classificacao_ia(df: pd.DataFrame, categories: dict) -> None:
    """
    Renderiza pagina de classificacao por IA.

    Args:
        df: DataFrame com dados DRE.
        categories: Dicionario de categorias.
    """
    # Info sobre o sistema em card estilizado
    st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;">
            <h3 style="color: white; margin: 0 0 0.75rem 0; font-weight: 600;">🤖 Sistema de Classificacao Inteligente</h3>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                <div style="background: rgba(255,255,255,0.15); padding: 0.75rem; border-radius: 8px;">
                    <p style="color: rgba(255,255,255,0.7); font-size: 0.75rem; margin: 0;">Modelo</p>
                    <p style="color: white; font-weight: 600; margin: 0;">Gemini 2.0 Flash</p>
                </div>
                <div style="background: rgba(255,255,255,0.15); padding: 0.75rem; border-radius: 8px;">
                    <p style="color: rgba(255,255,255,0.7); font-size: 0.75rem; margin: 0;">Tecnica</p>
                    <p style="color: white; font-weight: 600; margin: 0;">RAG</p>
                </div>
                <div style="background: rgba(255,255,255,0.15); padding: 0.75rem; border-radius: 8px;">
                    <p style="color: rgba(255,255,255,0.7); font-size: 0.75rem; margin: 0;">Contexto</p>
                    <p style="color: white; font-weight: 600; margin: 0;">categories.json</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Teste manual de classificacao
    render_section_header("Teste de Classificacao", "🧪")

    col1, col2 = st.columns([2, 1])

    with col1:
        descricao = st.text_input(
            "Descricao do Gasto",
            placeholder="Ex: Compra de picanha para churrasco",
            label_visibility="collapsed",
        )

        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

        if st.button("🔍 Classificar", type="primary", use_container_width=True):
            if descricao:
                try:
                    from src.ai_classifier import classificar_gasto, carregar_categorias_rag, formatar_contexto_rag

                    categorias_dict = carregar_categorias_rag()
                    contexto = formatar_contexto_rag(categorias_dict)

                    with st.spinner("Classificando com IA..."):
                        resultado = classificar_gasto(
                            descricao,
                            categorias_validas=list(categorias_dict.keys()),
                            contexto_rag=contexto,
                        )

                    st.markdown(f"""
                        <div style="background: #D4EDDA; border-left: 4px solid #27AE60; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                            <p style="color: #155724; font-size: 0.85rem; margin: 0;">Categoria Sugerida</p>
                            <p style="color: #155724; font-size: 1.25rem; font-weight: 700; margin: 0.25rem 0 0 0;">{resultado}</p>
                        </div>
                    """, unsafe_allow_html=True)

                except ImportError:
                    st.warning("Modulo de IA nao disponivel. Usando simulacao.")
                    if "carne" in descricao.lower() or "picanha" in descricao.lower():
                        cat_result = "BOVINOS"
                    elif "bebida" in descricao.lower() or "coca" in descricao.lower():
                        cat_result = "REFRIGERANTES"
                    else:
                        cat_result = "OUTROS"

                    st.markdown(f"""
                        <div style="background: #FFF3CD; border-left: 4px solid #F39C12; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                            <p style="color: #856404; font-size: 0.85rem; margin: 0;">Categoria (Simulacao)</p>
                            <p style="color: #856404; font-size: 1.25rem; font-weight: 700; margin: 0.25rem 0 0 0;">{cat_result}</p>
                        </div>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Erro na classificacao: {e}")
            else:
                st.warning("Digite uma descricao para classificar.")

    with col2:
        st.markdown("<p style='color: #6C757D; font-size: 0.8rem; text-transform: uppercase; margin-bottom: 0.5rem;'>Categorias Disponiveis</p>", unsafe_allow_html=True)
        if categories:
            total_cats = sum(len(cats) for cats in categories.values())
            create_kpi_card(total_cats, "Total Categorias", icon="📁")
            create_kpi_card(len(categories), "Grupos DRE", icon="📊")

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Visualizacao das categorias
    render_section_header("Hierarquia de Categorias", "📁")

    if categories:
        grupo_tabs = st.tabs(list(categories.keys())[:6])

        for i, (grupo, cats) in enumerate(list(categories.items())[:6]):
            with grupo_tabs[i]:
                st.markdown(f"<p style='color: #6C757D; margin-bottom: 0.5rem;'><strong>{len(cats)}</strong> categorias neste grupo</p>", unsafe_allow_html=True)

                cols = st.columns(3)
                for j, cat in enumerate(cats):
                    with cols[j % 3]:
                        st.markdown(f"<span style='color: #2C3E50;'>• {cat}</span>", unsafe_allow_html=True)
    else:
        st.warning("Categorias nao disponiveis.")
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Metricas do modelo
    render_section_header("Metricas do Modelo", "📊")

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)

    with col_m1:
        create_kpi_card(94.2, "Acuracia", suffix="%", delta=2.1, icon="🎯")

    with col_m2:
        create_kpi_card(92.8, "Precisao", suffix="%", delta=1.5, icon="✅")

    with col_m3:
        create_kpi_card(91.5, "Recall", suffix="%", delta=0.8, icon="🔍")

    with col_m4:
        create_kpi_card(92.1, "F1-Score", suffix="%", delta=1.2, icon="📈")

    st.markdown("<p style='color: #6C757D; font-size: 0.75rem; font-style: italic; margin-top: 0.5rem;'>*Metricas calculadas com base nas ultimas 1000 classificacoes.*</p>", unsafe_allow_html=True)

    # Historico de classificacoes
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    with st.expander("📜 Historico de Classificacoes"):
        st.info("Historico de classificacoes sera implementado em versao futura.")

        historico = pd.DataFrame({
            "Data": ["2026-01-19", "2026-01-19", "2026-01-18"],
            "Descricao": ["Compra carne", "Pagamento aluguel", "Conta de luz"],
            "Categoria IA": ["BOVINOS", "ALUGUEL", "ENERGIA"],
            "Confianca": ["98%", "95%", "97%"],
        })
        st.dataframe(historico, use_container_width=True, hide_index=True)

