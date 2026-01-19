# PROJETO STATUS
## Pipeline DRE - Manda Picanha

<br>

| **Informação** | **Valor** |
|----------------|-----------|
| Última atualização | 19 de Janeiro de 2026 |
| Versão | 1.1.0 |
| Repositório | github.com/villarantonio/Projeto_DRE |
| Linguagem | Python 3.11+ |
| IA | Google Gemini 2.0 Flash |
| Licença | Proprietário |

<br>

---

<div style="page-break-after: always;"></div>

## SUMÁRIO

1. Visão Geral do Projeto
2. Histórico de Desenvolvimento
3. Arquitetura Técnica Detalhada
4. Features Implementadas (Detalhamento Completo)
5. Status Atual do Pipeline
6. Roadmap Futuro e Importância das Features
7. Sugestões de Melhorias Técnicas
8. Contatos e Contribuidores

<br>

---

<div style="page-break-after: always;"></div>

## 1. VISAO GERAL DO PROJETO

### 1.1 Objetivo

O **Pipeline DRE Manda Picanha** é um sistema de automação para processamento de dados financeiros da Demonstração do Resultado do Exercício (DRE). O projeto foi desenvolvido para transformar dados brutos exportados do SharePoint em formatos otimizados para análise e treinamento de modelos de Inteligência Artificial.

<br>

### 1.2 Problema Resolvido

| Problema | Solução |
|:---------|:--------|
| Dados financeiros em formato brasileiro difícil de processar | Conversão automática de moeda (R$ 1.234,56 para float) |
| Meses em português incompatíveis com análise temporal | Conversão para timestamps padronizados |
| Hierarquia de categorias não estruturada | Extração automática para JSON |
| Dados não preparados para IA/ML | Geração de narrativas em linguagem natural |
| Arquivos Excel com metadados | Leitura inteligente pulando cabeçalhos |

<br>

### 1.3 Benefícios do Pipeline

| Benefício | Impacto |
|:----------|:--------|
| Automatização completa | Reduz tempo de processamento de horas para segundos |
| Padronização de dados | Garante consistência para análises futuras |
| Preparação para IA | Dados prontos para RAG, fine-tuning e classificação |
| Formato otimizado | Parquet reduz tamanho em até 90% vs CSV |
| CI/CD integrado | Validação automática a cada commit |

<br>

---

<div style="page-break-after: always;"></div>

## 2. HISTORICO DE DESENVOLVIMENTO

### 2.1 Cronologia de Commits

| Data | Commit | Autor | Descrição |
|:-----|:-------|:------|:----------|
| 08/01/2026 | 258cc03 | villarantonio | Initial commit: Pipeline DRE completo com 35 testes |
| 08/01/2026 | 8e124ac | villarantonio | Traduz README.md para português brasileiro |
| 10/01/2026 | 6296179 | LuccasJose | Adiciona script gerador de narrativas |
| 11/01/2026 | 3b50b49 | villarantonio | Integra narrative_generator ao pipeline ETL |
| 11/01/2026 | fcf471d | villarantonio | Adiciona suporte a arquivos Excel do SharePoint |

<br>

### 2.2 Evolução do Projeto

**Semana 1 (08-10/01/2026):**
- Criação da estrutura base do projeto
- Implementação do pipeline ETL para CSV
- Desenvolvimento de 35 testes unitários
- Tradução da documentação para português

**Semana 2 (10-11/01/2026):**
- Contribuição externa: módulo de narrativas (LuccasJose)
- Integração do gerador de narrativas ao pipeline principal
- Migração de CSV para Excel como formato primário
- Expansão para 56 testes unitários

<br>

---

<div style="page-break-after: always;"></div>

## 3. ARQUITETURA TECNICA DETALHADA

### 3.1 Estrutura de Arquivos do Projeto

| Caminho | Linhas | Descrição |
|:--------|-------:|:----------|
| config.py | 118 | Configurações centralizadas do projeto |
| main.py | 219 | Orquestrador principal do pipeline ETL |
| src/data_cleaner.py | 415 | Módulo de carregamento e limpeza de dados |
| src/category_engine.py | 244 | Motor de extração de hierarquia de categorias |
| src/narrative_generator.py | 235 | Gerador de narrativas para IA |
| **src/ai_classifier.py** | **262** | **Classificador IA com RAG (Google Gemini)** |
| **src/data_processor_ia.py** | **235** | **Processador com trava de segurança** |
| tests/test_data_cleaner.py | - | 29 testes unitários para limpeza |
| tests/test_category_engine.py | - | 11 testes unitários para categorias |
| tests/test_narrative_generator.py | - | 15 testes unitários para narrativas |
| **tests/test_classificador_ia.py** | **232** | **Testes para classificador IA** |
| **tests/test_processador_ia.py** | **227** | **Testes para processador IA** |

