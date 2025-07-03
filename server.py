import base64
import json
import os

import psycopg2
import requests
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

# Instancia uma aplicação FastAPI
app = FastAPI(
    title="API - Analizador de notas fiscais",
    description="API desenvolvida utilizando FastAPI que integra a API do Gemini para recuperar campos de notas fiscais.",
    version="0.1.0",
)


# Recupera variáveis relativas à integração com GEMINI do .env
CHAVE_API_GEMINI = os.environ.get("CHAVE_API_GEMINI")
ENDPOINT_GEMINI = os.environ.get("ENDPOINT_GEMINI")


def conectar_banco():
    try:
        conexao = psycopg2.connect(
            dbname=os.environ["DB_POSTGRES"],
            user=os.environ["USUARIO_POSTGRES"],
            password=os.environ["SENHA_POSTGRES"],
            host="db",
            port="5432",
        )
        return conexao
    except Exception as e:
        return str(e)


@app.get("/")
def get_notas():
    conexao = conectar_banco()
    if not isinstance(conexao, str):
        cursor = conexao.cursor()

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS notas (id serial PRIMARY KEY, valor real, cnpj varchar, data date)"
        )

        cursor.execute("SELECT * FROM notas")
        resultado = cursor.fetchall()

        conexao.commit()

        cursor.close()
        conexao.close()

        return resultado
    else:
        return {"Erro": conexao}


@app.post("/docs/")
async def processar_documento(arquivo: UploadFile = File(...)):
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
    # Recupera o arquivo na forma de bytes
    conteudo = await arquivo.read()
    # Converte o arquivo (bytes) para base64, para enviar para o Gemini
    arquivo_base64 = base64.b64encode(conteudo).decode("utf-8")

    # Monta o cabecalho da requisição, passando a chave da API
    headers = {"Content-Type": "application/json", "X-goog-api-key": CHAVE_API_GEMINI}

    # Monta o payload para o gemini
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
                            "Valor": campo_valor_extraido_do_arquivo formatado como R$XXX.XX, lembre-se de trocar a vírgula por um ponto, 
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
        return JSONResponse(
            status_code=500,
            content={
                "erro": "Erro ao processar imagem no Gemini",
                "detalhe": resposta.text,
            },
        )

    # Retorna resultado do gemini
    resposta_json = resposta.json()
    # Dentro dos metadados que o Gemini retorna, obtém o real retorno do prompt, ou seja, os campos Valor, CNPJ e Data
    campos = resposta_json["candidates"][0]["content"]["parts"][0]["text"]
    # O Gemini retorna os valores dentro de um markdown, por isso, substitui as partes que definem o markdown com strings vazias
    campos_formatado = json.loads(campos.replace("```json\n", "").replace("\n```", ""))

    # Cria o JSON de retorno com os campos devidamente formatados
    valor_retorno = {
        "Valor": campos_formatado["Valor"],
        "CNPJ": campos_formatado["CNPJ"],
        "Data": campos_formatado["Data"],
    }

    conexao = conectar_banco()
    if not isinstance(conexao, str):
        cursor = conexao.cursor()

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS notas (id serial PRIMARY KEY, valor real, cnpj varchar, data date)"
        )
        cursor.execute(
            "INSERT INTO notas (valor, cnpj, data) VALUES (%s, %s, %s)",
            (
                float(campos_formatado["Valor"].split("$")[1]),
                campos_formatado["CNPJ"],
                campos_formatado["Data"],
            ),
        )

        conexao.commit()

        cursor.close()
        conexao.close()

        return valor_retorno
    else:
        return {"Erro": conexao}
