import base64
import json
import os

import functions_framework
import psycopg
import requests

# Implementação Cloud Build


def conectar_banco():
    """
    Função responsável por criar uma conexão com o banco de dados postgres.
    Caso a conexão com o banco falhe, retorna a exceção formatada como string.
    """
    try:
        conexao = psycopg.connect(
            dbname=os.environ["DB_POSTGRES"],
            user=os.environ["USUARIO_POSTGRES"],
            password=os.environ["SENHA_POSTGRES"],
            host=os.environ["URL_POSTGRES"],
        )
        return conexao
    except Exception as e:
        return str(e)


@functions_framework.http
def post(request):
    """
    Função destinada para envio de arquivo / processamento via Gemini da mesma

    Parâmetros:
        arquivo (UploadFile): Imagem da nota fiscal enviada via API.

    Retorno:
        JSON no seguinte formato:
        {
            "Valor": "R$XXX.XX",
            "CNPJ": "XX.XXX.XXX/XXXX-XX",
            "Data": "YYYY/MM/DD"
        }
    """

    if "arquivo" not in request.files:
        return (
            json.dumps({"erro": "Arquivo não enviado na requisição."}),
            400,
            {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            },
        )

    arquivo = request.files["arquivo"]

    CHAVE_API_GEMINI = os.environ.get("CHAVE_API_GEMINI")
    ENDPOINT_GEMINI = os.environ.get("ENDPOINT_GEMINI")

    try:
        # Recupera o arquivo na forma de bytes
        conteudo = arquivo.read()
        # Converte o arquivo (bytes) para base64, para enviar para o Gemini
        arquivo_base64 = base64.b64encode(conteudo).decode("utf-8")

        # Monta o cabecalho da requisição, passando a chave da API
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": CHAVE_API_GEMINI,
        }

        # Monta o payload para o Gemini
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "inline_data": {
                                "mime_type": arquivo.content_type,
                                "data": arquivo_base64,
                            }
                        },
                        {
                            "text": """
                            Me retorne os campos Valor Total, CNPJ e Data de Emissão desta nota fiscal. 
                            Não me retorne nenhum texto adicional, além dos campos formatados nesse formato:
                            {
                                "Valor": campo_valor_extraido_do_arquivo formatado como R$XXX.XX, lembre-se de trocar a vírgula por um ponto, deixando no formato americano de dinheiro, 
                                "CNPJ": campo_cnpj_extraido_do_arquivo formatado como XX.XXX.XXX/XXXX-XX,
                                "Data": campo_data_extraido_do_arquivo formatado como YYYY/MM/DD,
                            }
                            Caso os campos não sejam encontrados, substituir o valor extraído do arquivo por 'null'.
                            Não me retorne os dados formatados ou com espaçamento de linha entre eles. 
                            Retorne apenas a string pura contendo os campos e valores que forneci.
                        """
                        },
                    ]
                }
            ]
        }

        # Realiza a requisição, passando a imagem, prompt e headers para a API do Gemini
        resposta = requests.post(ENDPOINT_GEMINI, headers=headers, json=payload)

        # Retorna erro, caso haja algum
        if resposta.status_code != 200:
            return (
                json.dumps(
                    {"erro": "Erro ao processar imagem no Gemini: " + resposta.text}
                ),
                500,
                {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST, OPTIONS",
                    "Access-Control-Allow-Headers": "*",
                },
            )

        # Retorna resultado do gemini
        resposta_json = resposta.json()
        # Dentro dos metadados que o Gemini retorna, obtém o real retorno do prompt, ou seja, os campos Valor, CNPJ e Data
        campos = resposta_json["candidates"][0]["content"]["parts"][0]["text"]
        # O Gemini retorna os valores dentro de um markdown, por isso, substitui as partes que definem o markdown com strings vazias
        campos_formatado = json.loads(
            campos.replace("```json\n", "").replace("\n```", "")
        )

        # Cria o JSON de retorno com os campos devidamente formatados
        valor_retorno = {
            "Valor": campos_formatado["Valor"],
            "CNPJ": campos_formatado["CNPJ"],
            "Data": campos_formatado["Data"],
        }

        # Tenta se conectar com o banco
        conexao = conectar_banco()
        # Caso a conexão não tenha retornado uma string, quer dizer que a conexão foi bem sucedida e assim o código corre normalmente
        if not isinstance(conexao, str):
            with conexao:
                with conexao.cursor() as cursor:
                    # Cria a tabela se ela não existir (precaução)
                    cursor.execute(
                        "CREATE TABLE IF NOT EXISTS notas (id serial PRIMARY KEY, valor real, cnpj varchar, data date)"
                    )
                    # Insere os valores formatados na tabela
                    cursor.execute(
                        "INSERT INTO notas (valor, cnpj, data) VALUES (%s, %s, %s)",
                        (
                            float(
                                campos_formatado["Valor"].split("$")[1]
                            ),  # Extrai somente o valor formatado como float (exclui o R$)
                            campos_formatado["CNPJ"],
                            campos_formatado["Data"],
                        ),
                    )

                    conexao.commit()

                    return (
                        json.dumps(valor_retorno),
                        200,
                        {
                            "Content-Type": "application/json",
                            "Access-Control-Allow-Origin": "*",
                            "Access-Control-Allow-Methods": "POST, OPTIONS",
                            "Access-Control-Allow-Headers": "*",
                        },
                    )
        else:
            # Caso a conexão retorne uma string, quer dizer que houve um erro. Exibe o erro para o usuário
            return (
                json.dumps({"erro": conexao}),
                500,
                {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST, OPTIONS",
                    "Access-Control-Allow-Headers": "*",
                },
            )
    except Exception as e:
        return (
            json.dumps({"erro": str(e)}),
            500,
            {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            },
        )