**Arquivos de Workflow (GitHub Actions):**

| Caminho | Descrição |
|:--------|:----------|
| .github/workflows/process_dre.yml | CI/CD principal - executa testes |
| **.github/workflows/classificacao.yml** | **Classificação automática via IA** |
| **.github/workflows/processar_narrativas.yml** | **Geração de narrativas automática** |

<br>

### 3.2 Fluxo Completo do Pipeline ETL

| Step | Módulo | Função | Entrada | Saída |
|:----:|:-------|:-------|:--------|:------|
| 1 | data_cleaner | load_dre_file() | DRE_BI.xlsx | DataFrame |
| 2 | data_cleaner | apply_currency_conversion() | Coluna Realizado | Float values |
| 3 | data_cleaner | apply_month_conversion() | Coluna Mês | Timestamps |
| 4 | category_engine | extract_category_hierarchy() | DataFrame | Dict hierarchy |
| 5 | pandas | to_parquet() | DataFrame | .parquet file |
| 6 | category_engine | save_categories_json() | Dict | .json file |
| 7 | narrative_gen | generate_narratives() | DataFrame | DataFrame + texto |
| 8 | narrative_gen | save_narrative_report() | DataFrame | .csv file |

<br>

### 3.3 Arquivos de Saída Gerados

| Arquivo | Formato | Tamanho Típico | Finalidade |
|:--------|:--------|---------------:|:-----------|
| processed_dre.parquet | Apache Parquet | ~50KB | Análise rápida com pandas/polars |
| categories.json | JSON | ~5KB | Contexto para RAG e LLM |
| relatorio_narrativo_ia.csv | CSV UTF-8 BOM | ~200KB | Fine-tuning de modelos de IA |

<br>

### 3.4 Dependências do Projeto

| Pacote | Versão | Uso | Status |
|:-------|:-------|:----|:------:|
| pandas | >=2.0.0 | Manipulação de DataFrames | Ativo |
| numpy | >=1.24.0 | Operações numéricas | Ativo |
| openpyxl | >=3.1.0 | Leitura de arquivos Excel | Ativo |
| pyarrow | >=14.0.0 | Engine para Parquet | Ativo |
| pytest | >=7.0.0 | Framework de testes | Ativo |
| **google-generativeai** | **>=0.3.0** | **API Google Gemini (IA)** | **Ativo** |
| prophet | >=1.1.0 | Previsões (Prophet) | Futuro |
| openai | >=1.0.0 | OpenAI (alternativa) | Futuro |

<br>

---

<div style="page-break-after: always;"></div>

## 4. FEATURES IMPLEMENTADAS - DETALHAMENTO COMPLETO

### 4.1 Carregamento Inteligente de Arquivos (data_cleaner.py)

**O que faz:**
O módulo detecta automaticamente o formato do arquivo de entrada (Excel ou CSV) e aplica a configuração correta de leitura. Arquivos Excel do SharePoint frequentemente possuem 4 linhas de metadados antes do cabeçalho real, que são ignoradas automaticamente.

**Funções principais:**

| Função | Descrição Detalhada |
|:-------|:--------------------|
| load_dre_file() | Ponto de entrada principal. Detecta extensão (.xlsx, .xls, .csv) e redireciona para o loader correto. |
| load_dre_excel() | Usa openpyxl para ler Excel. Pula 4 linhas de metadados (header=4). Valida colunas obrigatórias. |
| load_dre_csv() | Mantido para compatibilidade. Usa encoding latin-1 e separador ponto-vírgula (padrão BR). |
| _validate_dre_dataframe() | Verifica se DataFrame não está vazio e se colunas obrigatórias existem. |

**Por que é importante:**
- Arquivos do SharePoint têm formato específico com metadados
- Detecção automática evita erros de configuração
- Validação previne falhas silenciosas no pipeline

<br>

---

<div style="page-break-after: always;"></div>

