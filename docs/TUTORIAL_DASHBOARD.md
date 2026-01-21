# 📖 Tutorial Completo do Dashboard DRE - Manda Picanha

> **Guia passo a passo para utilizar todas as funcionalidades do Dashboard Financeiro**

---

## 📋 Índice

1. [Introdução](#introdução)
2. [Pré-requisitos e Configuração](#pré-requisitos-e-configuração)
3. [Autenticação (Login/Logout)](#autenticação-loginlogout)
4. [Navegação Principal](#navegação-principal)
5. [Visão Geral](#1-visão-geral-)
6. [DRE Mensal](#2-dre-mensal-)
7. [Evolução Temporal](#3-evolução-temporal-)
8. [Composição de Custos](#4-composição-de-custos-)
9. [Previsões Financeiras](#5-previsões-financeiras-)
10. [Classificação IA](#6-classificação-ia-)
11. [Tutorial (Como Usar)](#7-tutorial-como-usar-)
12. [Solução de Problemas](#solução-de-problemas)
13. [Glossário](#glossário)

---

## Introdução

O **Dashboard DRE Manda Picanha** é uma aplicação web interativa desenvolvida em Streamlit para análise financeira de Demonstração do Resultado do Exercício (DRE). Ele permite visualizar, analisar e projetar dados financeiros de forma intuitiva e profissional.

### Principais Funcionalidades

| Funcionalidade | Descrição |
|----------------|-----------|
| 📊 **Visão Geral** | KPIs e métricas principais em tempo real |
| 📈 **DRE Mensal** | Tabelas detalhadas por período |
| 📉 **Evolução** | Gráficos de tendência temporal |
| 🥧 **Composição** | Distribuição de receitas e custos |
| 🔮 **Previsões** | Projeções com Prophet (Machine Learning) |
| 🤖 **Classificação IA** | Classificação automática com Gemini AI |

---

## Pré-requisitos e Configuração

### Requisitos do Sistema

- **Python:** 3.10 ou superior
- **Navegador:** Chrome, Edge, Firefox (versões recentes)
- **Memória RAM:** Mínimo 4GB (8GB recomendado)
- **Sistema Operacional:** Windows, Linux ou macOS

### Arquivos Necessários

Antes de usar o dashboard, certifique-se de que os seguintes arquivos existem:

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

---

## Autenticação (Login/Logout)

### Tela de Login

Ao acessar o dashboard, você verá a tela de autenticação:

```
┌─────────────────────────────────┐
│           🥩                    │
│      Manda Picanha              │
│   Dashboard Financeiro DRE      │
│                                 │
│  ┌───────────────────────────┐  │
│  │   🔐 Acesso ao Sistema    │  │
│  │                           │  │
│  │   Usuário: [___________]  │  │
│  │   Senha:   [___________]  │  │
│  │                           │  │
│  │     [ 🔓 Entrar ]         │  │
│  └───────────────────────────┘  │
│                                 │
│         v1.4.0 | Pipeline DRE   │
└─────────────────────────────────┘
```

### Credenciais de Acesso

| Campo | Valor |
|-------|-------|
| **Usuário** | `mandapicanha` |
| **Senha** | `MP@1234` |

### Passo a Passo para Login

1. Digite o usuário: `mandapicanha`
2. Digite a senha: `MP@1234`
3. Clique no botão **"🔓 Entrar"**
4. Aguarde o redirecionamento para o dashboard

### Sistema de Segurança

- **Hash SHA-256:** Senhas são armazenadas com criptografia
- **Limite de tentativas:** Após 3 tentativas falhas, um aviso é exibido
- **Session State:** Sessão mantida até logout ou fechamento do navegador

### Como Fazer Logout

1. No menu lateral (sidebar), localize a seção inferior
2. Você verá "Logado como: 👤 mandapicanha"
3. Clique no botão **"🚪 Sair"**
4. Você será redirecionado para a tela de login

---

## Navegação Principal

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
│ │ ○ 🔮 Previsões  │ │  │                                     ││ │
│ │ ○ 🤖 Classif. IA│ │  └─────────────────────────────────────┘│ │
│ │ ○ ❓ Como Usar  │ │                                         │ │
│ │                 │ │  ─────────────────────────────────────  │ │
│ │ ─────────────── │ │  © 2026 Manda Picanha | v1.4.0          │ │
│ │ STATUS DADOS    │ └─────────────────────────────────────────┘ │
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
| **Grupos DRE** | Número de categorias macro (Receitas, Custos, etc.) |
| **Status Verde** | Dados carregados corretamente |
| **Status Vermelho** | Dados não encontrados - execute `python main.py` |

---

## 1. Visão Geral 📊

### Propósito

A página **Visão Geral** fornece um resumo executivo dos principais indicadores financeiros do negócio. É a página inicial recomendada para obter uma visão rápida da saúde financeira.

### O que Você Verá

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
│                                                                │
│  ┌───────────────────────────────┐  ┌────────────────────────┐│
│  │  RECEITAS POR CATEGORIA      │  │  RESUMO DO PERÍODO    ││
│  │  [Gráfico de Pizza]          │  │  • Total Lojas: 14    ││
│  │                              │  │  • Meses: 12          ││
│  │                              │  │  • Categorias: 259    ││
│  └───────────────────────────────┘  └────────────────────────┘│
└────────────────────────────────────────────────────────────────┘
```

### Elementos da Interface

#### KPI Cards (Cartões de Métricas)

| Card | Descrição | Interpretação |
|------|-----------|---------------|
| 💚 **Receitas** | Total de entradas (valores positivos) | Valor em verde = saudável |
| 🔴 **Custos** | Total de saídas (valores negativos) | Monitorar tendência de crescimento |
| 📊 **Resultado** | Receitas - Custos (Lucro/Prejuízo) | Positivo = lucro, Negativo = prejuízo |
| ▲/▼ **Delta** | Variação percentual vs período anterior | Verde = melhoria, Vermelho = piora |

#### Gráfico de Evolução

- **Eixo X:** Meses do ano
- **Eixo Y:** Valores em Reais (R$)
- **Linhas:** Cada série representa uma métrica diferente
- **Interação:** Passe o mouse para ver valores exatos

### Como Usar

1. **Navegue** até "📊 Visão Geral" na sidebar
2. **Analise** os KPIs principais no topo
3. **Observe** as setas de tendência (▲ verde = bom, ▼ vermelho = atenção)
4. **Explore** o gráfico passando o mouse sobre os pontos
5. **Compare** receitas vs custos para avaliar margem

### Casos de Uso Comuns

| Cenário | O que fazer |
|---------|-------------|
| Reunião executiva | Mostre os KPIs principais para visão rápida |
| Análise mensal | Verifique tendências no gráfico de evolução |
| Identificar problemas | Procure setas vermelhas (▼) nos deltas |

---

## 2. DRE Mensal 📈

### Propósito

A página **DRE Mensal** exibe o Demonstrativo de Resultado do Exercício completo, permitindo análise detalhada por mês e categoria.

### O que Você Verá

```
┌────────────────────────────────────────────────────────────────┐
│                     DRE MENSAL                                 │
├────────────────────────────────────────────────────────────────┤
│  ┌─ FILTROS ─────────────────────────────────────────────────┐│
│  │  Mês: [Todos ▼]        Grupo: [Todos ▼]                   ││
│  └───────────────────────────────────────────────────────────┘│
│                                                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ 💚 RECEITAS  │  │ 🔴 CUSTOS    │  │ 📊 RESULTADO │         │
│  │ R$ 6.01M     │  │ R$ 5.90M     │  │ R$ 109K      │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                │
│  ┌─ DEMONSTRATIVO DE RESULTADO ─────────────────────────────┐ │
│  │  Grupo                              │  Valor Formatado   │ │
│  │  ─────────────────────────────────────────────────────── │ │
│  │  RECEITAS S/ VENDAS                 │  R$ 6.010.000,00   │ │
│  │  (+) OUTRAS RECEITAS OPERACIONAIS   │  R$ 121.000,00     │ │
│  │  ( - ) CUSTOS VARIÁVEIS             │  -R$ 3.200.000,00  │ │
│  │  ( - ) GASTOS COM PESSOAL           │  -R$ 1.500.000,00  │ │
│  │  ( - ) DESPESAS ADMINISTRATIVAS     │  -R$ 450.000,00    │ │
│  │  ...                                │  ...               │ │
│  └───────────────────────────────────────────────────────────┘│
│                                                                │
│  ┌─ VISUALIZAÇÃO POR GRUPO ─────────────────────────────────┐ │
│  │  [Gráfico de Barras Horizontal]                          │ │
│  │                                                          │ │
│  │  RECEITAS S/ VENDAS      ████████████████████  R$ 6.01M  │ │
│  │  CUSTOS VARIÁVEIS        ████████████  -R$ 3.2M          │ │
│  │  GASTOS COM PESSOAL      ██████  -R$ 1.5M                │ │
│  │  ...                                                      │ │
│  └───────────────────────────────────────────────────────────┘│
└────────────────────────────────────────────────────────────────┘
```

### Filtros Disponíveis

| Filtro | Opções | Uso |
|--------|--------|-----|
| **Mês** | "Todos" ou mês específico (Jan-Dez) | Analisar período específico |
| **Grupo** | "Todos" ou grupo DRE específico | Focar em categoria |

### Como Usar os Filtros

1. **Selecionar Mês:**
   - Clique no dropdown "Mês"
   - Escolha "Todos" para ver o ano completo
   - Ou selecione um mês específico (ex: "Jan", "Fev")

2. **Selecionar Grupo:**
   - Clique no dropdown "Grupo"
   - Escolha "Todos" para ver todas as categorias
   - Ou selecione um grupo específico (ex: "CUSTOS VARIÁVEIS")

### Interpretação da Tabela DRE

| Tipo de Linha | Prefixo | Cor | Significado |
|---------------|---------|-----|-------------|
| Receitas | sem prefixo | Verde | Entradas de dinheiro |
| Outras Receitas | (+) | Verde | Receitas complementares |
| Custos | ( - ) | Vermelho | Saídas operacionais |
| Resultado | ( = ) | Azul | Totalizadores |

### Gráfico de Barras

- **Barras verdes (→):** Valores positivos (receitas)
- **Barras vermelhas (←):** Valores negativos (custos)
- **Orientação horizontal:** Facilita leitura de nomes longos
- **Hover:** Passe o mouse para ver valores exatos

### Passo a Passo Detalhado

1. Acesse "📈 DRE Mensal" na sidebar
2. Defina o filtro de **Mês** (ex: "Set" para setembro)
3. Observe os 3 KPIs no topo (Receitas, Custos, Resultado)
4. Role para baixo e analise a **tabela DRE**
5. Use o **gráfico de barras** para comparação visual

---

## 3. Evolução Temporal 📉

### Propósito

A página **Evolução Temporal** mostra tendências e padrões ao longo do tempo, permitindo identificar sazonalidades e comparar períodos.

### O que Você Verá

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
│  │                                                          │ │
│  │    ^                          ╱╲                         │ │
│  │    │     ╱╲    ╱╲    ╱╲     ╱  ╲                        │ │
│  │ R$ │    ╱  ╲  ╱  ╲  ╱  ╲   ╱    ╲╱                      │ │
│  │    │   ╱    ╲╱    ╲╱    ╲ ╱                              │ │
│  │    │  ╱                   ╲                              │ │
│  │    └──────────────────────────────────────────────→      │ │
│  │       Jan  Fev  Mar  Abr  Mai  Jun  Jul  Ago  Set  Out   │ │
│  │                                                          │ │
│  │    ── RECEITAS S/ VENDAS  ── CUSTOS VARIÁVEIS            │ │
│  └───────────────────────────────────────────────────────────┘│
│                                                                │
│  ┌─ RESULTADO TOTAL CONSOLIDADO ────────────────────────────┐ │
│  │  [Gráfico de Área com preenchimento]                     │ │
│  └───────────────────────────────────────────────────────────┘│
│                                                                │
│  ┌─ ANÁLISE DE VARIAÇÃO ────────────────────────────────────┐ │
│  │  Mês     │ Resultado Formatado │ Variação %              │ │
│  │  ─────────────────────────────────────────               │ │
│  │  Jan     │ R$ 95.000           │ -                       │ │
│  │  Fev     │ R$ 102.000          │ +7.4%                   │ │
│  │  Mar     │ R$ 98.000           │ -3.9%                   │ │
│  │  ...     │ ...                 │ ...                     │ │
│  └───────────────────────────────────────────────────────────┘│
└────────────────────────────────────────────────────────────────┘
```

### Configurações Disponíveis

| Configuração | Opções | Descrição |
|--------------|--------|-----------|
| **Grupos** | Multi-seleção | Escolha quais categorias exibir |
| **Tipo de Gráfico** | Linha / Barras | Formato de visualização |

### Tipos de Gráfico

| Tipo | Quando Usar | Vantagem |
|------|-------------|----------|
| **Linha** | Identificar tendências | Mostra continuidade e padrões |
| **Barras** | Comparar valores absolutos | Facilita comparação direta |

### Interatividade dos Gráficos

| Ação | Como Fazer | Resultado |
|------|------------|-----------|
| **Ver detalhes** | Passe o mouse sobre um ponto | Tooltip com valor e data |
| **Zoom** | Clique e arraste uma área | Amplia região selecionada |
| **Reset zoom** | Duplo clique no gráfico | Volta à visualização original |
| **Ocultar série** | Clique na legenda | Esconde/mostra linha específica |

### Tabela de Variação

A tabela mostra a **variação percentual** mês a mês:

- **Positivo (+):** Crescimento em relação ao mês anterior
- **Negativo (-):** Queda em relação ao mês anterior
- **Cores:** Verde para positivo, vermelho para negativo

### Passo a Passo

1. Acesse "📉 Evolução Temporal" na sidebar
2. Selecione os **grupos** que deseja comparar
3. Escolha o **tipo de gráfico** (Linha ou Barras)
4. Analise o gráfico de **Evolução por Grupo**
5. Veja o **Resultado Consolidado** (soma de todos os grupos)
6. Consulte a **Tabela de Variação** para valores exatos

---

## 4. Composição de Custos 🥧

### Propósito

A página **Composição de Custos** permite visualizar a distribuição percentual de receitas e despesas, identificando quais categorias representam maior impacto no resultado financeiro.

### O que Você Verá

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
│  │           │  └───┤        ├───┘  │                       │ │
│  │           │      │   D    │      │                       │ │
│  │           └──────┴────────┴──────┘                       │ │
│  │                                                          │ │
│  │  📋 Detalhamento das Receitas  [▼ Expandir]              │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

### Abas Disponíveis

| Aba | Ícone | Conteúdo |
|-----|-------|----------|
| **Receitas** | 💚 | Top 10 fontes de receita (valores positivos) |
| **Custos/Despesas** | 🔴 | Top 10 maiores custos (valores negativos) |
| **Hierarquia Completa** | 🗺️ | Treemap com Grupo → Categoria |

### Elementos da Interface

#### Filtro de Período

- **Mês:** Selecione "Todos" ou um mês específico
- Afeta todas as 3 abas simultaneamente

#### Gráfico de Pizza (Abas Receitas e Custos)

- **Segmentos:** Cada fatia representa uma categoria
- **Tamanho:** Proporcional ao valor absoluto
- **Cores:** Paleta automática para diferenciação
- **Hover:** Mostra nome, valor e percentual

#### Treemap (Aba Hierarquia)

O treemap é um gráfico hierárquico que mostra a estrutura completa:

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
│ │ (60%)            │ (25%)       │ (15%)         │     │
│ └──────────────────┴─────────────┴───────────────┘     │
└────────────────────────────────────────────────────────┘
```

- **Retângulo maior:** Grupo DRE (ex: RECEITAS, CUSTOS)
- **Retângulos internos:** Categorias dentro do grupo
- **Área:** Proporcional ao valor

### Como Usar

#### Passo a Passo - Análise de Receitas

1. Acesse "🥧 Composição de Custos" na sidebar
2. Selecione o período desejado no filtro **Mês**
3. Clique na aba **"💚 Receitas"**
4. Observe o gráfico de pizza com as top 10 fontes
5. Clique em **"📋 Detalhamento das Receitas"** para expandir
6. Veja a tabela com valores formatados e percentuais

#### Passo a Passo - Análise de Custos

1. Clique na aba **"🔴 Custos/Despesas"**
2. Identifique as maiores despesas no gráfico
3. Expanda o detalhamento para valores exatos
4. Compare percentuais para priorizar cortes

#### Passo a Passo - Visão Hierárquica

1. Clique na aba **"🗺️ Hierarquia Completa"**
2. Observe a estrutura Grupo → Categoria
3. Clique em um grupo para focar nele (zoom)
4. Duplo clique para voltar à visão geral

### Interpretação dos Dados

| Elemento | O que Indica | Ação Recomendada |
|----------|--------------|------------------|
| Fatia grande (>30%) | Concentração de receita/custo | Diversificar ou otimizar |
| Muitas fatias pequenas | Distribuição pulverizada | Consolidar categorias similares |
| Cores escuras | Maiores valores | Foco principal de análise |

### Expander de Detalhamento

Cada aba possui um expander com tabela detalhada:

| Coluna | Descrição |
|--------|-----------|
| **Categoria** | Nome da categoria DRE |
| **Valor Formatado** | Valor em R$ com separadores |
| **Percentual** | % do total daquela aba |

---


## 5. Previsões Financeiras 🔮

### Propósito

A página **Previsões Financeiras** utiliza o algoritmo **Facebook Prophet** para gerar projeções de receitas e custos para os próximos meses, ajudando no planejamento estratégico.

### O que Você Verá

```
┌────────────────────────────────────────────────────────────────┐
│                 PREVISÕES FINANCEIRAS                           │
├────────────────────────────────────────────────────────────────┤
│  ℹ️ Modelo Simplificado - Este previsor usa apenas 12 meses    │
│     de histórico. Use os resultados como INDICATIVO.            │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─ MÉTRICAS DO MODELO ────────────────────────────────────┐  │
│  │                                                          │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌───────────┐   │  │
│  │  │ Meses   │  │ Meses   │  │Tendência│  │ Próxima   │   │  │
│  │  │Histórico│  │Previsão │  │  ALTA   │  │ Previsão  │   │  │
│  │  │   12    │  │    6    │  │   ▲     │  │ R$ 6.2M   │   │  │
│  │  └─────────┘  └─────────┘  └─────────┘  └───────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  ┌─ GRÁFICO DE PREVISÃO ────────────────────────────────────┐  │
│  │                                        ┊                 │  │
│  │    Realizado (Azul)    ◇ Previsão (Verde)               │  │
│  │         │                  ╱                             │  │
│  │    ╭────●────╮       ◇───◇                              │  │
│  │   ╱          ╲     ╱    │                                │  │
│  │  ●            ╲   ╱     │                                │  │
│  │                ●──      │ Intervalo                      │  │
│  │                 ┊       │ Confiança                      │  │
│  │  ───────────────┊───────┴────────────►                  │  │
│  │  Jan Fev Mar Abr│Mai Jun Jul Ago                        │  │
│  │                 │                                        │  │
│  │            Início Previsão                               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  ┌─ PREVISÕES DETALHADAS ───────────────────────────────────┐  │
│  │  Mês      │ Previsão      │ Mínimo (80%) │ Máximo (80%) │  │
│  │  ─────────┼───────────────┼──────────────┼────────────── │  │
│  │  Mai/2026 │ R$ 6.200.000  │ R$ 5.800.000 │ R$ 6.600.000 │  │
│  │  Jun/2026 │ R$ 6.350.000  │ R$ 5.900.000 │ R$ 6.800.000 │  │
│  │  ...      │ ...           │ ...          │ ...          │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

### Configurações na Sidebar

| Configuração | Tipo | Opções | Descrição |
|--------------|------|--------|-----------|
| **Meses a prever** | Slider | 1-12 | Quantidade de meses futuros |
| **Grupo DRE** | Selectbox | TODOS ou específico | Categoria para previsão |
| **Gerar Previsão** | Botão | Clique | Executa o modelo Prophet |

### Métricas do Modelo

| Métrica | Descrição | Valores Ideais |
|---------|-----------|----------------|
| **Meses Histórico** | Quantidade de dados passados | 24+ meses (12 = limitado) |
| **Meses Previsão** | Período projetado | Definido pelo usuário |
| **Tendência** | Direção do movimento | ALTA / BAIXA / ESTÁVEL |
| **Próxima Previsão** | Valor do próximo mês | Valor projetado em R$ |

### Elementos do Gráfico

| Elemento | Cor | Descrição |
|----------|-----|-----------|
| **Linha Azul** | 🔵 | Valores realizados (histórico) |
| **Linha Verde** | 🟢 | Valores previstos (futuro) |
| **Linha Pontilhada** | ⚪ | Modelo ajustado ao histórico |
| **Área Sombreada** | 🔵 (transparente) | Intervalo de confiança 80% |
| **Linha Vertical** | ⚫ (tracejada) | Divisão histórico/previsão |

### Tabela de Previsões

Mostra detalhes de cada mês previsto:

| Coluna | Descrição |
|--------|-----------|
| **Mês** | Período futuro (ex: Mai/2026) |
| **Previsão** | Valor central estimado |
| **Mínimo (80%)** | Limite inferior do intervalo |
| **Máximo (80%)** | Limite superior do intervalo |

### Passo a Passo

1. Acesse **"🔮 Previsões Financeiras"** na sidebar
2. Configure o número de **meses a prever** (slider 1-12)
3. Selecione o **Grupo DRE** (TODOS ou específico)
4. Clique no botão **"Gerar Previsão"**
5. Aguarde o treinamento do modelo (5-15 segundos)
6. Analise as **métricas** no topo
7. Observe o **gráfico** com histórico e projeção
8. Consulte a **tabela** para valores exatos

### Interpretação dos Resultados

| Cenário | O que Significa | Ação |
|---------|-----------------|------|
| Tendência ALTA | Valores crescentes | Planejar capacidade |
| Tendência BAIXA | Valores decrescentes | Revisar estratégia |
| Intervalo largo | Alta incerteza | Usar valores conservadores |
| Intervalo estreito | Maior confiança | Pode confiar mais no valor central |

### Avisos e Limitações

⚠️ **Importante:** O modelo exibe avisos quando detecta limitações:

| Aviso | Causa | Recomendação |
|-------|-------|--------------|
| "Histórico limitado" | Menos de 24 meses | Coletar mais dados |
| "Sazonalidade não detectada" | Dados insuficientes | Interpretar com cautela |
| "Outliers detectados" | Valores extremos | Revisar dados fonte |

### Casos de Uso

| Situação | Como Usar |
|----------|-----------|
| **Orçamento anual** | Prever 12 meses, grupo TODOS |
| **Fluxo de caixa** | Prever 3 meses, focar em custos |
| **Análise de categoria** | Selecionar grupo específico |

---

## 6. Classificação IA 🤖

### Propósito

A página **Classificação IA** permite classificar automaticamente descrições de gastos em categorias DRE usando o modelo de linguagem **Google Gemini 2.0 Flash** com técnica **RAG** (Retrieval-Augmented Generation).

### O que Você Verá

```
┌────────────────────────────────────────────────────────────────┐
│                   CLASSIFICAÇÃO IA                              │
├────────────────────────────────────────────────────────────────┤
│  ┌─ SISTEMA DE CLASSIFICAÇÃO INTELIGENTE ───────────────────┐  │
│  │  🤖 Sistema de Classificação Inteligente                 │  │
│  │                                                          │  │
│  │  ┌─────────────┐  ┌───────────┐  ┌───────────────────┐  │  │
│  │  │ Modelo      │  │ Técnica   │  │ Contexto          │  │  │
│  │  │Gemini 2.0   │  │ RAG       │  │ categories.json   │  │  │
│  │  └─────────────┘  └───────────┘  └───────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  ┌─ TESTE DE CLASSIFICAÇÃO ─────────────────────────────────┐  │
│  │  [Digite a descrição do gasto...               ]         │  │
│  │                                                          │  │
│  │  [ 🔍 Classificar ]                                      │  │
│  │                                                          │  │
│  │  ┌─ Resultado ───────────────────────────────────────┐   │  │
│  │  │  Categoria Sugerida: BOVINOS                      │   │  │
│  │  └───────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  ┌─ HIERARQUIA DE CATEGORIAS ───────────────────────────────┐  │
│  │  [RECEITAS] [CUSTOS VAR.] [GASTOS PESSOAL] [DESP ADM]... │  │
│  │                                                          │  │
│  │  • BOVINOS        • AVES          • SUÍNOS               │  │
│  │  • PESCADOS       • EMBUTIDOS     • CONGELADOS           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  ┌─ MÉTRICAS DO MODELO ─────────────────────────────────────┐  │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐         │  │
│  │  │Acurácia│  │Precisão│  │ Recall │  │F1-Score│         │  │
│  │  │ 94.2%  │  │ 92.8%  │  │ 91.5%  │  │ 92.1%  │         │  │
│  │  │ ▲ 2.1% │  │ ▲ 1.5% │  │ ▲ 0.8% │  │ ▲ 1.2% │         │  │
│  │  └────────┘  └────────┘  └────────┘  └────────┘         │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

### Elementos da Interface

#### Painel de Informações

| Info | Valor | Descrição |
|------|-------|-----------|
| **Modelo** | Gemini 2.0 Flash | LLM do Google para classificação |
| **Técnica** | RAG | Retrieval-Augmented Generation |
| **Contexto** | categories.json | Arquivo com categorias válidas |

#### Campo de Teste

- **Input:** Campo de texto para digitar descrição do gasto
- **Botão:** "🔍 Classificar" executa a classificação
- **Resultado:** Card verde com categoria sugerida

#### Hierarquia de Categorias

- **Abas:** Navegação entre grupos DRE (máximo 6 visíveis)
- **Lista:** Categorias dentro de cada grupo
- **Contagem:** Número de categorias por grupo

#### Métricas do Modelo

| Métrica | Significado | Valor Esperado |
|---------|-------------|----------------|
| **Acurácia** | % de classificações corretas | >90% |
| **Precisão** | % de positivos corretos | >90% |
| **Recall** | % de categorias identificadas | >90% |
| **F1-Score** | Média harmônica (Precisão+Recall) | >90% |

### Como Usar

#### Passo a Passo - Classificar um Gasto

1. Acesse **"🤖 Classificação IA"** na sidebar
2. No campo de texto, digite a descrição do gasto
   - Exemplo: "Compra de picanha para churrasco"
3. Clique no botão **"🔍 Classificar"**
4. Aguarde o processamento (1-3 segundos)
5. Veja a **Categoria Sugerida** no card verde

#### Exemplos de Descrições

| Descrição | Categoria Esperada |
|-----------|-------------------|
| "Compra de picanha para churrasco" | BOVINOS |
| "Pagamento conta de energia" | ENERGIA ELÉTRICA |
| "Coca-cola e guaraná" | REFRIGERANTES |
| "Salário funcionários janeiro" | SALÁRIOS |
| "Aluguel do mês" | ALUGUEL |

### Explorar Categorias

1. Role até a seção **"📁 Hierarquia de Categorias"**
2. Clique nas abas para ver diferentes grupos:
   - RECEITAS S/ VENDAS
   - CUSTOS VARIÁVEIS
   - GASTOS COM PESSOAL
   - DESPESAS ADMINISTRATIVAS
   - etc.
3. Veja as categorias disponíveis em cada grupo
4. Use essas categorias como referência para suas descrições

### Interpretação dos Resultados

| Resultado | Cor do Card | Significado |
|-----------|-------------|-------------|
| Categoria válida | Verde | IA classificou com sucesso |
| Simulação | Amarelo | IA indisponível, usando regras |
| Erro | Vermelho | Problema na classificação |

### Histórico de Classificações

- Expanda **"📜 Histórico de Classificações"** para ver registros
- Mostra: Data, Descrição, Categoria IA, Confiança

---

## 7. Tutorial (Como Usar) ❓

### Propósito

A página **Tutorial** é a documentação integrada no próprio dashboard, com explicações rápidas sobre cada funcionalidade.

### Conteúdo Disponível

A página contém expanders com as seguintes seções:

| Seção | Conteúdo |
|-------|----------|
| **🚀 Início Rápido** | Como começar a usar |
| **📊 Visão Geral** | Explicação dos KPIs |
| **📈 DRE Mensal** | Como usar filtros e tabelas |
| **📉 Evolução** | Interpretação de gráficos |
| **🥧 Composição** | Análise de treemaps |
| **🔮 Previsões** | Limitações do Prophet |
| **🤖 Classificação IA** | Como funciona o RAG |
| **⚙️ Arquitetura** | Detalhes técnicos |
| **❓ FAQ** | Perguntas frequentes |

### Como Usar

1. Acesse **"❓ Como Usar"** na sidebar
2. Clique no expander da seção desejada
3. Leia o conteúdo explicativo
4. Use os links internos se disponíveis

---

## Solução de Problemas

### Erros Comuns e Soluções

| Problema | Causa Provável | Solução |
|----------|----------------|---------|
| "Dados não disponíveis" | Arquivos não gerados | Execute `python main.py` |
| Erro no login | Credenciais incorretas | Use `mandapicanha` / `MP@1234` |
| Gráficos não carregam | Biblioteca não instalada | Execute `pip install plotly` |
| Previsão falha | Prophet não instalado | Execute `pip install prophet` |
| IA não classifica | API key não configurada | Configure `GEMINI_API_KEY` |
| Dashboard lento | Muitos dados | Aguarde carregamento |

### Mensagens de Erro

#### "FileNotFoundError: processed_dre.parquet"

```bash
# Solução: Gerar os dados
python main.py
```

#### "Prophet não instalado"

```bash
# Solução: Instalar Prophet
pip install prophet
```

#### "Erro na classificação IA"

```bash
# Solução: Configurar variável de ambiente
# Windows:
set GEMINI_API_KEY=sua_chave_aqui

# Linux/Mac:
export GEMINI_API_KEY=sua_chave_aqui
```

### Verificações de Ambiente

```bash
# Verificar instalação de dependências
pip list | grep -i "streamlit\|prophet\|plotly\|pandas"

# Verificar arquivos de dados
ls output/
# Deve mostrar: processed_dre.parquet, categories.json

# Testar execução do dashboard
streamlit run dashboard/app.py --server.headless true
```

---

## Glossário

### Termos DRE

| Termo | Definição |
|-------|-----------|
| **DRE** | Demonstração do Resultado do Exercício - relatório financeiro |
| **Receita** | Entrada de dinheiro (valores positivos) |
| **Custo** | Saída diretamente ligada à produção |
| **Despesa** | Saída operacional não ligada à produção |
| **Resultado** | Diferença entre receitas e custos/despesas |
| **Margem** | Percentual de lucro sobre receita |

### Termos Técnicos

| Termo | Definição |
|-------|-----------|
| **Prophet** | Algoritmo de ML do Facebook para séries temporais |
| **RAG** | Retrieval-Augmented Generation - técnica de IA |
| **KPI** | Key Performance Indicator - indicador chave |
| **Treemap** | Gráfico hierárquico de áreas proporcionais |
| **Parquet** | Formato de arquivo colunar otimizado |

### Abreviações

| Abreviação | Significado |
|------------|-------------|
| **CMV** | Custo de Mercadorias Vendidas |
| **CC** | Centro de Custo |
| **IA** | Inteligência Artificial |
| **ML** | Machine Learning |
| **API** | Application Programming Interface |

---

## Contato e Suporte

- **Repositório:** https://github.com/villarantonio/Projeto_DRE
- **Issues:** https://github.com/villarantonio/Projeto_DRE/issues
- **Versão:** v1.4.0

---

*Tutorial gerado em Janeiro/2026 - Dashboard DRE Manda Picanha*
