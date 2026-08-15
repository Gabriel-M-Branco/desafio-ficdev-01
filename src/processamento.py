import logging

import numpy as np
import pandas as pd

from src.validacao import validar_email


def padronizar_categoria(texto, mapa_categorias):
    """Mapeia o texto inserido de forma incorreta para a categoria oficial."""
    if pd.isna(texto):
        return "Desconhecida"

    texto_limpo = str(texto).strip().lower()
    for categoria_oficial, palavras_chave in mapa_categorias.items():
        if texto_limpo in [p.lower() for p in palavras_chave]:
            return categoria_oficial
    return "Outros"


def processar_dados(config, mapa_categorias):
    """Realiza a leitura, limpeza e processamento dos dados via Pandas."""
    caminho_csv = config.get("arquivo_atendimentos", "data/atendimentos.csv")
    sep = config.get("separador_csv", ";")

    try:
        # Importar os registros
        df = pd.read_csv(caminho_csv, sep=sep)
    except Exception as e:
        logging.error(f"Erro fatal ao ler o CSV: {e}")
        return None, 0

    total_linhas_originais = len(df)

    # Tolerância a falhas: se colunas essenciais não existirem, criá-las vazias
    colunas_esperadas = [
        "protocolo",
        "data",
        "email",
        "categoria",
        "tempo_minutos",
        "status",
    ]
    for col in colunas_esperadas:
        if col not in df.columns:
            df[col] = np.nan
            logging.warning(f"Coluna ausente no CSV, preenchida com nulos: {col}")

    # Tratamento: remover espaços, uniformizar
    df["email"] = df["email"].astype(str).str.strip().str.lower()
    df["protocolo"] = df["protocolo"].astype(str).str.strip().str.upper()
    df["status"] = df["status"].astype(str).str.strip().str.capitalize()

    # Converter datas, tratando formatos distintos (Coerce converte erros para NaT)
    df["data"] = pd.to_datetime(df["data"], errors="coerce")

    # Validar campos obrigatórios e rejeitar inválidos
    df["email_valido"] = df["email"].apply(validar_email)
    df["registro_valido"] = (
        df["email_valido"] & df["protocolo"].notna() & df["data"].notna()
    )

    # Separar os inválidos para log e estatísticas (RF03)
    df_invalidos = df[~df["registro_valido"]]
    for _, row in df_invalidos.iterrows():
        logging.warning(
            f"Registro rejeitado. Protocolo: {row['protocolo']}, Motivo: Campos essenciais inválidos ou e-mail malformado."
        )

    # Identificar e tratar registros duplicados pelo protocolo
    df = df.drop_duplicates(subset=["protocolo"], keep="last")

    # Padronizar categorias
    df["categoria_padronizada"] = df["categoria"].apply(
        lambda x: padronizar_categoria(x, mapa_categorias)
    )

    # Operação numérica com NumPy: Normalização dos tempos de atendimento (Min-Max)
    # Convertemos para numérico primeiro, forçando erros a NaN
    df["tempo_minutos"] = pd.to_numeric(df["tempo_minutos"], errors="coerce")

    tempo_min = df["tempo_minutos"].min()
    tempo_max = df["tempo_minutos"].max()

    # Proteção contra divisão por zero usando NumPy
    if pd.notna(tempo_min) and pd.notna(tempo_max) and tempo_max > tempo_min:
        df["tempo_normalizado"] = np.where(
            df["tempo_minutos"].notna(),
            (df["tempo_minutos"] - tempo_min) / (tempo_max - tempo_min),
            np.nan,
        )
    else:
        df["tempo_normalizado"] = np.nan

    return df, total_linhas_originais