### 4.2 Conversão de Moeda Brasileira (data_cleaner.py)

**O que faz:**
Converte strings no formato monetário brasileiro (ex: "R$ 1.234,56") para valores numéricos float. Trata casos especiais como valores negativos, ausência de centavos e valores nulos.

**Exemplos de conversão:**

| Entrada | Saída | Observação |
|:--------|------:|:-----------|
| "R$ 1.234,56" | 1234.56 | Formato padrão |
| "-R$ 1.234,56" | -1234.56 | Valor negativo |
| "R$ 0,00" | 0.0 | Zero |
| "R$ 63.713" | 63713.0 | Sem centavos |
| "" ou NaN | 0.0 | Valor ausente |

**Algoritmo:**
1. Remove prefixo "R$" e espaços
2. Detecta sinal negativo (- ou parênteses)
3. Remove pontos (separador de milhar)
4. Substitui vírgula por ponto (decimal)
5. Converte para float

**Por que é importante:**
- Formato brasileiro é incompatível com operações matemáticas
- Permite cálculos de totais, médias e análises estatísticas
- Essencial para comparações e ordenações numéricas

<br>

---

<div style="page-break-after: always;"></div>

### 4.3 Conversão de Meses em Português (data_cleaner.py)

**O que faz:**
Transforma abreviações de meses em português (Jan, Fev, Mar, etc.) em objetos Timestamp do pandas, permitindo análises temporais e ordenação cronológica.

**Mapeamento completo:**

| Abreviação | Mês | Timestamp Gerado |
|:-----------|----:|:-----------------|
| Jan | 1 | 2025-01-01 |
| Fev | 2 | 2025-02-01 |
| Mar | 3 | 2025-03-01 |
| Abr | 4 | 2025-04-01 |
| Mai | 5 | 2025-05-01 |
| Jun | 6 | 2025-06-01 |
| Jul | 7 | 2025-07-01 |
| Ago | 8 | 2025-08-01 |
| Set | 9 | 2025-09-01 |
| Out | 10 | 2025-10-01 |
| Nov | 11 | 2025-11-01 |
| Dez | 12 | 2025-12-01 |

**Por que é importante:**
- Permite ordenação cronológica correta (Jan < Fev < Mar)
- Habilita agrupamentos por trimestre, semestre
- Necessário para séries temporais e previsões (Prophet)
- Formato padrão para integração com outras ferramentas

<br>

---

<div style="page-break-after: always;"></div>

### 4.4 Extração de Hierarquia de Categorias (category_engine.py)

**O que faz:**
A classe CategoryManager extrai a estrutura hierárquica única de categorias financeiras do DataFrame. Agrupa os itens detalhados (cc_nome) sob suas categorias macro (Nome Grupo).

**Estrutura de saída (categories.json):**

```
{
  "RECEITAS S/ VENDAS": ["DINHEIRO", "IFOOD", "PIX", "TED/DOC", ...],
  "CUSTOS VARIÁVEIS": ["AÇOUGUE", "CARVÃO", "BEBIDAS", ...],
  "DESPESAS FIXAS": ["ALUGUEL", "ENERGIA", "INTERNET", ...],
  ...
}
```

**Métodos da classe:**

| Método | Descrição |
|:-------|:----------|
| extract_category_hierarchy() | Agrupa cc_nome por Nome Grupo, remove duplicatas, ordena alfabeticamente |
| save_categories_json() | Salva hierarquia em JSON com indentação, encoding UTF-8 |
| load_categories_json() | Carrega JSON existente para uso incremental |
| get_category_summary() | Retorna estatísticas: total de grupos, itens por grupo |

**Por que é importante:**
- Contexto estruturado para RAG (Retrieval-Augmented Generation)
- Permite LLM classificar novos itens em categorias existentes
- Base para análises comparativas entre períodos
- Documenta taxonomia financeira da empresa

<br>

---

<div style="page-break-after: always;"></div>

### 4.5 Gerador de Narrativas para IA (narrative_generator.py)

**O que faz:**
Transforma cada linha de dados financeiros em uma frase em linguagem natural, criando um dataset adequado para treinamento e fine-tuning de modelos de linguagem.

**Exemplo de narrativa gerada:**

| Dados de Entrada | Narrativa Gerada |
|:-----------------|:-----------------|
| Mês: Ago, Grupo: RECEITAS, Item: PIX, Valor: 15000.50 | "Em Ago, o grupo 'RECEITAS S/ VENDAS' registrou um valor de R$ 15.000,50 referente ao item 'PIX'." |

