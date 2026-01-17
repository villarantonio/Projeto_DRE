import pandas as pd
import google.generativeai as genai
import os
import sys

# --- CONFIGURAÇÕES ---
# O NOME DO SEU ARQUIVO ÚNICO (O RELATÓRIO NARRATIVO QUE VOCÊ JÁ TEM)
# Troque 'nome_do_seu_arquivo_narrativo.csv' pelo nome real que está no GitHub
ARQUIVO_MESTRE = "relatorio_narrativo_ia.csv" 

# O ARQUIVO 'ENVELOPE' (ONDE VOCÊ COLA OS DADOS NOVOS)
ARQUIVO_INPUT = "entrada.csv"

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def carregar_dados():
    # 1. Carrega o Relatório Mestre (Onde tudo fica guardado)
    if os.path.exists(ARQUIVO_MESTRE):
        try:
            # Tenta ler com ; (padrão Excel BR) ou , (padrão US)
            df_mestre = pd.read_csv(ARQUIVO_MESTRE, sep=';', encoding='utf-8')
        except:
            df_mestre = pd.read_csv(ARQUIVO_MESTRE, sep=',', encoding='utf-8')
    else:
        print(f"ERRO CRÍTICO: O arquivo mestre '{ARQUIVO_MESTRE}' não foi encontrado no repositório.")
        sys.exit(1)

    # 2. Carrega o Input (O envelope com os dados novos)
    if os.path.exists(ARQUIVO_INPUT):
        df_novo = pd.read_csv(ARQUIVO_INPUT, sep=';', encoding='utf-8')
    else:
        print("Arquivo 'entrada.csv' não encontrado. Nada a processar.")
        sys.exit(0)

    return df_mestre, df_novo

def trava_seguranca_duplicidade(df_mestre, df_novo):
    """
    TRAVA DE SEGURANÇA:
    Verifica se os meses que estamos tentando inserir JÁ EXISTEM no relatório narrativo.
    Isso impede que você duplique Agosto, por exemplo.
    """
    # IMPORTANTE: Ajuste 'Mes' para o nome exato da coluna de mês no seu arquivo
    coluna_mes = 'Mes' 
    
    if coluna_mes not in df_mestre.columns or coluna_mes not in df_novo.columns:
        print(f"Aviso: Coluna '{coluna_mes}' não encontrada para validação. Pulando trava.")
        return

    meses_existentes = df_mestre[coluna_mes].unique()
    meses_novos = df_novo[coluna_mes].unique()

    duplicados = [m for m in meses_novos if m in meses_existentes]

    if duplicados:
        print(f"⛔ BLOQUEIO DE SEGURANÇA: O mês {duplicados} já existe no Relatório Narrativo.")
        print("A operação foi cancelada para evitar duplicidade de dados.")
        sys.exit(1) # Força o erro para o GitHub avisar você
    
    print("✅ Validação de Mês: OK (Dados novos detectados).")

def classificar_gasto(descricao, categorias_validas):
    categorias_str = ", ".join(categorias_validas)
    prompt = f"""
    Atue como analista. Classifique o gasto abaixo em UMA das categorias existentes.
    Contexto: [{categorias_str}]
    Gasto: "{descricao}"
    Responda apenas a categoria. Use 'OUTROS' se não encaixar.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return "ERRO_IA"

def main():
    if not API_KEY:
        print("Erro: Chave API não configurada.")
        return

    print(f"--- ATUALIZANDO: {ARQUIVO_MESTRE} ---")
    
    # 1. Carregar
    df_mestre, df_novo = carregar_dados()
    
    # 2. Validar
    trava_seguranca_duplicidade(df_mestre, df_novo)

    # 3. Preparar Contexto (Lê as categorias do próprio arquivo mestre)
    coluna_categoria = 'cc_nome' # Nome da sua coluna de categorias
    if coluna_categoria in df_mestre.columns:
        categorias = df_mestre[coluna_categoria].dropna().unique().tolist()
    else:
        categorias = ["Despesas Gerais", "Custos"] # Fallback

    # 4. Classificar Novos Dados
    print(f"Classificando {len(df_novo)} novos itens...")
    
    # Garante que a coluna existe no novo
    if coluna_categoria not in df_novo.columns:
        df_novo[coluna_categoria] = ""

    for i, row in df_novo.iterrows():
        # Ajuste 'descricao_original' para o nome da coluna no seu CSV novo
        desc = str(row.get('Descricao', '')) 
        cat = classificar_gasto(desc, categorias)
        df_novo.at[i, coluna_categoria] = cat
        print(f"Item: {desc[:20]}... -> {cat}")

    # 5. Append (Colar no final)
    # Garante que as colunas estejam na mesma ordem
    df_novo = df_novo.reindex(columns=df_mestre.columns, fill_value='')
    
    df_final = pd.concat([df_mestre, df_novo], ignore_index=True)

    # 6. Salvar (Atualiza o Arquivo Mestre)
    df_final.to_csv(ARQUIVO_MESTRE, sep=';', index=False, encoding='utf-8')
    print("Sucesso! Relatório Narrativo atualizado.")

if __name__ == "__main__":
    main()