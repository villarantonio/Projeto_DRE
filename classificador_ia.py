import pandas as pd
import google.generativeai as genai
import requests
import io
import os

# --- CONFIGURAÇÃO ESPECÍFICA DA BRANCH ---
# URL Raw apontando para a branch 'narrativa-ia'
# IMPORTANTE: Substitua 'SEU_ARQUIVO_BASE.csv' pelo nome real do arquivo no repo
URL_CSV_GITHUB = "https://raw.githubusercontent.com/villarantonio/Projeto_DRE/narrativa-ia/relatorio_narrativo_ia.csv"

COLUNA_CATEGORIA = "cc_nome"
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def obter_categorias_do_github(url):
    print(f"Baixando dados da branch narrativa-ia: {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.content.decode('utf-8')
        df = pd.read_csv(io.StringIO(content), sep=';') # Confirme se o separador é ;
        
        if COLUNA_CATEGORIA not in df.columns:
            print(f"Erro: Coluna '{COLUNA_CATEGORIA}' não encontrada.")
            return []
            
        categorias = df[COLUNA_CATEGORIA].dropna().unique().tolist()
        return categorias
    except Exception as e:
        print(f"Erro ao acessar GitHub: {e}")
        return []

def classificar_transacao(descricao, lista_categorias):
    categorias_str = ", ".join(lista_categorias)
    prompt = f"""
    Atue como analista financeiro. Classifique o gasto abaixo usando APENAS uma das categorias da lista.
    LISTA PERMITIDA: [{categorias_str}]
    GASTO: "{descricao}"
    RESPOSTA (Apenas a categoria):
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "ERRO_API"

def main():
    if not API_KEY:
        print("ERRO: Configure a secret GEMINI_API_KEY no GitHub.")
        return

    categorias = obter_categorias_do_github(URL_CSV_GITHUB)
    
    if categorias:
        print(f"Sucesso! {len(categorias)} categorias carregadas para contexto.")
        
        # Teste rápido para validar no log do Actions
        teste = "Pagamento de servidor AWS"
        resultado = classificar_transacao(teste, categorias)
        print(f"Teste de classificação:\nInput: {teste}\nResultado: {resultado}")
    else:
        print("Falha ao carregar categorias.")

if __name__ == "__main__":
    main()