**Funções do módulo:**

| Função | Descrição |
|:-------|:----------|
| clean_text() | Corrige caracteres corrompidos em exports brasileiros (mojibake) |
| create_narrative() | Gera frase para uma única linha de dados |
| generate_narratives() | Processa DataFrame inteiro, adiciona coluna Narrativa_IA |
| save_narrative_report() | Salva CSV com BOM UTF-8 (compatível com Excel) |
| get_narrative_summary() | Estatísticas: total gerado, tamanho médio das narrativas |

**Correções de texto aplicadas:**

| Texto Corrompido | Correção |
|:-----------------|:---------|
| VARIVEIS | VARIÁVEIS |
| DEDUES | DEDUÇÕES |
| SERVIOS | SERVIÇOS |
| SALRIO | SALÁRIO |

**Por que é importante:**
- Fine-tuning de LLMs requer dados em linguagem natural
- Melhora interpretação de contexto financeiro por IA
- Base para geração de relatórios automáticos
- Treina modelos a entender terminologia contábil

<br>

---

<div style="page-break-after: always;"></div>

### 4.6 Suporte a Arquivos Excel do SharePoint

**O que faz:**
Permite carregar diretamente arquivos .xlsx exportados do SharePoint da empresa, sem necessidade de conversão manual para CSV.

**Configurações específicas:**

| Parâmetro | Valor | Motivo |
|:----------|:------|:-------|
| EXCEL_HEADER_ROW | 4 | SharePoint adiciona 4 linhas de metadados |
| EXCEL_SHEET_NAME | 0 | Dados na primeira planilha |
| Engine | openpyxl | Biblioteca padrão para .xlsx |

**Vantagens sobre CSV:**

| Aspecto | CSV | Excel |
|:--------|:----|:------|
| Preserva formatação | Não | Sim |
| Problemas de encoding | Frequentes | Raros |
| Múltiplas planilhas | Não | Sim |
| Fórmulas preservadas | Não | Sim |
| Tamanho do arquivo | Maior | Menor (comprimido) |

**Por que é importante:**
- Elimina etapa manual de conversão
- Reduz erros de encoding (acentos, cedilha)
- Fluxo direto do SharePoint para o pipeline
- Formato nativo do Power BI e ferramentas Microsoft

<br>

---

<div style="page-break-after: always;"></div>

### 4.7 Pipeline CI/CD com GitHub Actions

**O que faz:**
Automatiza execução de testes e processamento de dados a cada push para o repositório. Garante qualidade do código e detecta regressões imediatamente.

**Jobs do workflow (process_dre.yml):**

| Job | Duração | Descrição |
|:----|--------:|:----------|
| Run Tests | ~30s | Executa pytest com 56 testes unitários |
| Process DRE Financial Data | ~30s | Roda main.py, gera arquivos de saída |
| Validate Processed Data | ~20s | Verifica integridade dos arquivos gerados |

**Tecnologias utilizadas:**

| Componente | Tecnologia |
|:-----------|:-----------|
| Runner | ubuntu-latest |
| Python | 3.11 |
| Cache | pip dependencies (~118MB) |
| Trigger | push to main, pull_request |

**Por que é importante:**
- Detecta bugs antes de chegar em produção
- Documenta que código funciona corretamente
- Facilita revisão de Pull Requests
- Gera artefatos de saída automaticamente

<br>

---

<div style="page-break-after: always;"></div>

## 5. STATUS ATUAL DO PIPELINE

### 5.1 Último Commit

| Campo | Valor |
|:------|:------|
| SHA | fcf471d4079d4efa94a1db1a8ecb5ae9776cb25a |
| Mensagem | feat: Adiciona suporte a arquivos Excel do SharePoint |
| Autor | Antonio Henrique (villarantonio) |
| Data | 11/01/2026 às 21:57:56 UTC |
| Branch | main |

<br>

### 5.2 Resultado do Workflow (GitHub Actions Run #5)

| Job | Status | Duração |
|:----|:------:|--------:|
| Run Tests | SUCCESS | 29s |
| Process DRE Financial Data | SUCCESS | 28s |
| Validate Processed Data | SUCCESS | 19s |

<br>

### 5.3 Cobertura de Testes por Módulo

