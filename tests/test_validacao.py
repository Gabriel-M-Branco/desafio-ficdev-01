from src.validacao import validar_email

def test_validar_email_correto():
    assert validar_email("aluno.teste@etec.mt.gov.br") == True
    assert validar_email("contato123@gmail.com") == True

def test_validar_email_incorreto():
    assert validar_email("email-sem-arroba.com") == False
    assert validar_email("email@com-espaco .com") == False
    assert validar_email(None) == False