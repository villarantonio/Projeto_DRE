import pandas as pd
import os
import sys

# Configurações
INPUT_FILE = 'DRE_BI(BaseDRE).csv'
OUTPUT_FILE = 'relatorio_narrativo_ia.csv'

def find_header_row_safe(filepath):
    """
    Lê o arquivo como texto puro para achar o cabeçalho sem travar o Pandas.
    """
    try:
        with open(filepath, 'r', encoding='latin1') as f:
            for i, line in enumerate(f):
                # Para não ler o arquivo todo, para na linha 50
                if i > 50: 
                    break
                
                # Converte para minúsculo para verificar
                line_lower = line.lower()
                
                # Procura as palavras-chave mágicas
                if 'loja' in line_lower and 'realizado' in line_lower:
                    return i
        return 4 # Retorno padrão se não achar
    except Exception as e:
        print(f"Aviso: Erro ao ler texto bruto ({e}). Usando padrão 4.")
        return 4

def clean_column_name(col_name):
    if not isinstance(col_name, str): return str(col_name)
    col = col_name.strip().lower()
    if 'mês' in col or 'mes' in col or 'ms' in col: return 'Mês'
    if 'grupo' in col: return 'Nome Grupo'
    if 'realizado' in col: return 'Realizado'
    if 'cc_nome' in col or 'item' in col: return 'cc_nome'
    if 'camada03' in col: return 'Camada03'
    return col_name.strip()

def create_narrative(row):
    try:
        mes = row.get('Mês', 'N/D')
        grupo = row.get('Nome Grupo', 'Grupo Desconhecido')
        item = row.get('cc_nome', 'Item Desconhecido')
        valor = row.get('Realizado', '0')
        subcat = row.get('Camada03', '')
        
        narrativa = f"Em {mes}, o grupo '{grupo}' registrou {valor} referente a '{item}'"
        if subcat and subcat != item and str(subcat).lower() != 'nan':
            narrativa += f" ({subcat})."
        else:
            narrativa += "."
        return narrativa
    except:
        return ""

def main():
    print("--- Iniciando Processamento Blindado ---")
    
    if not os.path.exists(INPUT_FILE):
        print(f"ERRO: Arquivo {INPUT_FILE} não encontrado.")
        # Lista arquivos para debug no GitHub Actions
        print("Arquivos na pasta atual:", os.listdir())
        sys.exit(1)

    # 1. Acha a linha certa SEM usar Pandas (seguro)
    header_row = find_header_row_safe(INPUT_FILE)
    print(f"Cabeçalho detectado na linha índice: {header_row}")

    try:
        # 2. Carrega com Pandas pulando explicitamente o lixo
        # 'on_bad_lines' ajuda a ignorar linhas quebradas se houver mais alguma
        df = pd.read_csv(
            INPUT_FILE, 
            sep=';', 
            header=header_row, 
            encoding='latin1',
            on_bad_lines='skip' 
        )
        
        # 3. Limpeza
        new_columns = {col: clean_column_name(col) for col in df.columns}
        df = df.rename(columns=new_columns)
        
        # Remove a linha de repetição do cabeçalho se ela existir nos dados
        if 'Realizado' in df.columns:
            df = df[df['Realizado'] != 'Realizado']
            df = df[df['Realizado'].notna()]

        # 4. Geração
        print(f"Processando {len(df)} linhas de dados...")
        df['Narrativa_IA'] = df.apply(create_narrative, axis=1)
        
        # 5. Salva
        cols_to_save = ['Narrativa_IA', 'Mês', 'Nome Grupo', 'cc_nome', 'Realizado']
        cols_final = [c for c in cols_to_save if c in df.columns]
        
        df[cols_final].to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig', sep=';')
        print(f"Sucesso! Arquivo gerado.")

    except Exception as e:
        print(f"Erro fatal durante o processamento: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()