| Arquivo de Teste | Testes | Status | Tempo |
|:-----------------|-------:|:------:|------:|
| test_data_cleaner.py | 29 | PASSED | 0.15s |
| test_category_engine.py | 11 | PASSED | 0.01s |
| test_narrative_generator.py | 15 | PASSED | 0.02s |
| **TOTAL** | **56** | **100%** | **0.63s** |

<br>

### 5.4 Configurações Atuais do Pipeline

| Parâmetro | Valor | Descrição |
|:----------|:------|:----------|
| INPUT_FILE_NAME | DRE_BI.xlsx | Arquivo de entrada |
| EXCEL_HEADER_ROW | 4 | Cabeçalho na linha 5 |
| EXCEL_SHEET_NAME | 0 | Primeira planilha |
| REFERENCE_YEAR | 2025 | Ano para timestamps |
| REQUIRED_COLUMNS | Nome Grupo, cc_nome, Mês, Realizado | Colunas obrigatórias |

<br>

---

<div style="page-break-after: always;"></div>

## 6. ROADMAP FUTURO E IMPORTANCIA DAS FEATURES

### 6.1 Fase 1: Previsões com Prophet (T1 2026)

**Estimativa: 25 horas de desenvolvimento**

| Item | Prioridade | Esforço |
|:-----|:----------:|--------:|
| Instalar Prophet no requirements.txt | Alta | 1h |
| Criar src/forecaster.py | Alta | 8h |
| Previsão de receita mensal | Alta | 4h |
| Previsão de custos por categoria | Média | 4h |
| Visualização de tendências | Média | 4h |
| Testes para forecaster | Alta | 4h |

**IMPORTANCIA DESTA FEATURE:**

Prophet é uma biblioteca de previsão de séries temporais desenvolvida pelo Facebook/Meta. Sua integração permitirá:

| Benefício | Impacto no Negócio |
|:----------|:-------------------|
| Previsão de receita | Planejamento financeiro mais preciso |
| Detecção de sazonalidade | Identificar padrões mensais de vendas |
| Anomalias | Alertar sobre desvios significativos |
| Projeção de custos | Antecipar necessidades de capital de giro |

**Caso de uso prático:**
"Com base nos últimos 12 meses, projetamos receita de R$ 850.000 para março/2026, com intervalo de confiança de R$ 780.000 a R$ 920.000."

**Bloqueadores técnicos:**
- Prophet requer histórico mínimo de 2 anos para previsões confiáveis
- Dados atuais podem ter apenas 12 meses (necessário verificar)

<br>

---

<div style="page-break-after: always;"></div>

### 6.2 Fase 2: Classificação por IA com Google Gemini (T1 2026)

**STATUS: 🟡 EM ANDAMENTO (60% concluído)**

> **NOTA:** Esta fase foi implementada usando **Google Gemini 2.0 Flash** em vez de OpenAI GPT-4 conforme planejado originalmente. Veja seção "Decisão Arquitetural" abaixo.

**Estimativa original: 51 horas | Executado: ~30 horas**

| Item | Prioridade | Esforço | Status |
|:-----|:----------:|--------:|:------:|
| ~~Configurar API key (Gemini)~~ | Alta | 1h | ✅ Concluído |
| ~~Criar src/ai_classifier.py~~ | Alta | 12h | ✅ Concluído |
| ~~RAG com categories.json~~ | Alta | 8h | ✅ Concluído |
| ~~Classificação automática de novos itens~~ | Alta | 8h | ✅ Concluído |
| Fine-tuning com narrativas | Baixa | 16h | ⏳ Pendente |
| ~~Testes para ai_classifier~~ | Alta | 6h | ✅ Concluído |

**DECISÃO ARQUITETURAL - Gemini vs OpenAI:**

| Aspecto | OpenAI (Planejado) | Google Gemini (Implementado) |
|:--------|:-------------------|:-----------------------------|
| Modelo | GPT-4 Turbo | Gemini 2.0 Flash |
| Custo | ~$0.01/1K tokens | Tier gratuito disponível |
| Latência | ~2-3s | ~1-2s |
| SDK | openai>=1.0.0 | google-generativeai>=0.3.0 |
| Motivo | - | Custo inicial zero, velocidade |

**IMPORTANCIA DESTA FEATURE:**

A classificação por IA automatiza um processo atualmente manual e propenso a erros. Usando RAG (Retrieval-Augmented Generation), o sistema consultará o categories.json para classificar novos itens.

