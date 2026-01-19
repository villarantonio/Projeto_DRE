# Documentação de Prompts de IA

## Pipeline DRE - Manda Picanha

Este documento descreve os prompts utilizados nos módulos de IA do projeto, configurações recomendadas e boas práticas para classificação financeira.

---

## Índice

1. [Visão Geral](#visão-geral)
2. [Prompt de Classificação](#prompt-de-classificação)
3. [Configurações do Modelo](#configurações-do-modelo)
4. [Contexto RAG](#contexto-rag)
5. [Fine-tuning](#fine-tuning)
6. [Métricas de Qualidade](#métricas-de-qualidade)
7. [Troubleshooting](#troubleshooting)

---

## Visão Geral

O projeto utiliza **Google Gemini 2.0 Flash** para classificação automática de gastos financeiros. A IA recebe descrições de transações e retorna a categoria DRE correspondente.

### Arquitetura

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  entrada.csv │ ──▶ │ ai_classifier │ ──▶ │  categoria  │
│  (descrição) │     │   + RAG ctx   │     │   (cc_nome) │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                    ┌──────┴──────┐
                    │ categories  │
                    │    .json    │
                    └─────────────┘
```

---

## Prompt de Classificação

### Prompt Principal (`src/ai_classifier.py`)

```python
prompt = f"""
Você é um especialista em classificação financeira para restaurantes.

{contexto}

TAREFA: Classifique o gasto abaixo em UMA categoria específica (cc_nome).
GASTO: "{descricao}"

REGRAS:
1. Responda APENAS com o nome exato da categoria (ex: BOVINOS, REFRIGERANTES)
2. NÃO inclua o grupo (ex: "( - ) CUSTOS VARIÁVEIS")
3. Se não encontrar categoria adequada, responda "OUTROS"
"""
```

### Variáveis do Prompt

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `{contexto}` | Hierarquia de categorias do RAG | Ver seção [Contexto RAG](#contexto-rag) |
| `{descricao}` | Descrição do gasto a classificar | "Pagamento fornecedor carne" |

### Exemplos de Classificação

| Entrada | Saída Esperada | Grupo |
|---------|----------------|-------|
| "Compra de picanha" | BOVINOS | CUSTOS VARIÁVEIS |
| "Pagamento Coca-Cola" | REFRIGERANTES | CUSTOS VARIÁVEIS |
| "Aluguel mensal" | ALUGUEL | DESPESAS FIXAS |
| "Venda cartão crédito" | CARTÃO | RECEITAS S/ VENDAS |
| "Gasto não identificado" | OUTROS | - |

---

## Configurações do Modelo

### Modelo Utilizado

```python
# src/ai_classifier.py
MODEL_NAME = "gemini-2.0-flash"
```

### Parâmetros Recomendados

| Parâmetro | Valor | Motivo |
|-----------|-------|--------|
| `temperature` | 0.1 | Respostas mais determinísticas |
| `max_output_tokens` | 50 | Resposta curta (apenas categoria) |
| `top_p` | 0.95 | Balanceia diversidade/precisão |

### Exemplo de Configuração Avançada

```python
generation_config = {
    "temperature": 0.1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 50,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
]
```

---

## Contexto RAG

### Formato do Contexto

O contexto RAG é construído a partir do `categories.json`:

```python
def formatar_contexto_rag(categorias_dict: dict) -> str:
    contexto_partes = []
    for grupo, categorias in categorias_dict.items():
        cats_str = ", ".join(categorias)
        contexto_partes.append(f"- {grupo}: {cats_str}")
    return "\n".join(contexto_partes)
```

### Exemplo de Contexto Gerado

```
HIERARQUIA DE CATEGORIAS FINANCEIRAS (DRE):
- RECEITAS S/ VENDAS: DINHEIRO, PIX, CARTÃO, IFOOD, TED/DOC
- ( - ) CUSTOS VARIÁVEIS: BOVINOS, SUÍNOS, AVES, BEBIDAS, HORTIFRUTI
- ( - ) DESPESAS FIXAS: ALUGUEL, ENERGIA, ÁGUA, INTERNET, TELEFONE
- ( - ) DESPESAS VARIÁVEIS: MARKETING, MANUTENÇÃO, MATERIAIS
```

### Benefícios do RAG

1. **Contexto atualizado**: Sempre usa categorias atuais do sistema
2. **Sem alucinação**: Limita respostas às categorias existentes
3. **Flexível**: Novas categorias são automaticamente incluídas

---

## Fine-tuning

### Dataset de Fine-tuning

O módulo `src/finetune_preparer.py` gera datasets estruturados:

#### Formato Gemini (JSONL)

```json
{"text_input": "Classifique o gasto 'BOVINOS' em uma categoria DRE.", "output": "O gasto 'BOVINOS' pertence ao grupo '( - ) CUSTOS VARIÁVEIS'."}
{"text_input": "Qual foi o valor de 'PIX' em Jan?", "output": "O valor de 'PIX' em Jan foi R$ 15.000,50."}
```

#### Formato OpenAI (JSONL)

```json
{"messages": [{"role": "user", "content": "Classifique..."}, {"role": "assistant", "content": "BOVINOS"}]}
```

### Requisitos Mínimos

| Requisito | Valor | Motivo |
|-----------|-------|--------|
| Pares Q&A | ≥ 100 | Mínimo para aprendizado |
| Cobertura | ≥ 80% | Todas categorias representadas |
| Diversidade | 3 tipos | Classificação, valor, narrativa |

---

## Métricas de Qualidade

### Métricas de Validação

```python
validation = {
    "total_pairs": 500,           # Total de exemplos
    "unique_categories": 45,      # Categorias cobertas
    "unique_groups": 8,           # Grupos DRE cobertos
    "avg_answer_length": 85.2,    # Tamanho médio resposta
    "is_valid": True,             # Passou validação
}
```

### Cobertura por Grupo

```python
coverage = {
    "RECEITAS S/ VENDAS": 1.0,        # 100% coberto
    "( - ) CUSTOS VARIÁVEIS": 0.85,   # 85% coberto
    "DESPESAS FIXAS": 0.90,           # 90% coberto
}
```

### Critérios de Aceitação

- [ ] Cobertura total ≥ 80%
- [ ] Nenhum grupo com cobertura < 50%
- [ ] Mínimo 100 pares Q&A
- [ ] Encoding UTF-8 válido

---

## Troubleshooting

### Problemas Comuns

#### 1. Classificação "OUTROS" frequente

**Causa**: Descrição muito genérica ou categoria não existe.

**Solução**:
- Verificar se categoria existe no `categories.json`
- Melhorar descrição da transação
- Adicionar nova categoria se necessário

#### 2. Categoria incorreta

**Causa**: Ambiguidade na descrição.

**Solução**:
```python
# Adicionar contexto adicional ao prompt
prompt += f"\nDICA: Considere que este é um restaurante de carnes."
```

#### 3. Erro de API (ERRO_IA)

**Causa**: API indisponível ou limite excedido.

**Solução**:
- Verificar `GEMINI_API_KEY`
- Implementar retry com backoff
- Usar fallback para categorias existentes

#### 4. Timeout em lote grande

**Causa**: Muitas requisições sequenciais.

**Solução**:
```python
# Implementar batch com delay
import time
for item in items:
    result = classificar_gasto(item)
    time.sleep(0.5)  # Rate limiting
```

---

## Referências

- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [OpenAI Fine-tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)
- [RAG Best Practices](https://www.pinecone.io/learn/retrieval-augmented-generation/)

---

*Documento atualizado em 19 de Janeiro de 2026*

