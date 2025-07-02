import base64
import json
import os

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


@app.get("/")
def get_teste():
    return {"Hello": "World"}


@app.post("/docs/")
async def processar_documento(arquivo: UploadFile = File(...)):
    """
    Função destinada para envio de arquivo / processamento via Gemini da mesma

    Parâmetros:
        arquivo (UploadFile): Imagem da nota fiscal enviada via API.

    Retorno:
        JSON no seguinte formato:
        {
            "Valor": "R$XXX,XX",
            "CNPJ": "XX.XXX.XXX/XXXX-XX",
            "Data": "DD/MM/YYYY"
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
                            "Valor": campo_valor_extraido_do_arquivo, 
                            "CNPJ": campo_cnpj_extraido_do_arquivo,
                            "Data": campo_data_extraido_do_arquivo,
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

    return valor_retorno