| Benefício | Impacto no Negócio |
|:----------|:-------------------|
| Classificação automática | Elimina trabalho manual repetitivo |
| Consistência | Mesmos critérios aplicados sempre |
| Velocidade | Classifica milhares de itens em segundos |
| Aprendizado | Fine-tuning melhora precisão com o tempo |

**Exemplo de uso (FUNCIONANDO):**
- **Entrada:** "Pagamento fornecedor carne"
- **Saída IA:** Categoria "BOVINOS" (grupo: CUSTOS VARIÁVEIS)

**Arquitetura implementada:**

| Componente | Função |
|:-----------|:-------|
| categories.json | Base de conhecimento (contexto RAG) |
| relatorio_narrativo_ia.csv | Dataset para fine-tuning |
| GPT-4 API | Modelo base para classificação |
| src/ai_classifier.py | Orquestração e prompts |

**Bloqueadores:**
- Custos de API OpenAI (estimar R$ 100-500/mês dependendo do volume)
- Latência de classificação em lote (considerar batch API)

<br>

---

<div style="page-break-after: always;"></div>

### 6.3 Fase 3: Dashboard Interativo com Streamlit (T3 2026)

**Estimativa: 48 horas de desenvolvimento**

| Item | Prioridade | Esforço |
|:-----|:----------:|--------:|
| Configurar Streamlit no projeto | Alta | 2h |
| Criar dashboard/app.py | Alta | 16h |
| Visualização de DRE mensal | Alta | 8h |
| Gráficos de tendência | Média | 6h |
| Filtros interativos | Média | 4h |
| Export para Excel/PDF | Baixa | 8h |
| Deploy no Streamlit Cloud | Baixa | 4h |

**IMPORTANCIA DESTA FEATURE:**

Streamlit permite criar dashboards interativos com Python puro, sem necessidade de frontend separado. A visualização de dados financeiros em tempo real melhora a tomada de decisão.

| Benefício | Impacto no Negócio |
|:----------|:-------------------|
| Visualização intuitiva | Gestores entendem dados sem planilhas |
| Filtros dinâmicos | Análise por período, categoria, loja |
| Acesso web | Disponível de qualquer dispositivo |
| Exportação | Relatórios em PDF para reuniões |

**Visualizações planejadas:**

| Gráfico | Dados |
|:--------|:------|
| Barras empilhadas | Receitas vs Custos por mês |
| Linha temporal | Evolução do resultado líquido |
| Pizza/Donut | Composição de custos variáveis |
| Tabela pivot | DRE completo com drill-down |
| KPIs cards | Margem bruta, EBITDA, variação % |

**Tecnologias:**
- Streamlit 1.30+ para interface
- Plotly/Altair para gráficos interativos
- Streamlit Cloud para hospedagem gratuita

<br>

---

<div style="page-break-after: always;"></div>

### 6.4 Fase 4: Suporte Multi-Empresa (T4 2026)

**Estimativa: 52 horas de desenvolvimento**

| Item | Prioridade | Esforço |
|:-----|:----------:|--------:|
| Refatorar config para multi-tenant | Alta | 8h |
| Suporte a múltiplos arquivos DRE | Alta | 8h |
| Consolidação de relatórios | Média | 12h |
| Análise comparativa | Média | 8h |
| Dashboard multi-empresa | Baixa | 16h |

**IMPORTANCIA DESTA FEATURE:**

O grupo Manda Picanha pode expandir para múltiplas unidades ou marcas. O suporte multi-empresa permite análise consolidada e comparativa.

| Benefício | Impacto no Negócio |
|:----------|:-------------------|
| Visão consolidada | Resultado total do grupo |
| Benchmark interno | Comparar performance entre unidades |
| Escalabilidade | Adicionar novas empresas facilmente |
| Governança | Padronização de categorias entre unidades |

**Arquitetura proposta:**

| Componente | Mudança |
|:-----------|:--------|
| config.py | Dict de empresas com configs individuais |
| main.py | Loop para processar múltiplos arquivos |
| output/ | Subpastas por empresa + consolidado |
| dashboard | Filtro de empresa + visão grupo |

**Exemplo de estrutura:**

```
output/
├── empresa_1/
│   ├── processed_dre.parquet
│   └── categories.json
├── empresa_2/
│   ├── processed_dre.parquet
│   └── categories.json
└── consolidado/
    ├── all_companies.parquet
    └── unified_categories.json
```

