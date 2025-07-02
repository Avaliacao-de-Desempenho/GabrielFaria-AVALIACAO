import base64
import os

from fastapi import FastAPI, File, UploadFile

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
    with open("teste.png", "wb") as imagem:
        imagem.write(conteudo)

    return {"teste": "foi"}
