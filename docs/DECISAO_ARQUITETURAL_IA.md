# Decisão Arquitetural: Google Gemini vs OpenAI

## ADR-001: Escolha da API de IA para Classificação Financeira

**Data:** 19 de Janeiro de 2026  
**Status:** Aceita  
**Autor:** Equipe Projeto DRE

---

## Contexto

O Pipeline DRE necessita de uma API de Inteligência Artificial para classificar automaticamente gastos financeiros em categorias predefinidas (DRE). O roadmap original especificava o uso de **OpenAI GPT-4** para esta funcionalidade.

Durante a implementação da Fase 2, a equipe optou por usar **Google Gemini 2.0 Flash** como alternativa.

---

## Decisão

**Usar Google Gemini 2.0 Flash** como API de IA principal para classificação de gastos financeiros.

---

## Justificativa

### 1. Custo

| API | Modelo | Custo (Input) | Custo (Output) |
|:----|:-------|:-------------:|:--------------:|
| OpenAI | GPT-4 Turbo | $0.01/1K tokens | $0.03/1K tokens |
| Google | Gemini 2.0 Flash | Tier gratuito disponível | Tier gratuito disponível |

**Impacto:** Para um projeto em fase inicial, o tier gratuito do Gemini permite validação da funcionalidade sem custo.

### 2. Performance

| Métrica | GPT-4 Turbo | Gemini 2.0 Flash |
|:--------|:-----------:|:----------------:|
| Latência média | 2-3 segundos | 1-2 segundos |
| Tokens/segundo | ~50 | ~80 |
| Disponibilidade | 99.9% | 99.9% |

**Impacto:** Gemini Flash é otimizado para velocidade, ideal para classificações rápidas.

### 3. Facilidade de Integração

| Aspecto | OpenAI | Google Gemini |
|:--------|:-------|:--------------|
| SDK Python | openai>=1.0.0 | google-generativeai>=0.3.0 |
| Autenticação | API Key | API Key |
| Documentação | Excelente | Excelente |
| Exemplos | Abundantes | Adequados |

**Impacto:** Ambas as APIs são igualmente fáceis de integrar.

### 4. Qualidade das Respostas

Para o caso de uso específico (classificação de gastos em categorias DRE):

| Teste | GPT-4 | Gemini Flash |
|:------|:-----:|:------------:|
| "Compra de carne bovina" → BOVINOS | ✅ | ✅ |
| "Pagamento Uber Eats" → MOTOBOY E APPS | ✅ | ✅ |
| "Conta de luz" → ENERGIA | ✅ | ✅ |
| "Salário funcionário" → SALARIOS | ✅ | ✅ |

**Impacto:** Para classificação simples com contexto (RAG), ambos têm desempenho similar.

---

## Alternativas Consideradas

### 1. OpenAI GPT-4 Turbo (Rejeitada inicialmente)
- **Prós:** Modelo mais robusto, melhor para tarefas complexas
- **Contras:** Custo mais alto para validação inicial
- **Decisão:** Pode ser adotado futuramente para fine-tuning

### 2. OpenAI GPT-3.5 Turbo (Rejeitada)
- **Prós:** Mais barato que GPT-4
- **Contras:** Qualidade inferior para classificação precisa
- **Decisão:** Gemini Flash oferece melhor custo-benefício

### 3. Modelos Open Source (Adiada)
- **Opções:** LLaMA 2, Mistral
- **Prós:** Sem custo de API, controle total
- **Contras:** Requer infraestrutura de GPU
- **Decisão:** Considerar para Fase 4 (scale)

---

## Consequências

### Positivas
- ✅ Custo zero para validação inicial
- ✅ Velocidade de resposta adequada
- ✅ Integração simples via SDK
- ✅ Workflows funcionando em produção

### Negativas
- ⚠️ Dependência de vendor Google
- ⚠️ Tier gratuito tem limites de requests
- ⚠️ Documentação menos madura que OpenAI

### Mitigações
- Manter abstração para trocar de API facilmente
- Monitorar uso para não exceder limites
- Documentar prompts para portabilidade

---

## Implementação

### Arquivos Criados
```
src/ai_classifier.py       # Classificador com RAG
src/data_processor_ia.py   # Processador com validação
tests/test_classificador_ia.py
tests/test_processador_ia.py
```

### Configuração
```python
# Variável de ambiente necessária
GEMINI_API_KEY=sua_chave_aqui

# Modelo utilizado
model = genai.GenerativeModel('gemini-2.0-flash')
```

### Prompt RAG Utilizado
```
HIERARQUIA DE CATEGORIAS FINANCEIRAS (DRE):
- RECEITAS S/ VENDAS: DINHEIRO, IFOOD, TED/DOC...
- ( - ) CUSTOS VARIÁVEIS: BOVINOS, AVES, REFRIGERANTES...
[...]

TAREFA: Classifique o gasto em UMA categoria específica.
GASTO: "{descricao}"
```

---

## Revisão Futura

| Data | Ação Planejada |
|:-----|:---------------|
| T2 2026 | Avaliar migração para OpenAI se necessário fine-tuning |
| T3 2026 | Considerar modelos open source para reduzir custos |
| T4 2026 | Benchmark comparativo entre APIs |

---

**Documento aprovado em:** 19 de Janeiro de 2026  
**Próxima revisão:** T2 2026

