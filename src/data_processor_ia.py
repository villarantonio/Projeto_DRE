"""
Processador de Dados com IA e Trava de Segurança.

Este módulo processa dados financeiros com validação contra duplicidade
e classificação automática usando Google Gemini.

Refatorado para seguir a estrutura do projeto (src/).

Author: Projeto DRE - Manda Picanha
"""

import logging
import os
import sys
from pathlib import Path

import pandas as pd

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None

# Import config from parent
try:
    import config
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    import config


logger = logging.getLogger(__name__)


# --- CONFIGURAÇÕES ---
ARQUIVO_MESTRE = Path("relatorio_narrativo_ia.csv")
ARQUIVO_INPUT = Path("entrada.csv")

API_KEY = os.getenv("GEMINI_API_KEY")

# Modelo da IA (inicialização lazy)
_model = None


def get_model():
    """Retorna instância do modelo Gemini (singleton)."""
    global _model
    if _model is None and API_KEY and GENAI_AVAILABLE:
        genai.configure(api_key=API_KEY)
        _model = genai.GenerativeModel('gemini-2.0-flash')
    return _model


def carregar_dados(mestre_path: Path = None, input_path: Path = None):
    """
    Carrega dados do arquivo mestre e entrada.

    Args:
        mestre_path: Caminho para o arquivo mestre.
        input_path: Caminho para o arquivo de entrada.

    Returns:
        Tupla (df_mestre, df_novo).
    """
    mestre = mestre_path or ARQUIVO_MESTRE
    entrada = input_path or ARQUIVO_INPUT

    # Carrega o Mestre
    if mestre.exists():
        try:
            df_mestre = pd.read_csv(mestre, sep=';', encoding='utf-8')
        except Exception:
            df_mestre = pd.read_csv(mestre, sep=',', encoding='utf-8')
    else:
        logger.error(f"Arquivo mestre '{mestre}' não encontrado.")
        sys.exit(1)

    # Carrega a Entrada
    if entrada.exists():
        try:
            df_novo = pd.read_csv(entrada, sep=';', encoding='utf-8')
        except Exception:
            df_novo = pd.read_csv(entrada, sep=',', encoding='utf-8')
    else:
        logger.info("Arquivo de entrada não encontrado.")
        sys.exit(0)

    return df_mestre, df_novo


def trava_seguranca_duplicidade(df_mestre: pd.DataFrame, df_novo: pd.DataFrame) -> None:
    """
    Trava de segurança contra duplicidade de meses.

    Verifica se os meses no novo DataFrame já existem no mestre.
    Se existirem, interrompe a execução para evitar dados duplicados.

    Args:
        df_mestre: DataFrame com dados históricos.
        df_novo: DataFrame com novos dados.

    Raises:
        SystemExit: Se houver meses duplicados.
    """
    coluna_mes = 'Mes'

    if coluna_mes not in df_mestre.columns or coluna_mes not in df_novo.columns:
        logger.warning(f"Coluna '{coluna_mes}' não encontrada. Pulando validação.")
        return

    meses_existentes = set(df_mestre[coluna_mes].dropna().unique())
    meses_novos = set(df_novo[coluna_mes].dropna().unique())

    duplicados = meses_novos.intersection(meses_existentes)

    if duplicados:
        logger.error(f"⛔ BLOQUEIO: Mês(es) {list(duplicados)} já existe(m) no relatório.")
        print(f"⛔ BLOQUEIO DE SEGURANÇA: O mês {list(duplicados)} já existe no Relatório Narrativo.")
        print("A operação foi cancelada para evitar duplicidade de dados.")
        sys.exit(1)

    logger.info("✅ Validação de Mês: OK (Dados novos detectados).")
    print("✅ Validação de Mês: OK (Dados novos detectados).")


def classificar_gasto(descricao: str, categorias_validas: list) -> str:
    """
    Classifica um gasto usando IA.

    Args:
        descricao: Descrição do gasto.
        categorias_validas: Lista de categorias válidas.

    Returns:
        Categoria classificada ou "ERRO_IA"/"OUTROS".
    """
    model = get_model()
    if model is None:
        return "ERRO_IA"

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
    except Exception:
        return "ERRO_IA"


def processar_com_validacao(
    df_mestre: pd.DataFrame,
    df_novo: pd.DataFrame,
    output_path: Path = None
) -> pd.DataFrame:
    """
    Processa dados com validação e classificação.

    Args:
        df_mestre: DataFrame com dados históricos.
        df_novo: DataFrame com novos dados.
        output_path: Caminho para salvar resultado.

    Returns:
        DataFrame final com dados concatenados.
    """
    # 1. Validar duplicidade
    trava_seguranca_duplicidade(df_mestre, df_novo)

    # 2. Preparar contexto
    coluna_categoria = 'cc_nome'
    if coluna_categoria in df_mestre.columns:
        categorias = df_mestre[coluna_categoria].dropna().unique().tolist()
    else:
        categorias = ["Despesas Gerais", "Custos"]

    # 3. Classificar novos dados
    logger.info(f"Classificando {len(df_novo)} novos itens...")

    if coluna_categoria not in df_novo.columns:
        df_novo[coluna_categoria] = ""

    for i, row in df_novo.iterrows():
        desc = str(row.get('Descricao', ''))
        cat = classificar_gasto(desc, categorias)
        df_novo.at[i, coluna_categoria] = cat
        logger.info(f"Item: {desc[:20]}... -> {cat}")

    # 4. Append e retornar
    df_novo = df_novo.reindex(columns=df_mestre.columns, fill_value='')
    df_final = pd.concat([df_mestre, df_novo], ignore_index=True)

    # 5. Salvar se path fornecido
    if output_path:
        df_final.to_csv(output_path, sep=';', index=False, encoding='utf-8')
        logger.info(f"Arquivo salvo em {output_path}")

    return df_final


# =============================================================================
# Standalone Execution
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    if not API_KEY:
        print("Erro: GEMINI_API_KEY não configurada.")
        sys.exit(1)

    print(f"--- PROCESSADOR IA (src/data_processor_ia.py) ---")

    # Carregar dados
    df_mestre, df_novo = carregar_dados()

    if df_novo.empty:
        print("Entrada vazia. Nada a processar.")
        sys.exit(0)

    # Processar com validação
    df_final = processar_com_validacao(df_mestre, df_novo, ARQUIVO_MESTRE)

    print(f"✅ SUCESSO: Relatório atualizado com {len(df_novo)} novos itens.")

