import base64
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
                    {"text": "Descreva o que está nesta imagem."},
                ]
            }
        ]
    }

    resposta = requests.post(ENDPOINT_GEMINI, headers=headers, json=payload)

    if resposta.status_code != 200:
        return JSONResponse(
            status_code=500,
            content={
                "erro": "Erro ao processar imagem no Gemini",
                "detalhe": resposta.text,
            },
        )

    resultado = resposta.json()
    return resultado
