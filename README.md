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
python -m venv .venv

# Ativar no Windows:
venv\Scripts\activate

# Ativar no Linux/Mac:
source .venv/bin/activate
```

### 2. Instalação das Dependências
```Bash
pip install -r requirements.txt
```

### 3. Comando de Execução

Na raiz do projeto, execute o módulo principal assim:
```Bash
python -m src.main
```

### 4. Comando de Execução dos Testes

Na raiz do projeto, execute o módulo de testes assim:
```Bash
python -m pytest tests/
```


## decisões adotadas para tratar dados inválidos;

Registros que falham na validação (ausência de protocolo, data, ou e-mails em formatos incorretos) não interrompem a execução. São classificados como inválidos em uma coluna específica (registro_valido = False) e notificados no arquivo de log (output/erros.log).

Erros de valores não-numéricos na coluna de tempo de atendimento foram coagidos a NaN para garantir que as operações aritméticas do NumPy e Pandas continuassem de maneira segura.

A normalização de tempo (Min-Max) possui proteção contra divisão por zero.

Arquivos faltantes geram um Warning no log, e o programa cria estruturas nulas para não colapsar a pipeline de dados.

Linhas mal-formadas (excesso ou falta de colunas) são ignoradas e geram um Warning no log.


## Declaração de Uso de Ferramentas de Inteligência Artificial

## Ferramenta Utilizada

Gemini

## Finalidade

A ferramenta de inteligência artificial foi empregada pontualmente em três etapas do desenvolvimento:

Documentação do código: Inserção de comentários explicativos após a revisão do código, visando aumentar a clareza, a legibilidade e a manutenibilidade do sistema.

Elaboração de testes: Geração de sugestões e cenários de testes unitários para validar as funcionalidades desenvolvidas.

Auxílio na documentação externa: Apoio na estruturação e redação do arquivo README.md e na organização da documentação técnica geral do repositório.

## Exemplos Resumidos das Solicitações Realizadas (Prompts)

Documentação do código: "Analise o seguinte trecho de código e sugira comentários objetivos para explicar a função de cada bloco de forma clara."

Sugestão de testes: "Com base na função [nome da função], liste casos de teste recomendados."

Estruturação do README: "Corrija esse texto para um arquivo README.md e ajude a organizar cada tópico."

## Partes da Solução que Foram Revisadas ou Modificadas pelo Próprio Discente

Refinamento dos comentários: Todos os comentários sugeridos pela IA foram revisados para garantir alinhamento com a lógica real do sistema, removendo explicações redundantes e padronizando a nomenclatura.

Seleção e validação dos testes: As sugestões de testes foram filtradas, adaptadas para a biblioteca de testes utilizada no projeto e implementadas manualmente, corrigindo inconsistências de escopo.

Personalização da documentação: O conteúdo do README.md foi totalmente personalizado com as especificações reais do projeto, ajustando links, comandos exatos de terminal e corrigindo o tom do texto.
