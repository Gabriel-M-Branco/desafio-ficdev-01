from src.validacao import validar_email, extrair_dados_observacoes
from src.processamento import padronizar_categoria

def test_validar_email_correto():
    assert validar_email("aluno.teste@etec.mt.gov.br") == True
    assert validar_email("contato123@gmail.com") == True

def test_validar_email_incorreto():
    assert validar_email("email-sem-arroba.com") == False
    assert validar_email("email@com-espaco .com") == False
    assert validar_email(None) == False

def test_padronizar_categoria():
    import pandas as pd

    mapa_mock = {
        "Acesso ao AVA": ["ava", "acesso ava"],
        "Senha": ["senha", "password"]
    }
    
    assert padronizar_categoria("  AVA  ", mapa_mock) == "Acesso ao AVA"
    assert padronizar_categoria("PASSWORD", mapa_mock) == "Senha"
    
    assert padronizar_categoria("meu computador quebrou", mapa_mock) == "Outros"
    
    assert padronizar_categoria(pd.NA, mapa_mock) == "Desconhecida"

def test_regex_extrair_dados(tmp_path):
    """
    Usa o 'tmp_path' do pytest para criar um arquivo temporário 
    e testar a leitura e o Regex sem sujar seu projeto.
    """
    arquivo_falso = tmp_path / "obs_teste.txt"
    arquivo_falso.write_text("O aluno do protocolo SUP-1234-5678 ligou do telefone (65) 99999-1234.")
    
    resultados = extrair_dados_observacoes(str(arquivo_falso))
    
    assert len(resultados) == 1
    assert resultados[0]["protocolo"] == "SUP-1234-5678"
    assert resultados[0]["telefone"] == "(65) 99999-1234"