import logging
import re


def validar_email(email):
    """Utiliza expressão regular para validar o formato de um e-mail."""
    
    if not isinstance(email, str):
        return False
    
    padrao = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(padrao, email.strip()))


def extrair_dados_observacoes(caminho_txt):
    """
    Lê o arquivo TXT e extrai os protocolos e telefones associados
    usando expressões regulares.
    """
    resultados = []
    # Padrão flexível: opcionalmente começa com SUP-, seguido por 4 dígitos, hífen, 4 dígitos
    padrao_protocolo = r"(?:SUP-)?\d{4}-\d{4}"
    # Padrão flexível: DD opcional entre parênteses, espaço opcional, 4 ou 5 dígitos, hífen opcional, 4 dígitos
    padrao_telefone = r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}"

    try:
        with open(caminho_txt, "r", encoding="utf-8") as f:
            linhas = f.readlines()
            for linha in linhas:
                protocolo = re.search(padrao_protocolo, linha)
                telefone = re.search(padrao_telefone, linha)

                if protocolo and telefone:
                    resultados.append(
                        {"protocolo": protocolo.group(), "telefone": telefone.group()}
                    )
    except FileNotFoundError:
        logging.warning(f"Arquivo de observações não encontrado: {caminho_txt}")

    return resultados
