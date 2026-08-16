import json
import logging
import os
from typing import TypedDict

CAMINHO_CONFIG = "data/config.json"


class ConfiguracaoCaminhos(TypedDict):
    arquivo_atendimentos: str
    arquivo_categorias: str
    arquivo_observacoes: str
    diretorio_saida: str
    separador_csv: str


def ler_configuracoes() -> ConfiguracaoCaminhos:
    """Lê as configurações armazenadas em JSON ou usa um padrão se falhar."""

    if not os.path.exists(CAMINHO_CONFIG):
        print(f"AVISO: Arquivo de configuração não encontrado em '{CAMINHO_CONFIG}'.")
        print("Carregando configurações padrão do sistema...")
        return {
            "arquivo_atendimentos": "data/atendimentos.csv",
            "arquivo_categorias": "data/categorias.json",
            "arquivo_observacoes": "data/observacoes.txt",
            "diretorio_saida": "output",
            "separador_csv": ";"
        }

    try:
        with open(CAMINHO_CONFIG, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"AVISO: O arquivo de configuração está corrompido ({e}).")
        print("Carregando configurações padrão do sistema...")
        return {
            "arquivo_atendimentos": "data/atendimentos.csv",
            "arquivo_categorias": "data/categorias.json",
            "arquivo_observacoes": "data/observacoes.txt",
            "diretorio_saida": "output",
            "separador_csv": ";"
        }


def garantir_diretorios(config):
    """Verifica e cria os diretórios de saída necessários."""
    
    dir_saida = config.get("diretorio_saida", "output")
    dir_graficos = os.path.join(dir_saida, "graficos")

    os.makedirs(dir_saida, exist_ok=True)
    os.makedirs(dir_graficos, exist_ok=True)

    return dir_saida


def ler_categorias(caminho_categorias):
    """Lê o arquivo de categorias."""

    if not os.path.exists(caminho_categorias):
        logging.warning(f"Arquivo de categorias não encontrado: {caminho_categorias}")
        return {}
    
    with open(caminho_categorias, "r", encoding="utf-8") as f:
        return json.load(f)
