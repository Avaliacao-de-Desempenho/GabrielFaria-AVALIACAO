## SEMANA 1: Analizador de documentos via IA
### Objetivo: Integrar API FastAPI com API do Gemini 
**02/07 - 04/07**
- **Backlog Semanal**
    - Obter chave da API Gemini, estudar documentação para futura integração ✅
    - Desenvolver API `FastAPI` em Python com métodos básicos (GET, POST, ...) ✅
    - Integrar upload de imagem à API ✅
    - Integrar API `FastAPI` com a API do Gemini, por meio de requisição via `requests` (python) ✅
    - Desenvolver prompt e formatar retorno do Gemini para um `JSON` padronizado ✅
    - Desenvolver `docker-compose` e rodar a API em um container local ✅
    
    - **Bônus**
      - Instalar dependências relativas à conexão com o Postgres ✅
      - Definir tabela ✅
        - ```mermaid
          erDiagram
          notas {
            serial id
            real valor
            varchar cnpj
            date data
          }
          ```
      - Integrar conexão com o Postgres no método `POST`, salvando os campos extraídos na tabela ✅
      - Integrar conexão com o Postgres no método `GET`, coletando todas as informações da tabela ✅
      - Definir container do banco no docker-compose com volume persistente ✅
      - Integrar container da API com o novo container do banco ✅

- **Resultado Esperado**
    - API desenvolvida em `FastAPI` que envia  um arquivo de uma nota fiscal e retorna o Valor Total, Data de Emissão e CNPJ em um `JSON` padronizado.
      - **02/07** - Em primeiro momento, criei uma chave da API Gemini e defini - com a ajuda do `PyPi` as dependências que necessitaria para a primeira parte do projeto. Com as dependências instaladas em um ambiente virtual `venv`, desenvolvi uma API simples com um único método `GET` que retornava um `Hello World`. A partir dessa API, comecei a desenvolver a aplicação em si, iniciando pelo método `POST`, que inicialmente recebia uma imagem e salvava no meu ambiente local. Vendo que a integração do `POST` com uma imagem funcionava, integrei a chave da API que tinha conseguido anteriormente e comecei fazendo requisições simples ao endpoint do Gemini com o intuito de testes. Com a requisição ao Gemini integrada, desenvolvi o prompt que iria utilizar e formatei o retorno em um `JSON` padronizado contendo apenas os campos requiridos (valor, CNPJ e data).
        - **Evolução**: 83%
        - **TODO**: Desenvolver `Dockerfile` e `docker-compose`, integrar com o banco de dados.
      - **03/07** - Em segundo momento, com a API já processando as imagens, trabalhei em subir a mesma em um container Docker. Desenvolvi um `Dockerfile` próprio para a API a partir da imagem padrão `Python` e buildei / rodei localmente. Depois que ela já estava rodando certinho, transportei a mesma ideia para um `docker-compose`, contendo apenas um container por enquanto. Com isso o objetivo definido da semana foi concluído!! E por isso decidi adiantar passos que viriam nas semanas posteriores. Comecei definindo a integração do banco com a API, instalando as dependências e desenvolvendo o método de conexão dentro da API. Com isso, desenvolvi a `query` que criaria a tabela e em seguida defini a lógica de inserção de dados na tabela via python. Parti da mesma lógica para o desenvolvimento da função `GET` também. Para realizar os testes, modifiquei para o `docker-compose` agora subir dois containeres: a API e o banco Postgres. Depois de alguns testes, consegui integrar os dois containeres e fazer com que o container do banco persistisse os dados, mesmo após seu desligamento!!
        - **Evolução**: 100% + **Integração com o banco**: 100%
        - **TODO**: Desenvolver um front-end para envio das imagens.

- **Dúvidas do Aluno/Impedimentos Encontrados**
    - \<DÚVIDAS\>

- **Questões para o Aluno**
    - \<QUESTÕES\>

- **Respostas das Questões**
    - \<RESPOSTAS\>

## SEMANA 2: \<NOME DO PROJETO\>
### Objetivo: \<OBJETIVO DA SEMANA\>
**07/07 - 11/07**
- **Backlog Semanal**
    - \<QUEBRAR O OBJETIVO DA SEMANA EM PARTES MENORES\>

