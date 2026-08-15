## identificação do discente ou equipe;

Equipe: Eduardo Lourenço Borges e Silva e Gabriel Moreira Branco
Turma: Vespertino

## descrição resumida da solução;

Esta é uma aplicação de linha de comando baseada em Python que automatiza a leitura, validação e organização de chamados de suporte técnico provenientes de múltiplas fontes (CSV, JSON, TXT). A solução consolida os dados padronizando categorias de problemas, normalizando textos, extraindo informações com Expressões Regulares, validando inconsistências e gerando relatórios gráficos estatísticos com auxílio das bibliotecas Pandas, NumPy e Matplotlib.


## instruções para criação e ativação do ambiente virtual;



### 1. Criação e Ativação do Ambiente Virtual
No terminal, execute:
```bash
# Criar o ambiente
python -m venv venv

# Ativar no Windows:
venv\Scripts\activate
# Ativar no Linux/Mac:
source venv/bin/activate
2. Instalação das Dependências
Bash
pip install -r requirements.txt
3. Comando de Execução
Na raiz do projeto, execute o módulo principal conforme os requisitos do desafio:

Bash
python -m src.main



## decisões adotadas para tratar dados inválidos;

Registros que falham na validação (ausência de protocolo, data, ou e-mails em formatos incorretos) não interrompem a execução. São classificados como inválidos em uma coluna específica (registro_valido = False) e notificados no arquivo de log (output/erros.log).

Erros de valores não-numéricos na coluna de tempo de atendimento foram coagidos a NaN para garantir que as operações aritméticas do NumPy e Pandas continuassem de maneira segura.

A normalização de tempo (Min-Max) possui proteção contra divisão por zero.

Arquivos faltantes geram um Warning no log, e o programa cria estruturas nulas para não colapsar a pipeline de dados.




## indicação de eventual uso de ferramentas de IA.

# Uso de ferramentas de IA

## ferramenta utilizada;

## finalidade;

## exemplos resumidos das solicitações realizadas (prompts);

## partes da solução que foram revisadas ou modificadas pelo próprio discente.
