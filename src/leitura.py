import os
import json
import logging
from typing import TypedDict

CAMINHO_CONFIG = "data/config.json"

class ConfiguracaoCaminhos(TypedDict):
    arquivo_atendimentos: str
    arquivo_categorias: str
    arquivo_observacoes: str
    diretorio_saida: str
    separador_csv: str

def ler_configuracoes(CAMINHO_CONFIG: str) -> ConfiguracaoCaminhos: 
    """Lê as configurações armazenadas em JSON."""

    if not os.path.exists(CAMINHO_CONFIG):
        raise FileNotFoundError(f"Arquivo de configuração não encontrado: {CAMINHO_CONFIG}")

    with open(CAMINHO_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


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
        logging.error(f"Arquivo não encontrado: {caminho_categorias}")
        return {}
    with open(caminho_categorias, "r", encoding="utf-8") as f:
        return json.load(f)