- **Resultado Esperado**
    - \<QUAL ENTREGÁVEL SERÁ PRODUZIDO QUANDO O OBJETIVO FOR ALCANÇADO (FINAL DA SEMANA)\>
    - Evolução: \<0% - 100%\>

- **Dúvidas do Aluno/Impedimentos Encontrados**
    - \<DÚVIDAS\>

- **Questões para o Aluno**
    - \<QUESTÕES\>

- **Respostas das Questões**
    - \<RESPOSTAS\>

## SEMANA 3: \<NOME DO PROJETO\>
### Objetivo: \<OBJETIVO DA SEMANA\>
**14/07 - 17/07**
- **Backlog Semanal**
    - \<QUEBRAR O OBJETIVO DA SEMANA EM PARTES MENORES\>

- **Resultado Esperado**
    - \<QUAL ENTREGÁVEL SERÁ PRODUZIDO QUANDO O OBJETIVO FOR ALCANÇADO (FINAL DA SEMANA)\>
    - Evolução: \<0% - 100%\>

- **Dúvidas do Aluno/Impedimentos Encontrados**
    - \<DÚVIDAS\>

- **Questões para o Aluno**
    - \<QUESTÕES\>

- **Respostas das Questões**
    - \<RESPOSTAS\>
---
## Descrição do Projeto
Criar uma API em Python, usando FastAPI, que receba uma imagem (.jpg, .jpeg, .png) ou um PDF de uma Nota Fiscal; salve o Valor Total, Data de Emissão e CNPJ no banco de dados Postgres e retorne os mesmos campos em formato json.

A API e o banco de dados devem rodar localmente em docker e o projeto como um todo deve poder ser iniciado usando o "docker compose". Também é necessário que os dados persistam mesmo que os dockers sejam pausados ou desligados.

O ambiente local deve estar num ambiente virtual, criado com o "venv", e os pacotes devem estar listados no arquivo "requirements.txt".

## Stack
- Python
- Postgres
- FastAPI
- Docker
    - Dockerfile
    - Docker compose
- Gemini
    - API

## Referências
- Python
    - https://www.python.org/downloads/
    - https://www.python.org/doc/
- Repositório de pacotes python
    - https://pypi.org/
- Ambiente virtual
    - https://docs.python.org/pt-br/3/library/venv.html
- Docker
    - Dockerfile, build de imagem e rodar container: https://docs.docker.com/build/concepts/dockerfile/
    - Docker compose: https://docs.docker.com/compose/
- FastAPI
    - https://fastapi.tiangolo.com/tutorial/
    - https://fastapi.tiangolo.com/tutorial/first-steps/#step-4-define-the-path-operation-function
    - https://pypi.org/project/fastapi/
    - https://www.youtube.com/watch?v=7eCdONqaHDc
- Banco de dados
    - https://www.postgresql.org/
    - https://pypi.org/project/SQLAlchemy/
    - https://pypi.org/project/psycopg/
    - https://www.postgresql.org/docs/current/datatype.html
    - https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
    - https://stackoverflow.com/questions/26496388/how-to-connect-python-to-postgresql
- Gemini
    - https://aistudio.google.com/apikey

## Passo a Passo do Projeto
1. Fazer o setup do ambiente
    - criar repositório
    - instalar dependências
    - instalar docker
1. Criar api do projeto com o FastAPI
1. Fazer a extração de campos com Gemini
1. Adicionar integração com banco de dados

## Benchmarks
- Semana 1
    - setup inicial: repositório, pacotes, docker
    - testar fastapi
    - testar gemini
- Semana 2
    - desenvolver api para fazer extração de campos
- Semana 3
    - integrar com banco de dados
    - finalizar documentação
    - apresentação final

## Diretivas
- **Reuniões**  
    **07/07 (segunda)** - report de progresso e impedimentos  
    **10/07 (quinta)** - report de progresso e impedimentos  
    **15/07 (terça)** - report de progresso e impedimentos  
    **17/07 (quinta, apresentação final)** - apresentação do resultado final  
- Documentar código e processos durante todo o projeto  
- Fazer update diário do relatório  
- Fazer update diário do código  
- O repositório deve ter um nome padrão: \<NOME DO ALUNO\>-AVALIAÇÃO

## Avaliação
- Evolução técnica com base nos resultados semanais
- Autonomia no desenvolvimento e impedimentos
- Organização (repositório, report, documentação, git)