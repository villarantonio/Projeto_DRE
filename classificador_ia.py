"""
Classificador de Gastos Financeiros com IA (Google Gemini).

Este módulo classifica gastos financeiros automaticamente usando
Google Gemini 2.0 Flash e contexto RAG do arquivo categories.json.

Author: Projeto DRE - Manda Picanha
"""

import json
import os
import sys
from pathlib import Path

import pandas as pd
import google.generativeai as genai


# --- CONFIGURAÇÕES ---
ARQUIVO_MESTRE = "relatorio_narrativo_ia.csv"
ARQUIVO_INPUT = "entrada.csv"
CATEGORIES_JSON = Path(__file__).parent / "output" / "categories.json"

API_KEY = os.getenv("GEMINI_API_KEY")

# Configura a IA (só inicializa se API_KEY existir)
model = None
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')


def carregar_categorias_rag() -> dict:
    """
    Carrega categorias do arquivo JSON para contexto RAG.

    Returns:
        Dicionário com grupos e suas categorias.
    """
    if CATEGORIES_JSON.exists():
        with open(CATEGORIES_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def formatar_contexto_rag(categorias_dict: dict) -> str:
    """
    Formata o dicionário de categorias em texto para o prompt.

    Args:
        categorias_dict: Dicionário {grupo: [categorias]}.

    Returns:
        Texto formatado para o prompt da IA.
    """
    if not categorias_dict:
        return "Sem categorias disponíveis."

    contexto_partes = []
    for grupo, categorias in categorias_dict.items():
        cats_str = ", ".join(categorias)
        contexto_partes.append(f"- {grupo}: {cats_str}")

    return "\n".join(contexto_partes)

def carregar_dados():
    # 1. Carrega o Mestre (Seu histórico)
    if os.path.exists(ARQUIVO_MESTRE):
        # Tenta ler com ; ou ,
        try:
            df_mestre = pd.read_csv(ARQUIVO_MESTRE, sep=';', encoding='utf-8')
        except:
            df_mestre = pd.read_csv(ARQUIVO_MESTRE, sep=',', encoding='utf-8')
    else:
        print(f"ERRO: O arquivo '{ARQUIVO_MESTRE}' não foi encontrado.")
        sys.exit(1)

    # 2. Carrega a Entrada (Novos dados)
    if os.path.exists(ARQUIVO_INPUT):
        try:
            df_novo = pd.read_csv(ARQUIVO_INPUT, sep=';', encoding='utf-8')
        except:
            df_novo = pd.read_csv(ARQUIVO_INPUT, sep=',', encoding='utf-8')
    else:
        print("Arquivo 'entrada.csv' não encontrado. Nada a processar.")
        sys.exit(0)

    return df_mestre, df_novo

def classificar_gasto(descricao: str, categorias_validas: list, contexto_rag: str = "") -> str:
    """
    Classifica um gasto usando IA com contexto RAG.

    Args:
        descricao: Descrição do gasto a classificar.
        categorias_validas: Lista de categorias válidas (fallback).
        contexto_rag: Contexto formatado do categories.json.

    Returns:
        Categoria classificada ou "ERRO_IA"/"OUTROS".
    """
    if model is None:
        return "ERRO_IA"

    # Usa contexto RAG se disponível, senão usa lista simples
    if contexto_rag:
        contexto = f"""
HIERARQUIA DE CATEGORIAS FINANCEIRAS (DRE):
{contexto_rag}
"""
    else:
        contexto = f"Categorias disponíveis: {', '.join(categorias_validas)}"

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
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "ERRO_IA"


def main():
    """Função principal de processamento."""
    if not API_KEY:
        print("Erro: Chave API não encontrada.")
        sys.exit(1)

    print("--- INICIANDO PROCESSAMENTO COM RAG ---")

    # 1. Carregar dados
    df_mestre, df_novo = carregar_dados()

    # 2. Carregar contexto RAG do categories.json
    categorias_dict = carregar_categorias_rag()
    contexto_rag = formatar_contexto_rag(categorias_dict)

    if categorias_dict:
        print(f"✅ RAG carregado: {len(categorias_dict)} grupos de categorias")
    else:
        print("⚠️ categories.json não encontrado, usando categorias do CSV")

    # 4. Verificar se tem dados novos
    if df_novo.empty:
        print("O arquivo de entrada está vazio.")
        sys.exit(0)

    # 5. Pegar categorias do CSV como fallback
    col_cat = 'cc_nome'
    if col_cat not in df_mestre.columns:
        col_cat = df_mestre.columns[2] if len(df_mestre.columns) > 2 else df_mestre.columns[0]

    categorias_fallback = df_mestre[col_cat].dropna().unique().tolist()

    # 6. Classificar e Processar com RAG
    print(f"Classificando {len(df_novo)} novos itens...")

    # Garante que a coluna de categoria existe no novo
    if col_cat not in df_novo.columns:
        df_novo[col_cat] = ""

    for i, row in df_novo.iterrows():
        desc = str(row.get('Descricao', 'Sem descrição'))
        # Usa contexto RAG para classificação mais precisa
        cat_ia = classificar_gasto(desc, categorias_fallback, contexto_rag)
        df_novo.at[i, col_cat] = cat_ia
        print(f"> {desc} -> {cat_ia}")

    # 5. Salvar (Append)
    # Alinha as colunas para ficarem na mesma ordem
    df_novo = df_novo.reindex(columns=df_mestre.columns, fill_value='')
    
    df_final = pd.concat([df_mestre, df_novo], ignore_index=True)
    
    # Salva em cima do arquivo mestre
    df_final.to_csv(ARQUIVO_MESTRE, sep=';', index=False, encoding='utf-8')
    print(f"SUCESSO: {len(df_novo)} linhas adicionadas ao '{ARQUIVO_MESTRE}'.")

if __name__ == "__main__":
    main()