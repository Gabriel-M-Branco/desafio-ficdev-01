import logging
import numpy as np
import pandas as pd
from src.validacao import validar_email


def tratar_linha_malformada(linha_ruim):
    logging.warning(f"Linha ignorada por erro estrutural (excesso/falta de colunas): {linha_ruim}")
    return None


def padronizar_categoria(texto, mapa_categorias):
    if pd.isna(texto):
        return "Desconhecida"
    texto_limpo = str(texto).strip().lower()
    for categoria_oficial, palavras_chave in mapa_categorias.items():
        if texto_limpo in [p.lower() for p in palavras_chave]:
            return categoria_oficial
    return "Outros"


def carregar_csv(caminho_csv, sep):
    """Etapa 1: Leitura resiliente do CSV."""
    try:
        df = pd.read_csv(
            caminho_csv, 
            sep=sep, 
            engine='python', 
            on_bad_lines=tratar_linha_malformada
        )
        return df
    except FileNotFoundError:
        logging.warning(f"Arquivo CSV não encontrado: '{caminho_csv}'. Verifique o caminho.")
    except pd.errors.EmptyDataError:
        logging.error(f"O arquivo CSV '{caminho_csv}' está completamente vazio.")
    except pd.errors.ParserError as e:
        logging.error(f"Erro severo de formatação ao processar o CSV: {e}")
    except Exception as e:
        logging.error(f"Erro inesperado ao ler o CSV: {e}")
    return None


def garantir_colunas(df, colunas_esperadas):
    """Etapa 2: Garantia de integridade das colunas."""
    for col in colunas_esperadas:
        if col not in df.columns:
            df[col] = np.nan
            logging.warning(f"Coluna ausente no CSV, preenchida com nulos: {col}")
    return df


def limpar_e_formatar_textos(df):
    """Etapa 3: Limpeza básica de strings e datas."""
    df["email"] = df["email"].fillna("").astype(str).str.strip().str.lower()
    df["protocolo"] = df["protocolo"].fillna("").astype(str).str.strip().str.upper()
    df["status"] = df["status"].fillna("").astype(str).str.strip().str.capitalize()
    
    df["data_original"] = df["data"] 
    df["data"] = pd.to_datetime(df["data"], format="mixed", dayfirst=True, errors="coerce")
    return df


def validar_e_logar_inconsistencias(df):
    """Etapa 4: Validação das regras de negócio e geração de logs cirúrgicos."""
    df["email_valido"] = df["email"].apply(validar_email)
    df["protocolo_valido"] = df["protocolo"] != ""
    df["data_valida"] = df["data"].notna()

    df["registro_valido"] = (
        df["email_valido"] & df["protocolo_valido"] & df["data_valida"]
    )

    df_invalidos = df[~df["registro_valido"]]
    for _, row in df_invalidos.iterrows():
        motivos = []
        if not row["protocolo_valido"]: motivos.append("Protocolo ausente")
        if not row["data_valida"]: motivos.append(f"Data inválida ('{row['data_original']}')")
        if not row["email_valido"]: motivos.append(f"E-mail malformado ('{row['email']}')")

        motivos_str = " + ".join(motivos)
        protocolo_log = row["protocolo"] if row["protocolo"] != "" else "SEM_PROTOCOLO"
        logging.warning(f"Rejeitado [{protocolo_log}] -> Motivo: {motivos_str}")
        
    return df


def normalizar_tempo_atendimento(df):
    """Etapa 5: Operação numérica com NumPy."""
    df["tempo_minutos"] = pd.to_numeric(df["tempo_minutos"], errors="coerce")
    tempo_min = df["tempo_minutos"].min()
    tempo_max = df["tempo_minutos"].max()

    if pd.notna(tempo_min) and pd.notna(tempo_max) and tempo_max > tempo_min:
        df["tempo_normalizado"] = np.where(
            df["tempo_minutos"].notna(),
            (df["tempo_minutos"] - tempo_min) / (tempo_max - tempo_min),
            np.nan,
        )
    else:
        df["tempo_normalizado"] = np.nan
    return df


def processar_dados(config, mapa_categorias):
    """Função orquestradora: Chama as etapas na ordem correta."""
    caminho_csv = config.get("arquivo_atendimentos", "data/atendimentos.csv")
    sep = config.get("separador_csv", ";")

    df = carregar_csv(caminho_csv, sep)
    if df is None:
        return None, 0
    total_linhas_originais = len(df)

    colunas_esperadas = ["protocolo", "data", "email", "categoria", "tempo_minutos", "status"]
    df = garantir_colunas(df, colunas_esperadas)
    df = limpar_e_formatar_textos(df)

    df = validar_e_logar_inconsistencias(df)

    df = df.drop_duplicates(subset=["protocolo"], keep="last")
    df["categoria_padronizada"] = df["categoria"].apply(
        lambda x: padronizar_categoria(x, mapa_categorias)
    )
    df = normalizar_tempo_atendimento(df)

    return df, total_linhas_originais