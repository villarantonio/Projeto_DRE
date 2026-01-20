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
        **Função:** Resumo executivo dos principais indicadores financeiros do negócio.

        **Como foi implementada:**
        - **Tecnologia:** Streamlit + Plotly para visualizações interativas
        - **Processamento:** Agregação de dados do arquivo `processed_dre.parquet`
        - **Métricas:** Cálculo automático de KPIs com comparação temporal
        - **Gráficos:** Plotly Express para gráficos de linha e barras responsivos

        **O que você encontra:**
        - KPIs principais (Receita Total, Custos Totais, Lucro Operacional)
        - Gráficos de tendência mensal com evolução temporal
        - Comparativo de períodos (mês atual vs. mês anterior)
        - Cards coloridos com indicadores visuais de performance

        **Importância para a empresa:**
        - ✅ **Visão rápida** do desempenho financeiro sem precisar abrir planilhas
        - ✅ **Tomada de decisão ágil** baseada em dados consolidados
        - ✅ **Identificação imediata** de tendências positivas ou negativas
        - ✅ **Comunicação eficaz** com stakeholders através de visualizações claras

        **Como interpretar:**
        - 📈 Setas verdes indicam crescimento positivo em relação ao período anterior
        - 📉 Setas vermelhas indicam queda em relação ao período anterior
        - Os valores percentuais mostram a variação exata
        """)

    # DRE Mensal
    with st.expander("📈 DRE Mensal", expanded=False):
        st.markdown("""
        **Função:** Demonstrativo de Resultado do Exercício (DRE) detalhado por mês.

        **Como foi implementada:**
        - **Tecnologia:** Pandas para manipulação de dados + Streamlit DataFrames
        - **Filtros dinâmicos:** Widgets interativos (selectbox, multiselect)
        - **Formatação:** Funções customizadas para exibição de valores monetários (R$)
        - **Estrutura:** Hierarquia DRE padrão (Receitas → Custos → Despesas → Resultado)

        **Funcionalidades:**
        - Filtro por mês específico (dropdown com todos os meses disponíveis)
        - Filtro por grupos DRE (Receitas, Custos Variáveis, Despesas, etc.)
        - Tabela formatada com valores monetários em padrão brasileiro
        - Drill-down por categoria e subcategoria

        **Importância para a empresa:**
        - ✅ **Análise detalhada** de cada linha do DRE por período
        - ✅ **Identificação de anomalias** em categorias específicas
        - ✅ **Comparação mensal** para detectar variações sazonais
        - ✅ **Auditoria facilitada** com dados organizados e rastreáveis

        **Dica:** Use os filtros para comparar meses específicos e
        identificar variações sazonais (ex: dezembro vs. outros meses).
        """)

    # Evolução Temporal
    with st.expander("📉 Evolução Temporal", expanded=False):
        st.markdown("""
        **Função:** Análise de tendências e evolução de indicadores ao longo do tempo.

        **Como foi implementada:**
        - **Tecnologia:** Plotly Graph Objects para gráficos interativos avançados
        - **Agregação temporal:** Pandas groupby com resample para séries temporais
        - **Múltiplas visualizações:** Alternância entre tipos de gráfico (linha, barra, área)
        - **Responsividade:** Layout adaptativo para diferentes tamanhos de tela

        **Tipos de visualização:**
        - **Gráfico de Linha:** Ideal para identificar tendências e padrões temporais
        - **Gráfico de Barras:** Melhor para comparar valores absolutos entre períodos
        - **Gráfico de Área:** Visualização de volume acumulado ao longo do tempo

        **Interatividade:**
        - Passe o mouse sobre os pontos para ver valores detalhados e datas
        - Use o zoom (arrastar) para focar em períodos específicos
        - Duplo clique para resetar o zoom
        - Clique na legenda para ocultar/exibir séries específicas

        **Importância para a empresa:**
        - ✅ **Identificação de tendências** de crescimento ou queda
        - ✅ **Detecção de sazonalidade** (picos e vales recorrentes)
        - ✅ **Planejamento estratégico** baseado em padrões históricos
        - ✅ **Previsão informal** de comportamentos futuros
        """)

    # Composição de Custos
    with st.expander("🥧 Composição de Custos", expanded=False):
        st.markdown("""
        **Função:** Entender a distribuição proporcional de custos, despesas e receitas.

        **Como foi implementada:**
        - **Tecnologia:** Plotly Express para gráficos de pizza e treemap
        - **Cálculo de proporções:** Agregação percentual por categoria
        - **Paleta de cores:** Esquema de cores consistente e acessível
        - **Hierarquia visual:** Treemap com níveis (Grupo → Categoria → Subcategoria)

        **Visualizações:**
        - **Gráfico de Pizza (Pie Chart):** Proporção percentual de cada categoria
        - **Treemap:** Hierarquia visual dos custos com áreas proporcionais
        - **Gráfico de Barras Empilhadas:** Composição ao longo do tempo

        **Análise:**
        - Identifique quais categorias consomem mais recursos (maiores fatias/áreas)
        - Descubra oportunidades de otimização (categorias com crescimento desproporcional)
        - Compare a estrutura de custos com benchmarks do setor

        **Importância para a empresa:**
        - ✅ **Gestão de custos** baseada em dados visuais claros
        - ✅ **Priorização de ações** focando nas categorias mais relevantes
        - ✅ **Negociação com fornecedores** usando dados de volume por categoria
        - ✅ **Controle de margem** identificando custos que impactam a lucratividade
        """)

    # Previsões Financeiras
    with st.expander("🔮 Previsões Financeiras", expanded=False):
        st.markdown("""
        **Função:** Projeção estatística de receitas e custos para os próximos meses.

        **Como foi implementada:**
        - **Tecnologia:** Facebook Prophet (biblioteca de forecasting de séries temporais)
        - **Algoritmo:** Modelo aditivo com componentes de tendência e sazonalidade
        - **Treinamento:** Ajuste automático aos dados históricos mensais
        - **Validação:** Cálculo de MAPE (Mean Absolute Percentage Error) para avaliar precisão
        - **Visualização:** Plotly para gráficos com intervalos de confiança (80%)

        **⚠️ Limitações:**
        - Modelo simplificado com apenas 12 meses de histórico disponível
        - Para maior precisão, são recomendados 24+ meses de dados
        - Não considera eventos externos (crises, mudanças de mercado, etc.)
        - Use como **indicativo**, não como valor exato ou garantido

        **Como usar:**
        1. Ajuste o número de meses a prever (1-12) usando o slider
        2. Selecione um grupo DRE específico ou "TODOS" para previsão agregada
        3. Clique em "Gerar Previsão" e aguarde o treinamento do modelo
        4. Analise os intervalos de confiança (área sombreada azul no gráfico)
        5. Consulte a tabela de previsões detalhadas com valores mínimos e máximos

        **Importância para a empresa:**
        - ✅ **Planejamento financeiro** com base em projeções estatísticas
        - ✅ **Gestão de fluxo de caixa** antecipando receitas e despesas
        - ✅ **Tomada de decisão estratégica** (investimentos, contratações, etc.)
        - ✅ **Preparação para cenários** usando intervalos de confiança (melhor/pior caso)
        - ✅ **Comunicação com investidores** apresentando projeções fundamentadas

        **Métricas exibidas:**
        - **Meses de Histórico:** Quantidade de dados usados no treinamento
        - **Tendência:** Direção geral da previsão (alta, baixa, estável)
        - **Próxima Previsão:** Valor projetado para o próximo mês
        - **Intervalo 80%:** Faixa de valores com 80% de probabilidade
        """)

    # Classificação IA
    with st.expander("🤖 Classificação IA", expanded=False):
        st.markdown("""
        **Função:** Classificação automática e inteligente de lançamentos financeiros.

        **Como foi implementada:**
        - **Tecnologia:** Google Gemini 2.0 Flash (modelo de linguagem generativa)
        - **Técnica RAG:** Retrieval-Augmented Generation usando `categories.json` como contexto
        - **Prompt Engineering:** Prompts otimizados para classificação financeira de restaurantes
        - **Fallback:** Sistema de simulação quando API não está disponível
        - **Validação:** Verificação de categorias válidas antes de retornar resultado

        **Funcionalidades:**
        - Classificação automática de descrições de gastos em categorias DRE
        - Sugestão inteligente baseada em contexto semântico (não apenas palavras-chave)
        - Visualização da hierarquia completa de categorias disponíveis
        - Métricas simuladas de performance do modelo (acurácia, precisão, recall, F1-score)
        - Interface de teste manual para validar classificações

        **Como funciona o RAG:**
        1. Sistema carrega todas as categorias do arquivo `categories.json`
        2. Formata as categorias em contexto estruturado (Grupo → Categorias)
        3. Envia descrição + contexto para o modelo Gemini
        4. Modelo retorna a categoria mais adequada baseado em semântica

        **Importância para a empresa:**
        - ✅ **Automação de processos** reduzindo trabalho manual de classificação
        - ✅ **Consistência** nas classificações (sem variação humana)
        - ✅ **Velocidade** processando centenas de lançamentos em segundos
        - ✅ **Aprendizado contínuo** melhorando com feedback e novos exemplos
        - ✅ **Redução de erros** em categorização de despesas e receitas

        **Exemplo de uso:**
        - Digite: "Compra de picanha para churrasco"
        - IA classifica: "BOVINOS" (dentro do grupo "CUSTOS VARIÁVEIS")

        **Requisitos:**
        - Variável de ambiente `GEMINI_API_KEY` configurada
        - Arquivo `output/categories.json` disponível
        - Biblioteca `google-generativeai` instalada
        """)

    st.divider()

    # Arquitetura Técnica
    st.subheader("🏗️ Arquitetura Técnica do Dashboard")

    col_tech1, col_tech2 = st.columns(2)

    with col_tech1:
        st.markdown("""
        **Stack Tecnológico:**
        - **Framework:** Streamlit 1.53+
        - **Visualização:** Plotly (Express + Graph Objects)
        - **Dados:** Pandas + PyArrow (Parquet)
        - **Forecasting:** Facebook Prophet
        - **IA:** Google Gemini 2.0 Flash
        - **Autenticação:** SHA-256 + Streamlit Secrets
        """)

    with col_tech2:
        st.markdown("""
        **Estrutura de Arquivos:**
        - `dashboard/app.py` - Aplicação principal
        - `dashboard/views/` - Páginas do dashboard
        - `dashboard/components/` - Componentes reutilizáveis
        - `src/` - Módulos de processamento
        - `output/` - Dados processados (parquet, JSON)
        """)

    st.markdown("""
    **Fluxo de Dados:**
    1. **ETL Pipeline** (`main.py`) processa dados brutos do Excel/SharePoint
    2. Gera `processed_dre.parquet` e `categories.json` em `output/`
    3. **Dashboard** carrega dados processados em tempo real
    4. **Visualizações** são geradas dinamicamente com Plotly
    5. **Forecasting** treina modelos Prophet sob demanda
    6. **IA** classifica gastos usando Gemini + RAG
    """)

    st.divider()

    # Dicas Gerais
    st.subheader("💡 Dicas de Uso")
    st.markdown("""
    - **Atualização:** Os dados são carregados em tempo real do arquivo parquet
    - **Filtros:** Use a sidebar para configurações globais e específicas de cada página
    - **Exportação:** Gráficos interativos podem ser salvos como imagem (ícone de câmera no canto superior direito)
    - **Tema:** O dashboard adapta-se automaticamente ao tema claro/escuro do Streamlit
    - **Performance:** Para melhor desempenho, use navegadores modernos (Chrome, Edge, Firefox)
    - **Responsividade:** O layout se adapta a diferentes tamanhos de tela (desktop, tablet, mobile)
    """)

    # Suporte e Troubleshooting
    st.subheader("🆘 Suporte e Solução de Problemas")

    with st.expander("❌ Erro: 'Arquivo não encontrado'", expanded=False):
        st.markdown("""
        **Causa:** Dados não foram processados ou estão em local incorreto.

        **Solução:**
        1. Execute o pipeline principal: `python main.py`
        2. Verifique se os arquivos foram gerados em `output/`:
           - `processed_dre.parquet`
           - `categories.json`
        3. Reinicie o dashboard
        """)

    with st.expander("❌ Erro: 'Prophet não instalado'", expanded=False):
        st.markdown("""
        **Causa:** Biblioteca Prophet não está instalada.

        **Solução:**
        ```bash
        pip install prophet
        ```

        **Nota:** No Windows, pode ser necessário instalar dependências adicionais.
        """)

    with st.expander("❌ Erro: 'GEMINI_API_KEY não configurada'", expanded=False):
        st.markdown("""
        **Causa:** Variável de ambiente da API do Google Gemini não está configurada.

        **Solução:**
        1. Obtenha uma chave API em: https://makersuite.google.com/app/apikey
        2. Configure a variável de ambiente:
           - **Windows:** `set GEMINI_API_KEY=sua_chave_aqui`
           - **Linux/Mac:** `export GEMINI_API_KEY=sua_chave_aqui`
        3. Ou adicione ao arquivo `.env` na raiz do projeto
        """)

    with st.expander("❌ Dashboard lento ou travando", expanded=False):
        st.markdown("""
        **Possíveis causas e soluções:**

        1. **Muitos dados:** Filtre períodos específicos em vez de carregar tudo
        2. **Gráficos complexos:** Reduza o número de séries exibidas simultaneamente
        3. **Memória insuficiente:** Feche outras aplicações e reinicie o dashboard
        4. **Cache desatualizado:** Limpe o cache do Streamlit (tecla 'C' no menu)
        """)

    st.markdown("""
    **Contato para Suporte:**
    - 📧 Email: suporte@mandapicanha.com.br
    - 📱 WhatsApp: (XX) XXXXX-XXXX
    - 🐛 Issues: GitHub do projeto

    **Logs e Diagnóstico:**
    - Logs do Streamlit: Terminal onde o dashboard está rodando
    - Logs do ETL: Arquivo `logs/pipeline.log` (se configurado)
    - Versão do Python: 3.10+ recomendado
    """)

