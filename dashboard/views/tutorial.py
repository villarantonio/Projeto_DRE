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

    | Funcionalidade | Descrição |
    |----------------|-----------|
    | 📊 **Visão Geral** | KPIs e métricas principais em tempo real |
    | 📈 **DRE Mensal** | Tabelas detalhadas por período |
    | 📉 **Evolução** | Gráficos de tendência temporal |
    | 🥧 **Composição** | Distribuição de receitas e custos |
    | 🔮 **Previsões** | Projeções com Prophet (Machine Learning) |
    | 🤖 **Classificação IA** | Classificação automática com Gemini AI |
    """)

    st.divider()

    # Pré-requisitos
    with st.expander("📋 Pré-requisitos e Configuração", expanded=False):
        st.markdown("""
        ### Requisitos do Sistema

        | Requisito | Especificação |
        |-----------|---------------|
        | **Python** | 3.10 ou superior |
        | **Navegador** | Chrome, Edge, Firefox (versões recentes) |
        | **Memória RAM** | Mínimo 4GB (8GB recomendado) |
        | **Sistema** | Windows, Linux ou macOS |

        ### Arquivos Necessários

        Antes de usar o dashboard, certifique-se de que os arquivos existem:

        ```
        projeto_dre/
        ├── output/
        │   ├── processed_dre.parquet  ← Dados processados
        │   └── categories.json        ← Hierarquia de categorias
        ```

        ### Como Gerar os Arquivos

        Se os arquivos não existirem, execute o pipeline ETL:

        ```bash
        # 1. Navegue até a raiz do projeto
        cd projeto_dre

        # 2. Execute o pipeline principal
        python main.py
        ```

        ### Iniciando o Dashboard

        ```bash
        # Iniciar o servidor Streamlit
        streamlit run dashboard/app.py

        # O dashboard abrirá automaticamente em http://localhost:8501
        ```
        """)

    # Autenticação
    with st.expander("🔐 Autenticação (Login/Logout)", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.info("**Usuário:** `mandapicanha`")
        with col2:
            st.info("**Senha:** `MP@1234`")

        st.markdown("""
        ### Passo a Passo para Login

        1. Digite o usuário: `mandapicanha`
        2. Digite a senha: `MP@1234`
        3. Clique no botão **"🔓 Entrar"**
        4. Aguarde o redirecionamento para o dashboard

        ### Sistema de Segurança

        | Recurso | Descrição |
        |---------|-----------|
        | **Hash SHA-256** | Senhas armazenadas com criptografia |
        | **Limite de tentativas** | Após 3 falhas, aviso é exibido |
        | **Session State** | Sessão mantida até logout |

        ### Como Fazer Logout

        1. No menu lateral (sidebar), localize a seção inferior
        2. Você verá "Logado como: 👤 mandapicanha"
        3. Clique no botão **"🚪 Sair"**
        """)

    # Navegação Principal
    with st.expander("🧭 Navegação Principal", expanded=False):
        st.markdown("""
        ### Estrutura da Interface

        ```
        ┌─────────────────────────────────────────────────────────────────┐
        │ ┌─────────────────┐ ┌─────────────────────────────────────────┐ │
        │ │    SIDEBAR      │ │            ÁREA PRINCIPAL               │ │
        │ │                 │ │                                         │ │
        │ │ 🥩 Manda Picanha│ │  Dashboard DRE                          │ │
        │ │                 │ │  Análise financeira em tempo real       │ │
        │ │ ─────────────── │ │                                         │ │
        │ │ NAVEGAÇÃO       │ │  ┌─────────────────────────────────────┐│ │
        │ │ ○ 📊 Visão Geral│ │  │       CONTEÚDO DA PÁGINA           ││ │
        │ │ ○ 📈 DRE Mensal │ │  │                                     ││ │
        │ │ ○ 📉 Evolução   │ │  │  (KPIs, gráficos, tabelas, etc.)    ││ │
        │ │ ○ 🥧 Composição │ │  │                                     ││ │
        │ │ ○ 🔮 Previsões  │ │  └─────────────────────────────────────┘│ │
        │ │ ○ 🤖 Classif. IA│ │                                         │ │
        │ │ ○ ❓ Como Usar  │ │  ─────────────────────────────────────  │ │
        │ │                 │ │  © 2026 Manda Picanha | v1.4.0          │ │
        │ │ ─────────────── │ └─────────────────────────────────────────┘ │
        │ │ STATUS DADOS    │                                             │
        │ │ 📊 15,500 Reg.  │                                             │
        │ │ 📁 13 Grupos    │                                             │
        │ │                 │                                             │
        │ │ ─────────────── │                                             │
        │ │ 👤 mandapicanha │                                             │
        │ │ [🚪 Sair]       │                                             │
        │ └─────────────────┘                                             │
        └─────────────────────────────────────────────────────────────────┘
        ```

        ### Como Navegar Entre Páginas

        1. Localize o menu **"NAVEGAÇÃO"** na sidebar (lado esquerdo)
        2. Clique no botão de rádio (○) ao lado da página desejada
        3. A página será carregada automaticamente na área principal

        ### Indicadores na Sidebar

        | Indicador | Significado |
        |-----------|-------------|
        | **Registros** | Total de lançamentos financeiros carregados |
        | **Grupos DRE** | Número de categorias macro |
        | **Status Verde** | Dados carregados corretamente |
        | **Status Vermelho** | Dados não encontrados |
        """)

    st.divider()

    # Páginas do Dashboard
    st.subheader("📑 Páginas Disponíveis")

    # Visão Geral
    with st.expander("📊 Visão Geral", expanded=False):
        st.markdown("""
        ### Propósito

        A página **Visão Geral** fornece um resumo executivo dos principais indicadores
        financeiros do negócio. É a página inicial recomendada para obter uma visão
        rápida da saúde financeira.

        ### Layout da Página

        ```
        ┌────────────────────────────────────────────────────────────────┐
        │                     VISÃO GERAL                                │
        ├────────────────────────────────────────────────────────────────┤
        │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
        │  │ 💚 RECEITAS  │  │ 🔴 CUSTOS    │  │ 📊 RESULTADO │         │
        │  │ R$ 72.1M     │  │ R$ 70.8M     │  │ R$ 1.31M     │         │
        │  │ ▲ +5.2%      │  │ ▲ +3.1%      │  │ ▲ +12.4%     │         │
        │  └──────────────┘  └──────────────┘  └──────────────┘         │
        │                                                                │
        │  ┌─────────────────────────────────────────────────────────┐  │
        │  │                 GRÁFICO DE EVOLUÇÃO                     │  │
        │  │        ╱╲    ╱╲                                         │  │
        │  │   ╱╲  ╱  ╲  ╱  ╲╱                                       │  │
        │  │  ╱  ╲╱    ╲╱                                            │  │
        │  │ Jan  Fev  Mar  Abr  Mai  Jun  Jul  Ago  Set  Out  Nov   │  │
        │  └─────────────────────────────────────────────────────────┘  │
        └────────────────────────────────────────────────────────────────┘
        ```

        ### KPI Cards (Cartões de Métricas)

        | Card | Descrição | Interpretação |
        |------|-----------|---------------|
        | 💚 **Receitas** | Total de entradas | Valor em verde = saudável |
        | 🔴 **Custos** | Total de saídas | Monitorar tendência |
        | 📊 **Resultado** | Receitas - Custos | Positivo = lucro |
        | ▲/▼ **Delta** | Variação vs período anterior | Verde = melhoria |

        ### Como Usar

        1. **Navegue** até "📊 Visão Geral" na sidebar
        2. **Analise** os KPIs principais no topo
        3. **Observe** as setas de tendência (▲ verde = bom, ▼ vermelho = atenção)
        4. **Explore** o gráfico passando o mouse sobre os pontos
        5. **Compare** receitas vs custos para avaliar margem

        ### Casos de Uso

        | Cenário | O que fazer |
        |---------|-------------|
        | Reunião executiva | Mostre os KPIs principais |
        | Análise mensal | Verifique tendências no gráfico |
        | Identificar problemas | Procure setas vermelhas (▼) |
        """)

    # DRE Mensal
    with st.expander("📈 DRE Mensal", expanded=False):
        st.markdown("""
        ### Propósito

        A página **DRE Mensal** exibe o Demonstrativo de Resultado do Exercício
        completo, permitindo análise detalhada por mês e categoria.

        ### Layout da Página

        ```
        ┌────────────────────────────────────────────────────────────────┐
        │                     DRE MENSAL                                 │
        ├────────────────────────────────────────────────────────────────┤
        │  ┌─ FILTROS ─────────────────────────────────────────────────┐│
        │  │  Mês: [Todos ▼]        Grupo: [Todos ▼]                   ││
        │  └───────────────────────────────────────────────────────────┘│
        │                                                                │
        │  ┌─ DEMONSTRATIVO DE RESULTADO ─────────────────────────────┐ │
        │  │  Grupo                              │  Valor Formatado   │ │
        │  │  ───────────────────────────────────────────────────────  │ │
        │  │  RECEITAS S/ VENDAS                 │  R$ 6.010.000,00   │ │
        │  │  (+) OUTRAS RECEITAS                │  R$ 121.000,00     │ │
        │  │  ( - ) CUSTOS VARIÁVEIS             │  -R$ 3.200.000,00  │ │
        │  │  ( - ) GASTOS COM PESSOAL           │  -R$ 1.500.000,00  │ │
        │  │  ...                                │  ...               │ │
        │  └───────────────────────────────────────────────────────────┘│
        │                                                                │
        │  ┌─ VISUALIZAÇÃO POR GRUPO ─────────────────────────────────┐ │
        │  │  [Gráfico de Barras Horizontal]                          │ │
        │  │  RECEITAS S/ VENDAS      ████████████████████  R$ 6.01M  │ │
        │  │  CUSTOS VARIÁVEIS        ████████████  -R$ 3.2M          │ │
        │  └───────────────────────────────────────────────────────────┘│
        └────────────────────────────────────────────────────────────────┘
        ```

        ### Filtros Disponíveis

        | Filtro | Opções | Uso |
        |--------|--------|-----|
        | **Mês** | "Todos" ou mês específico | Analisar período específico |
        | **Grupo** | "Todos" ou grupo DRE | Focar em categoria |

        ### Interpretação da Tabela DRE

        | Tipo de Linha | Prefixo | Cor | Significado |
        |---------------|---------|-----|-------------|
        | Receitas | sem prefixo | Verde | Entradas de dinheiro |
        | Outras Receitas | (+) | Verde | Receitas complementares |
        | Custos | ( - ) | Vermelho | Saídas operacionais |
        | Resultado | ( = ) | Azul | Totalizadores |

        ### Passo a Passo

        1. Acesse "📈 DRE Mensal" na sidebar
        2. Defina o filtro de **Mês** (ex: "Set" para setembro)
        3. Observe os 3 KPIs no topo (Receitas, Custos, Resultado)
        4. Role para baixo e analise a **tabela DRE**
        5. Use o **gráfico de barras** para comparação visual
        """)

    # Evolução Temporal
    with st.expander("📉 Evolução Temporal", expanded=False):
        st.markdown("""
        ### Propósito

        A página **Evolução Temporal** mostra tendências e padrões ao longo do tempo,
        permitindo identificar sazonalidades e comparar períodos.

        ### Layout da Página

        ```
        ┌────────────────────────────────────────────────────────────────┐
        │                   EVOLUÇÃO TEMPORAL                            │
        ├────────────────────────────────────────────────────────────────┤
        │  ┌─ CONFIGURAÇÕES ───────────────────────────────────────────┐│
        │  │  Grupos: [Selecione múltiplos ▼]                          ││
        │  │  Tipo de Gráfico: ○ Linha  ○ Barras                       ││
        │  └───────────────────────────────────────────────────────────┘│
        │                                                                │
        │  ┌─ EVOLUÇÃO POR GRUPO ─────────────────────────────────────┐ │
        │  │    ^                          ╱╲                         │ │
        │  │    │     ╱╲    ╱╲    ╱╲     ╱  ╲                        │ │
        │  │ R$ │    ╱  ╲  ╱  ╲  ╱  ╲   ╱    ╲╱                      │ │
        │  │    │   ╱    ╲╱    ╲╱    ╲ ╱                              │ │
        │  │    └────────────────────────────────────────────────►    │ │
        │  │       Jan  Fev  Mar  Abr  Mai  Jun  Jul  Ago  Set  Out   │ │
        │  └──────────────────────────────────────────────────────────┘ │
        │                                                                │
        │  ┌─ ANÁLISE DE VARIAÇÃO ────────────────────────────────────┐ │
        │  │  Mês     │ Resultado       │ Variação %                  │ │
        │  │  ───────────────────────────────────────────────────────  │ │
        │  │  Jan     │ R$ 95.000       │ -                           │ │
        │  │  Fev     │ R$ 102.000      │ +7.4%                       │ │
        │  │  Mar     │ R$ 98.000       │ -3.9%                       │ │
        │  └──────────────────────────────────────────────────────────┘ │
        └────────────────────────────────────────────────────────────────┘
        ```

        ### Tipos de Gráfico

        | Tipo | Quando Usar | Vantagem |
        |------|-------------|----------|
        | **Linha** | Identificar tendências | Mostra continuidade |
        | **Barras** | Comparar valores absolutos | Facilita comparação |

        ### Interatividade dos Gráficos

        | Ação | Como Fazer | Resultado |
        |------|------------|-----------|
        | **Ver detalhes** | Passe o mouse | Tooltip com valor |
        | **Zoom** | Clique e arraste | Amplia região |
        | **Reset zoom** | Duplo clique | Volta à visualização |
        | **Ocultar série** | Clique na legenda | Esconde/mostra linha |

        ### Tabela de Variação

        - **Positivo (+):** Crescimento em relação ao mês anterior
        - **Negativo (-):** Queda em relação ao mês anterior
        - **Cores:** Verde para positivo, vermelho para negativo
        """)

    # Composição de Custos
    with st.expander("🥧 Composição de Custos", expanded=False):
        st.markdown("""
        ### Propósito

        A página **Composição de Custos** permite visualizar a distribuição percentual
        de receitas e despesas, identificando quais categorias representam maior
        impacto no resultado financeiro.

        ### Layout da Página

        ```
        ┌────────────────────────────────────────────────────────────────┐
        │                   COMPOSIÇÃO DE CUSTOS                          │
        ├────────────────────────────────────────────────────────────────┤
        │  ┌─ PERÍODO ────────────────────────────────────────────────┐  │
        │  │  Mês: [Todos ▼]                                          │  │
        │  └──────────────────────────────────────────────────────────┘  │
        │                                                                │
        │  ┌─────────────────┬─────────────────┬─────────────────┐      │
        │  │  💚 Receitas   │  🔴 Custos      │  🗺️ Hierarquia  │      │
        │  └─────────────────┴─────────────────┴─────────────────┘      │
        │                                                                │
        │  ┌─ TAB SELECIONADA ────────────────────────────────────────┐ │
        │  │                                                          │ │
        │  │           [Gráfico de Pizza]                             │ │
        │  │                                                          │ │
        │  │        Top 10 Fontes de Receita                          │ │
        │  │                    ┌────┐                                │ │
        │  │                 ┌──┤ A  ├──┐                             │ │
        │  │              ┌──┤  └────┘  ├──┐                          │ │
        │  │           ┌──┤ B │        │ C ├──┐                       │ │
        │  │           └──────┴────────┴──────┘                       │ │
        │  │                                                          │ │
        │  │  📋 Detalhamento das Receitas  [▼ Expandir]              │ │
        │  └──────────────────────────────────────────────────────────┘ │
        └────────────────────────────────────────────────────────────────┘
        ```

        ### Abas Disponíveis

        | Aba | Ícone | Conteúdo |
        |-----|-------|----------|
        | **Receitas** | 💚 | Top 10 fontes de receita |
        | **Custos/Despesas** | 🔴 | Top 10 maiores custos |
        | **Hierarquia Completa** | 🗺️ | Treemap com Grupo → Categoria |

        ### Treemap (Aba Hierarquia)

        ```
        ┌────────────────────────────────────────────────────────┐
        │ RECEITAS S/ VENDAS                                      │
        │ ┌─────────────┬───────────┬──────────┬────────────┐    │
        │ │ Vendas Loja │ Delivery  │ iFood    │ Outros     │    │
        │ │ (45%)       │ (25%)     │ (20%)    │ (10%)      │    │
        │ └─────────────┴───────────┴──────────┴────────────┘    │
        ├────────────────────────────────────────────────────────┤
        │ CUSTOS VARIÁVEIS                                        │
        │ ┌──────────────────┬─────────────┬───────────────┐     │
        │ │ CMV              │ Embalagens  │ Delivery Tax  │     │
        │ └──────────────────┴─────────────┴───────────────┘     │
        └────────────────────────────────────────────────────────┘
        ```

        - **Retângulo maior:** Grupo DRE (ex: RECEITAS, CUSTOS)
        - **Retângulos internos:** Categorias dentro do grupo
        - **Área:** Proporcional ao valor

        ### Passo a Passo

        1. Acesse "🥧 Composição de Custos" na sidebar
        2. Selecione o período no filtro **Mês**
        3. Navegue entre as abas (Receitas, Custos, Hierarquia)
        4. Clique em **"📋 Detalhamento"** para expandir tabela
        """)

    # Previsões Financeiras
    with st.expander("🔮 Previsões Financeiras", expanded=False):
        st.markdown("""
        ### Propósito

        A página **Previsões Financeiras** utiliza machine learning (Prophet) para
        projetar valores futuros de receitas e custos, auxiliando no planejamento.

        ### Layout da Página

        ```
        ┌────────────────────────────────────────────────────────────────┐
        │                   PREVISÕES FINANCEIRAS                        │
        ├────────────────────────────────────────────────────────────────┤
        │  ┌─ CONFIGURAÇÕES ─────────────────────────────────────────┐  │
        │  │  Meses para prever: [========○====] 6                   │  │
        │  │  Grupo: [TODOS ▼]                                       │  │
        │  │  [🔮 Gerar Previsão]                                    │  │
        │  └─────────────────────────────────────────────────────────┘  │
        │                                                                │
        │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐           │
        │  │ 📅 Histórico │ │ 📈 Tendência │ │ 🎯 Próxima   │           │
        │  │ 12 meses     │ │ ▲ Alta       │ │ R$ 6.2M      │           │
        │  └──────────────┘ └──────────────┘ └──────────────┘           │
        │                                                                │
        │  ┌─ GRÁFICO DE PREVISÃO ───────────────────────────────────┐  │
        │  │                         ░░░░░░░░  (intervalo 80%)       │  │
        │  │    ╱╲    ╱╲    ╱╲     ╱░░░░░░░░░                        │  │
        │  │   ╱  ╲  ╱  ╲  ╱  ╲╲╲╱░░░░░░░░░░░                        │  │
        │  │  ╱    ╲╱    ╲╱      ░░░░░░░░░░░░░                        │  │
        │  │  ─────────────────|─────────────────────────────────    │  │
        │  │  Histórico        │ Previsão                            │  │
        │  │        Jan  Fev  Mar│ Abr  Mai  Jun  Jul  Ago  Set       │  │
        │  └─────────────────────────────────────────────────────────┘  │
        │                                                                │
        │  ┌─ TABELA DE PREVISÕES ───────────────────────────────────┐  │
        │  │  Mês      │ Previsão      │ Mínimo       │ Máximo       │  │
        │  │  Abr/2026 │ R$ 6.010.000  │ R$ 5.800.000 │ R$ 6.220.000 │  │
        │  │  Mai/2026 │ R$ 6.150.000  │ R$ 5.900.000 │ R$ 6.400.000 │  │
        │  └─────────────────────────────────────────────────────────┘  │
        └────────────────────────────────────────────────────────────────┘
        ```

        ### Configurações do Modelo

        | Parâmetro | Opções | Descrição |
        |-----------|--------|-----------|
        | **Meses** | 1-12 | Horizonte de previsão |
        | **Grupo** | "TODOS" ou específico | Filtrar por categoria |
        | **Botão** | 🔮 Gerar Previsão | Inicia o treinamento |

        ### Métricas Exibidas

        | Card | Descrição | Interpretação |
        |------|-----------|---------------|
        | **📅 Histórico** | Meses de dados | Mais dados = mais preciso |
        | **📈 Tendência** | Direção geral | ▲ Alta, ▼ Baixa, ─ Estável |
        | **🎯 Próxima** | Valor projetado | Estimativa para próximo mês |

        ### Interpretação do Gráfico

        | Elemento | Significado |
        |----------|-------------|
        | **Linha contínua** | Dados históricos reais |
        | **Linha tracejada** | Previsão futura |
        | **Área sombreada** | Intervalo de confiança 80% |
        | **Linha vertical** | Divisão histórico/previsão |

        ### ⚠️ Limitações

        - Modelo simplificado com 12 meses de histórico
        - Para maior precisão: 24+ meses recomendados
        - Não considera eventos externos (crises, promoções)
        - Use como **indicativo**, não como valor garantido
        """)

    # Classificação IA
    with st.expander("🤖 Classificação IA", expanded=False):
        st.markdown("""
        ### Propósito

        A página **Classificação IA** utiliza inteligência artificial (Google Gemini 2.0 Flash)
        para classificar automaticamente descrições de gastos nas categorias DRE corretas.

        ### Layout da Página

        ```
        ┌────────────────────────────────────────────────────────────────┐
        │                   CLASSIFICAÇÃO IA                             │
        ├────────────────────────────────────────────────────────────────┤
        │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐           │
        │  │ 🤖 Modelo    │ │ 📊 Categorias│ │ ✅ Acurácia  │           │
        │  │ Gemini 2.0   │ │ 120          │ │ 94.5%        │           │
        │  └──────────────┘ └──────────────┘ └──────────────┘           │
        │                                                                │
        │  ┌─ TESTE DE CLASSIFICAÇÃO ────────────────────────────────┐  │
        │  │  Descrição do gasto:                                    │  │
        │  │  ┌──────────────────────────────────────────────────┐   │  │
        │  │  │ Compra de picanha para churrasco                 │   │  │
        │  │  └──────────────────────────────────────────────────┘   │  │
        │  │                                                         │  │
        │  │  [🤖 Classificar com IA]                                │  │
        │  │                                                         │  │
        │  │  ┌─ RESULTADO ────────────────────────────────────────┐ │  │
        │  │  │  ✅ Classificação: BOVINOS                         │ │  │
        │  │  │  📂 Grupo: CUSTOS VARIÁVEIS                        │ │  │
        │  │  │  💡 Confiança: Alta                                 │ │  │
        │  │  └────────────────────────────────────────────────────┘ │  │
        │  └─────────────────────────────────────────────────────────┘  │
        │                                                                │
        │  ▶ 📂 Hierarquia de Categorias [Expandir]                     │
        └────────────────────────────────────────────────────────────────┘
        ```

        ### Como Funciona o RAG

        **RAG** = Retrieval-Augmented Generation

        ```
        ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
        │ Descrição   │───▶│ Contexto    │───▶│ Gemini 2.0  │
        │ do Gasto    │    │ categories  │    │   Flash     │
        │             │    │ .json       │    │             │
        └─────────────┘    └─────────────┘    └──────┬──────┘
                                                     │
                                                     ▼
                                             ┌─────────────┐
                                             │ Categoria   │
                                             │ Sugerida    │
                                             └─────────────┘
        ```

        ### Exemplos de Classificação

        | Descrição | Categoria | Grupo |
        |-----------|-----------|-------|
        | "Compra de picanha" | BOVINOS | CUSTOS VARIÁVEIS |
        | "Pagamento de aluguel" | ALUGUEL | OCUPAÇÃO |
        | "Salário funcionário" | SALÁRIOS | GASTOS COM PESSOAL |
        | "Conta de energia" | ENERGIA | UTILIDADES |

        ### Passo a Passo

        1. Acesse "🤖 Classificação IA" na sidebar
        2. Digite a descrição do gasto no campo de texto
        3. Clique em **"🤖 Classificar com IA"**
        4. Veja a categoria sugerida e o grupo DRE
        5. Expanda **"📂 Hierarquia"** para ver todas as categorias

        ### Requisitos

        - ⚙️ Variável `GEMINI_API_KEY` configurada
        - 📁 Arquivo `output/categories.json` disponível
        - 📦 Biblioteca `google-generativeai` instalada
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

    st.divider()

    # Glossário
    st.subheader("📚 Glossário de Termos")

    with st.expander("📊 Termos DRE (Financeiros)", expanded=False):
        st.markdown("""
        | Termo | Definição |
        |-------|-----------|
        | **DRE** | Demonstração do Resultado do Exercício - relatório contábil |
        | **Receita** | Entradas de dinheiro (vendas, serviços) |
        | **Custo** | Gastos diretamente ligados à produção |
        | **Despesa** | Gastos administrativos e operacionais |
        | **CMV** | Custo da Mercadoria Vendida |
        | **Margem** | Diferença entre receita e custos |
        | **Lucro Bruto** | Receita - CMV |
        | **Lucro Operacional** | Lucro Bruto - Despesas Operacionais |
        | **EBITDA** | Lucro antes de juros, impostos, depreciação e amortização |
        | **Resultado** | Lucro ou prejuízo final |
        """)

    with st.expander("💻 Termos Técnicos", expanded=False):
        st.markdown("""
        | Termo | Definição |
        |-------|-----------|
        | **Prophet** | Biblioteca de forecasting (previsão) do Facebook/Meta |
        | **RAG** | Retrieval-Augmented Generation - técnica de IA |
        | **Gemini** | Modelo de linguagem do Google (IA generativa) |
        | **Parquet** | Formato de arquivo colunar otimizado |
        | **ETL** | Extract, Transform, Load - pipeline de dados |
        | **KPI** | Key Performance Indicator - indicador de desempenho |
        | **Treemap** | Gráfico hierárquico com retângulos proporcionais |
        | **Streamlit** | Framework Python para dashboards |
        | **Plotly** | Biblioteca de visualização interativa |
        | **API** | Interface de Programação de Aplicações |
        """)

    with st.expander("🔤 Abreviações Comuns", expanded=False):
        st.markdown("""
        | Abreviação | Significado |
        |------------|-------------|
        | **IA** | Inteligência Artificial |
        | **ML** | Machine Learning (Aprendizado de Máquina) |
        | **CC** | Centro de Custo |
        | **R$** | Reais (moeda brasileira) |
        | **%** | Percentual |
        | **vs** | Versus (comparação) |
        | **YoY** | Year over Year (ano a ano) |
        | **MoM** | Month over Month (mês a mês) |
        | **MAPE** | Mean Absolute Percentage Error |
        | **JSON** | JavaScript Object Notation |
        """)

