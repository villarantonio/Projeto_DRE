import pandas as pd
import google.generativeai as genai
import os
import sys

# --- CONFIGURAÇÕES ---
# Nome exato do seu arquivo principal (baseado no seu print)
ARQUIVO_MESTRE = "relatorio_narrativo_ia.csv" 
ARQUIVO_INPUT = "entrada.csv"

API_KEY = os.getenv("GEMINI_API_KEY")

# Configura a IA
if not API_KEY:
    print("Erro: Chave API não encontrada.")
    sys.exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

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

def classificar_gasto(descricao, categorias_validas):
    categorias_str = ", ".join(categorias_validas)
    prompt = f"""
    Classifique o gasto abaixo em UMA das categorias existentes.
    Contexto: [{categorias_str}]
    Gasto: "{descricao}"
    Responda apenas a categoria exata. Se não souber, responda "OUTROS".
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return "ERRO_IA"

def main():
    print("--- INICIANDO PROCESSAMENTO ---")
    
    # 1. Carregar
    df_mestre, df_novo = carregar_dados()
    
    # 2. Verificar se tem dados novos
    if df_novo.empty:
        print("O arquivo de entrada está vazio.")
        sys.exit(0)

    # 3. Pegar Categorias Existentes para ensinar a IA
    # Tenta achar a coluna de categoria (ajuste se o nome for diferente)
    col_cat = 'cc_nome' 
    if col_cat not in df_mestre.columns:
        # Tenta achar a primeira coluna de texto se não achar cc_nome
        col_cat = df_mestre.columns[2] 
    
    categorias = df_mestre[col_cat].dropna().unique().tolist()

    # 4. Classificar e Processar
    print(f"Classificando {len(df_novo)} novos itens...")
    
    # Garante que a coluna de categoria existe no novo
    if col_cat not in df_novo.columns:
        df_novo[col_cat] = ""

    for i, row in df_novo.iterrows():
        desc = str(row.get('Descricao', 'Sem descrição'))
        cat_ia = classificar_gasto(desc, categorias)
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