<br>

---

<div style="page-break-after: always;"></div>

### 6.5 Resumo do Roadmap Completo

| Fase | Período | Horas | Status | Progresso |
|:-----|:--------|------:|:------:|:---------:|
| Fase 1 - Prophet | T1 2026 | 25h | Planejado | 0% |
| **Fase 2 - IA/Gemini** | **T1 2026** | **51h** | **Em Andamento** | **60%** |
| Fase 3 - Dashboard | T3 2026 | 48h | Planejado | 0% |
| Fase 4 - Multi-Empresa | T4 2026 | 52h | Planejado | 0% |
| **TOTAL** | **2026** | **176h** | **Em Progresso** | **~17%** |

**Ordem de implementação (ATUALIZADA):**

| Ordem | Feature | Status | Próximos Passos |
|:-----:|:--------|:------:|:----------------|
| 1 | ~~IA/Gemini~~ | 🟡 60% | Completar fine-tuning |
| 2 | Prophet | ⏳ | Aguardando mais dados |
| 3 | Dashboard | ⏳ | Após Fase 2 completa |
| 4 | Multi-Empresa | ⏳ | Depende de demanda |

<br>

---

<div style="page-break-after: always;"></div>

## 7. SUGESTOES DE MELHORIAS TECNICAS

### 7.1 Melhorias de Performance

| Melhoria | Descrição | Impacto Esperado |
|:---------|:----------|:-----------------|
| Processamento paralelo | Usar multiprocessing para conversão de moeda em DataFrames grandes | 3-5x mais rápido |
| Caching inteligente | Implementar cache LRU de categorias já extraídas | Reduz I/O em 80% |
| Lazy loading | Carregar apenas colunas necessárias do Excel | 50% menos memória |
| Chunked processing | Processar Excel em chunks de 10k linhas | Suporta arquivos >1GB |

<br>

### 7.2 Melhorias de Arquitetura

| Melhoria | Descrição | Benefício |
|:---------|:----------|:----------|
| Injeção de dependência | Usar dataclass para configuração em vez de módulo global | Facilita testes e mocking |
| Tipagem estrita | Adicionar py.typed e verificação com mypy | Detecta bugs em compile-time |
| Logging estruturado | Migrar para structlog com JSON output | Melhor rastreabilidade |
| Padrão Repository | Abstrair persistência de dados | Facilita trocar storage |

<br>

### 7.3 Melhorias de Qualidade

| Melhoria | Ferramenta | Descrição |
|:---------|:-----------|:----------|
| Cobertura de testes | pytest-cov | Métricas de cobertura no CI |
| Linting automático | ruff | 10x mais rápido que flake8 |
| Formatação | black + isort | Código consistente |
| Pre-commit hooks | pre-commit | Validação antes de commits |
| Type checking | mypy --strict | Verificação de tipos |

<br>

---

<div style="page-break-after: always;"></div>

## 8. CONTATOS E CONTRIBUIDORES

### 8.1 Time de Desenvolvimento

| Papel | Nome | GitHub | Contribuições |
|:------|:-----|:-------|:--------------|
| Maintainer | Antonio Henrique | villarantonio | Pipeline ETL, CI/CD, integração |
| Contributor | Luccas Jose | LuccasJose | Gerador de narrativas |

<br>

### 8.2 Como Contribuir

| Passo | Ação |
|:------|:-----|
| 1 | Fork do repositório |
| 2 | Criar branch feature/nome-da-feature |
| 3 | Implementar com testes |
| 4 | Abrir Pull Request |
| 5 | Aguardar review e CI passar |

<br>

### 8.3 Links Úteis

| Recurso | URL |
|:--------|:----|
| Repositório | github.com/villarantonio/Projeto_DRE |
| Issues | github.com/villarantonio/Projeto_DRE/issues |
| Actions | github.com/villarantonio/Projeto_DRE/actions |

<br>

---

<br>

<br>

**PROJETO STATUS - Pipeline DRE Manda Picanha**

**Documento gerado em 11 de Janeiro de 2026**

**Versão 1.0.0**

<br>

---

<br>

*Este documento foi preparado para conversão em PDF.*

*Todas as informações refletem o estado do projeto na data de geração.*

*Para informações atualizadas, consulte o repositório GitHub.*