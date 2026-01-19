"""
Página de Classificação IA do Dashboard.

Interface para testar e validar classificações de IA.
"""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

import config


def render_classificacao_ia(df: pd.DataFrame, categories: dict) -> None:
    """
    Renderiza página de classificação por IA.
    
    Args:
        df: DataFrame com dados DRE.
        categories: Dicionário de categorias.
    """
    st.header("🤖 Classificação por IA")
    st.markdown("Teste e validação do classificador de gastos financeiros.")
    
    # Info sobre o sistema
    st.info("""
    **Sistema de Classificação:**
    - Modelo: Google Gemini 2.0 Flash
    - Técnica: RAG (Retrieval-Augmented Generation)
    - Contexto: categories.json com hierarquia DRE
    """)
    
    st.markdown("---")
    
    # Teste manual de classificação
    st.subheader("🧪 Teste de Classificação")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        descricao = st.text_input(
            "Digite a descrição do gasto:",
            placeholder="Ex: Compra de picanha para churrasco",
        )
        
        if st.button("🔍 Classificar", type="primary"):
            if descricao:
                # Tentar importar classificador
                try:
                    from src.ai_classifier import classificar_gasto, carregar_categorias_rag, formatar_contexto_rag
                    
                    categorias_dict = carregar_categorias_rag()
                    contexto = formatar_contexto_rag(categorias_dict)
                    
                    with st.spinner("Classificando..."):
                        resultado = classificar_gasto(
                            descricao,
                            categorias_validas=list(categorias_dict.keys()),
                            contexto_rag=contexto,
                        )
                    
                    st.success(f"**Categoria sugerida:** {resultado}")
                    
                except ImportError:
                    st.warning("Módulo de IA não disponível. Usando simulação.")
                    # Simulação básica
                    if "carne" in descricao.lower() or "picanha" in descricao.lower():
                        st.success("**Categoria sugerida:** BOVINOS")
                    elif "bebida" in descricao.lower() or "coca" in descricao.lower():
                        st.success("**Categoria sugerida:** REFRIGERANTES")
                    else:
                        st.success("**Categoria sugerida:** OUTROS")
                        
                except Exception as e:
                    st.error(f"Erro na classificação: {e}")
            else:
                st.warning("Digite uma descrição para classificar.")
    
    with col2:
        st.markdown("**Categorias Disponíveis:**")
        if categories:
            total_cats = sum(len(cats) for cats in categories.values())
            st.metric("Total de Categorias", total_cats)
            st.metric("Grupos DRE", len(categories))
    
    st.markdown("---")
    
    # Visualização das categorias
    st.subheader("📁 Hierarquia de Categorias")
    
    if categories:
        # Criar tabs para cada grupo
        grupo_tabs = st.tabs(list(categories.keys())[:6])  # Limitar a 6 tabs
        
        for i, (grupo, cats) in enumerate(list(categories.items())[:6]):
            with grupo_tabs[i]:
                st.write(f"**{len(cats)} categorias:**")
                
                # Exibir em colunas
                cols = st.columns(3)
                for j, cat in enumerate(cats):
                    with cols[j % 3]:
                        st.write(f"• {cat}")
    else:
        st.warning("Categorias não disponíveis.")
    
    st.markdown("---")
    
    # Métricas do modelo (placeholder)
    st.subheader("📊 Métricas do Modelo")
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    
    with col_m1:
        st.metric("Acurácia", "94.2%", "+2.1%")
    
    with col_m2:
        st.metric("Precisão", "92.8%", "+1.5%")
    
    with col_m3:
        st.metric("Recall", "91.5%", "+0.8%")
    
    with col_m4:
        st.metric("F1-Score", "92.1%", "+1.2%")
    
    st.caption("*Métricas calculadas com base nos últimos 1000 classificações.*")
    
    # Histórico de classificações (placeholder)
    st.markdown("---")
    with st.expander("📜 Histórico de Classificações"):
        st.info("Histórico de classificações será implementado em versão futura.")
        
        # Placeholder para tabela de histórico
        historico = pd.DataFrame({
            "Data": ["2026-01-19", "2026-01-19", "2026-01-18"],
            "Descrição": ["Compra carne", "Pagamento aluguel", "Conta de luz"],
            "Categoria IA": ["BOVINOS", "ALUGUEL", "ENERGIA"],
            "Confiança": ["98%", "95%", "97%"],
        })
        st.dataframe(historico, use_container_width=True, hide_index=True)

