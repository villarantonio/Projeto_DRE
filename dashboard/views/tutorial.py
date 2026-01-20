"""
Página de Tutorial do Dashboard DRE.
Instruções de uso e guia de funcionalidades.
"""

import streamlit as st
from dashboard.components.styles import render_section_header


def render_tutorial() -> None:
    """Renderiza a página de tutorial e documentação."""
    render_section_header(
        "Como Usar o Dashboard",
        "Guia completo de navegação e funcionalidades",
    )

    # Introdução
    st.markdown("""
    Bem-vindo ao **Dashboard Financeiro DRE** do Manda Picanha! 🥩
    
    Este guia vai ajudá-lo a aproveitar ao máximo todas as funcionalidades 
    disponíveis para análise dos dados financeiros.
    """)

    st.divider()

    # Pré-requisitos
    st.subheader("📋 Pré-requisitos")
    st.markdown("""
    Antes de usar o dashboard, certifique-se de que:
    
    1. **Processou os dados**: Execute `python main.py` na raiz do projeto
    2. **Arquivos gerados**: Verifique se existem os arquivos:
       - `output/processed_dre.parquet`
       - `output/categories.json`
    3. **Dependências instaladas**: Execute `pip install -r requirements.txt`
    """)

    with st.expander("🔐 Credenciais de Acesso", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.info("**Usuário:** `mandapicanha`")
        with col2:
            st.info("**Senha:** `MP@1234`")

    st.divider()

    # Páginas do Dashboard
    st.subheader("📑 Páginas Disponíveis")

    # Visão Geral
    with st.expander("📊 Visão Geral", expanded=False):
        st.markdown("""
        **Objetivo:** Resumo executivo dos principais indicadores financeiros.
        
        **O que você encontra:**
        - KPIs principais (Receita Total, Custos, Lucro)
        - Gráficos de tendência mensal
        - Comparativo de períodos
        
        **Como interpretar:**
        - 📈 Setas verdes indicam crescimento positivo
        - 📉 Setas vermelhas indicam queda
        - Os valores são comparados com o mês anterior
        """)

    # DRE Mensal
    with st.expander("📈 DRE Mensal", expanded=False):
        st.markdown("""
        **Objetivo:** Demonstrativo de Resultado detalhado por mês.
        
        **Funcionalidades:**
        - Filtro por mês específico
        - Filtro por grupos DRE
        - Tabela formatada com valores monetários
        
        **Dica:** Use os filtros para comparar meses específicos e 
        identificar variações sazonais.
        """)

    # Evolução Temporal
    with st.expander("📉 Evolução Temporal", expanded=False):
        st.markdown("""
        **Objetivo:** Análise de tendências ao longo do tempo.
        
        **Tipos de visualização:**
        - **Gráfico de Linha:** Ideal para ver tendências
        - **Gráfico de Barras:** Melhor para comparar valores absolutos
        
        **Interatividade:**
        - Passe o mouse sobre os pontos para ver valores detalhados
        - Use o zoom para focar em períodos específicos
        """)

    # Composição de Custos
    with st.expander("🥧 Composição de Custos", expanded=False):
        st.markdown("""
        **Objetivo:** Entender a distribuição de custos e receitas.
        
        **Visualizações:**
        - **Gráfico de Pizza:** Proporção de cada categoria
        - **Treemap:** Hierarquia visual dos custos
        
        **Análise:** Identifique quais categorias consomem mais recursos
        e onde há oportunidades de otimização.
        """)

    # Previsões Financeiras
    with st.expander("🔮 Previsões Financeiras", expanded=False):
        st.markdown("""
        **Objetivo:** Projeção de receitas e custos futuros.
        
        **Tecnologia:** Utiliza o modelo **Prophet** do Facebook/Meta.
        
        **⚠️ Limitações:**
        - Modelo simplificado com 12 meses de histórico
        - Para maior precisão, são recomendados 24+ meses
        - Use como **indicativo**, não como valor exato
        
        **Como usar:**
        1. Ajuste o número de meses a prever (1-12)
        2. Selecione um grupo DRE específico ou "TODOS"
        3. Clique em "Gerar Previsão"
        4. Analise os intervalos de confiança (área sombreada)
        """)

    # Classificação IA
    with st.expander("🤖 Classificação IA", expanded=False):
        st.markdown("""
        **Objetivo:** Classificação inteligente de lançamentos.
        
        **Tecnologia:** Integração com Google Gemini 2.0 Flash.
        
        **Funcionalidades:**
        - Classificação automática de descrições
        - Sugestão de grupo e subgrupo DRE
        - Histórico de classificações
        """)

    st.divider()

    # Dicas Gerais
    st.subheader("💡 Dicas de Uso")
    st.markdown("""
    - **Atualização:** Os dados são carregados em tempo real do arquivo parquet
    - **Filtros:** Use a sidebar para configurações globais
    - **Exportação:** Gráficos interativos podem ser salvos como imagem (ícone de câmera)
    - **Tema:** O dashboard adapta-se ao tema claro/escuro do Streamlit
    """)

    # Suporte
    st.subheader("🆘 Suporte")
    st.markdown("""
    Em caso de problemas:
    1. Verifique os logs no terminal onde o Streamlit está rodando
    2. Reprocesse os dados com `python main.py`
    3. Reinicie o dashboard com `streamlit run dashboard/app.py`
    """)

