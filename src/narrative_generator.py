# Arquivo: src/narrative_generator.py
import pandas as pd
import os
import sys

# Tenta pegar o caminho do arquivo base, ou usa o padrão
INPUT_FILE = 'DRE_BI(BaseDRE).csv'
OUTPUT_FILE = 'relatorio_narrativo_ia.csv'

def clean_text(text):
    """Limpa caracteres corrompidos comuns em exportações brasileiras."""
    if not isinstance(text, str):
        return text
    
    # Mapa de correções (baseado no padrão que você me mostrou antes)
    replacements = {
        '': 'ç', 
        'Vrios': 'Vários',
        'Ms': 'Mês',
        'VARIVEIS': 'VARIÁVEIS',
        'DEDUES': 'DEDUÇÕES',
        'SERVIOS': 'SERVIÇOS',
        'CACHAA': 'CACHAÇA',
        'ALCLICAS': 'ALCOÓLICAS',
        'FRIAS': 'FÉRIAS',
        'SALRIO': 'SALÁRIO',
        'RESCISES': 'RESCISÕES'
    }
    
    for error, fix in replacements.items():
        text = text.replace(error, fix)
        
    return text.strip()

def create_narrative(row):
    """Transforma a linha de dados em uma frase natural."""
    try:
        # Pega valores com segurança (evita erro se coluna não existir)
        mes = row.get('Mês', 'N/D')
        grupo = row.get('Nome Grupo', 'Categoria Desconhecida')
        item = row.get('cc_nome', 'Item Desconhecido')
        valor = row.get('Realizado', '0')
        subcat = row.get('Camada03', '')
        
        # Constrói a frase
        narrativa = f"Em {mes}, o grupo '{grupo}' registrou um valor de {valor} referente ao item '{item}'"
        
        if subcat and subcat != item:
            narrativa += f" (Subcategoria: {subcat})."
        else:
            narrativa += "."
            
        return narrativa
    except Exception:
        return ""

def main():
    print(f"--- Iniciando Gerador de Narrativas ---")
    
    if not os.path.exists(INPUT_FILE):
        print(f"ERRO: Arquivo de entrada '{INPUT_FILE}' não encontrado na raiz.")
        sys.exit(1)

    try:
        # Lê o CSV ignorando as 4 primeiras linhas de metadados
        print(f"Lendo arquivo: {INPUT_FILE}")
        df = pd.read_csv(INPUT_FILE, sep=';', header=4, encoding='latin1')
        
        # Limpeza de colunas e dados
        df = df.dropna(how='all', axis=1)
        df.columns = [clean_text(col) for col in df.columns]
        
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].apply(clean_text)

        # Filtra linhas de cabeçalho repetido ou inválidas
        if 'Loja' in df.columns:
            df = df[df['Loja'].notna()]

        # Gera a coluna de IA
        print("Gerando narrativas...")
        df['Narrativa_IA'] = df.apply(create_narrative, axis=1)

        # Seleciona colunas chave para o arquivo final (mais limpo)
        cols_to_keep = ['Narrativa_IA', 'Mês', 'Nome Grupo', 'cc_nome', 'Realizado']
        # Mantém apenas colunas que realmente existem no DF
        cols_final = [c for c in cols_to_keep if c in df.columns]
        
        df_final = df[cols_final]

        # Salva
        df_final.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig', sep=';')
        print(f"Sucesso! Arquivo '{OUTPUT_FILE}' gerado com {len(df_final)} linhas.")

    except Exception as e:
        print(f"Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()